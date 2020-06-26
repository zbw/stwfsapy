# Copyright 2020 Leibniz Information Centre for Economics
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from typing import FrozenSet, List, Iterable, Container, Tuple, TypeVar
import rdflib
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.tree import DecisionTreeClassifier
from scipy.sparse import csr_matrix
from stwfsapy import thesaurus as t
from stwfsapy.automata import nfa, construction, conversion
from stwfsapy.thesaurus_features import ThesaurusFeatureTransformation
from stwfsapy.text_features import mk_text_features
from stwfsapy import case_handlers


T = TypeVar('T')
N = TypeVar('N', int, float)
Nl = TypeVar('Nl', List[int], List[float])


class StwfsapyPredictor(BaseEstimator, ClassifierMixin):
    """Finds labels of thesaurus concepts in texts
    and assigns them a score."""
    def __init__(
            self,
            graph: rdflib.graph.Graph,
            concept_type_uri: rdflib.term.URIRef,
            sub_thesaurus_type_uri: rdflib.term.URIRef,
            remove_deprecated: bool = True,
            langs: FrozenSet[str] = frozenset(),
            handle_title_case: bool = True,
            ):
        """Creates the predictor.
        Args:
            graph: The SKOS onthology used to extract the labels.
            concept_type_uri
                The uri of the concept type.
                It is assumed that for every concept c,
                there is a triple (c, RDF.type, concept_type_uri)
                in the graph.
            sub_thesaurus_type_uri: The uri of the concept type.
                It is assumed that for every sub thesaurus t,
                there is a triple (t, RDF.type, sub_thesaurus_type_uri)
                in the graph.
            remove_deprecated: When True will discard deprecated subjects.
                Deprecation of a subject has to be indicated by
                a triple (s, OWL.deprecated, Literal(True)) in the graph.
            langs: For each language present in the set,
                labels will be extracted from the graph.
                An empy set or None will extract labels regardless of language.
            handle_title_case: When True, will also match labels in title case.
                I.e., in a text the first letter of every word can be upper
                or lower case and will still be matched.
                When False only the case of the first word's first letter
                will be adapted.
                Example:
                    * Given a label "garbage can" and the
                        title "Oscar Lives in a Garbage Can"
                    * When handle_title_case == True
                        the label will match the text.
                    * When handle_title_case == False
                        the label will not match the text.
                        It would however still match
                        "Garbage can is home to grouchy neighbor."."""
        self.graph = graph
        self.concept_type_uri = concept_type_uri
        self.sub_thesaurus_type_uri = sub_thesaurus_type_uri
        self.remove_deprecated = remove_deprecated
        self.langs = langs
        self.handle_title_case = handle_title_case

    def _init(self):
        all_deprecated = set(t.extract_deprecated(self.graph))
        concepts = set(t.extract_by_type_uri(
            self.graph,
            self.concept_type_uri,
            remove=all_deprecated))
        thesauri = set(t.extract_by_type_uri(
            self.graph,
            self.sub_thesaurus_type_uri,
            remove=all_deprecated
        ))
        self.concept_map_ = dict(zip(concepts, range(len(concepts))))
        thesaurus_features = ThesaurusFeatureTransformation(
            self.graph,
            concepts,
            thesauri
        )
        labels = t.retrieve_concept_labels(
            self.graph,
            allowed=concepts,
            langs=self.langs)
        nfautomat = nfa.Nfa()
        if self.handle_title_case:
            case_handler = case_handlers.title_case_handler
        else:
            case_handler = case_handlers.sentence_case_handler
        for concept, label in labels:
            construction.ConstructionState(
                nfautomat,
                case_handler(label),
                concept
            ).construct()
        nfautomat.remove_empty_transitions()
        converter = conversion.NfaToDfaConverter(nfautomat)
        self.dfa_ = converter.start_conversion()
        self.pipeline_ = Pipeline([
            ("Combined Features", ColumnTransformer([
                ("Thesaurus Features", thesaurus_features, 0),
                ("Text Features", mk_text_features(), 1)])),
            ("Classifier", DecisionTreeClassifier(
                min_samples_leaf=25,
                max_leaf_nodes=100))
        ])

    def fit(self, X, y=None):
        self._init()
        return self._fit_after_init(X, y=y)

    def _fit_after_init(self, X, y=None):
        matches, train_y = self.match_and_extend(X, y)
        self.pipeline_.fit(matches, y=train_y)
        return self

    def predict_proba(self, X) -> csr_matrix:
        match_X, doc_counts = self.match_and_extend(X)
        predictions = self.pipeline_.predict_proba(match_X)[:, 1]
        return self._create_sparse_matrix(
            predictions,
            match_X,
            doc_counts
        )

    def suggest_proba(
            self,
            texts
            ) -> List[List[Tuple[rdflib.term.URIRef, float]]]:
        """For a given list of texts,
        this method returns the matched concepts and their scores."""
        match_X, doc_counts = self.match_and_extend(texts)
        predictions = self.pipeline_.predict_proba(match_X)[:, 1]
        combined = StwfsapyPredictor._collect_prediction_results(
            predictions,
            match_X,
            doc_counts
        )
        return [
            [
                (concept, score)
                for concept, score
                in zip(concepts, scores)
            ]
            for concepts, scores
            in combined
        ]

    def predict(self, X) -> csr_matrix:
        match_X, doc_counts = self.match_and_extend(X)
        predictions = self.pipeline_.predict(match_X)
        return self._create_sparse_matrix(
            predictions,
            match_X,
            doc_counts
        )

    def _create_sparse_matrix(
            self,
            values: Nl,
            tuples: List[Tuple[T, str]],
            doc_counts: List[int]
            ) -> csr_matrix:
        return csr_matrix(
            (
                values,
                (
                    [
                        doc_idx
                        for doc_idx
                        in range(len(doc_counts))
                        for _
                        in range(doc_counts[doc_idx])
                        ],
                    [
                        self.concept_map_.get(tpl[0])
                        for tpl
                        in tuples
                    ]
                )),
            shape=(len(doc_counts), len(self.concept_map_))
        )

    @staticmethod
    def _collect_prediction_results(
            values: Nl,
            tuples: List[Tuple[T, str]],
            doc_counts: List[int]
            ) -> List[Tuple[List[T], Nl]]:
        ret = []
        start = 0
        for count in doc_counts:
            end = start+count
            ret.append(([t[0] for t in tuples[start:end]], values[start:end]))
            start = end
        return ret

    def match_and_extend(
            self,
            texts: Iterable[str],
            truth_refss: Iterable[Container] = None
            ) -> Tuple[List[Tuple[rdflib.term.URIRef, str]], List[int]]:
        """Retrieves concepts by their labels from text.
        If ground truth values are present,
        it will also return a list of labels for scoring matches.
        If no ground truth values are present, a list
        with the number of matched concepts for each document is returned."""
        concepts = []
        if truth_refss is not None:
            ret_y = []
            for text, truth_refs in zip(texts, truth_refss):
                for match in self.dfa_.search(text):
                    concept = match[0]
                    text = match[1]
                    concepts.append((concept, text))
                    ret_y.append(int(concept in truth_refs))
            return concepts, ret_y
        else:
            doc_counts: List[int] = []
            for text in texts:
                count = 0
                for match in self.dfa_.search(text):
                    count += 1
                    concept = match[0]
                    text = match[1]
                    concepts.append((concept, text))
                doc_counts.append(count)
            return concepts, doc_counts
