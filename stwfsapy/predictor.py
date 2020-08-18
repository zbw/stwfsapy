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


from typing import FrozenSet, List, Iterable, Container, Tuple, TypeVar, Union
from rdflib.term import URIRef
from rdflib import Graph
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.tree import DecisionTreeClassifier
from scipy.sparse import csr_matrix
from stwfsapy import thesaurus as t
from stwfsapy.automata import nfa, construction, conversion, dfa
from stwfsapy.thesaurus_features import ThesaurusFeatureTransformation
from stwfsapy.text_features import mk_text_features
from stwfsapy import case_handlers
from stwfsapy import expansion
import pickle as pkl
from json import dumps, loads
from zipfile import ZipFile


T = TypeVar('T')
N = TypeVar('N', int, float)
Nl = TypeVar('Nl', List[int], List[float])


_KEY_DFA = 'dfa'
_KEY_PIPELINE = 'pipeline'
_KEY_CONCEPT_MAP = 'concept_map'
_KEY_GRAPH_ITEMS = 'graph_items'
_KEY_CONCEPT_TYPE_URI = 'concept_type_uri'
_KEY_THESAURUS_TYPE_URI = 'thesaurus_type_uri'
_KEY_THESAURUS_RELATION_TYPE_URI = 'thesaurus_relation_type_uri'
_KEY_THESAURUS_RELATION_IS_SPECIALISATION = (
    'thesaurus_relation_is_specialisation')
_KEY_REMOVE_DEPRECATED = 'remove_deprecated'
_KEY_LANGS = 'langs'
_KEY_HANDLE_TITLE_CASE = 'handle_title_case'
_KEY_EXTRACT_UPPER_CASE_FROM_BRACES = 'extract_upper_case_from_braces'
_KEY_EXTRACT_ANY_CASE_FROM_BRACES = 'extract_any_key_from_braces'
_KEY_EXPAND_AMPERSAND_WITH_SPACES = 'expand_ampersand_with_spaces'
_KEY_EXPAND_ABBREVIATION_WITH_PUNCTUATION = (
    'expand_abbreviation_with_punctuation')
_KEY_SIMPLE_ENGLISH_PLURAL_RULES = 'simple_english_plural_rules'

_NAME_GRAPH_FILE = 'graph.rdf'
_NAME_PIPELINE_FILE = 'pipeline.pkl'
_NAME_PREDICTOR_FILE = 'predictor.json'


class StwfsapyPredictor(BaseEstimator, ClassifierMixin):
    """Finds labels of thesaurus concepts in texts
    and assigns them a score."""
    def __init__(
            self,
            graph: Graph,
            concept_type_uri: Union[str, URIRef],
            sub_thesaurus_type_uri: Union[str, URIRef],
            thesaurus_relation_type_uri: Union[str, URIRef],
            thesaurus_relation_is_specialisation: bool = False,
            remove_deprecated: bool = True,
            langs: FrozenSet[str] = frozenset(),
            handle_title_case: bool = True,
            extract_upper_case_from_braces: bool = True,
            extract_any_case_from_braces: bool = False,
            expand_ampersand_with_spaces: bool = True,
            expand_abbreviation_with_punctuation: bool = True,
            simple_english_plural_rules: bool = False,
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
            thesaurus_relation_type_uri:
                Uri of the relation that links concepts to thesauri.
            thesaurus_relation_is_specialisation:
                Indicates whether the thesaurus_relation links thesauri to
                concepts or the other way round.
                E.g., for the relation skos:broader it should be false.
                Conversely it should be true for skos:narrower.
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
        if isinstance(concept_type_uri, str):
            concept_type_uri = URIRef(concept_type_uri)
        self.concept_type_uri = concept_type_uri
        if isinstance(sub_thesaurus_type_uri, str):
            sub_thesaurus_type_uri = URIRef(sub_thesaurus_type_uri)
        self.sub_thesaurus_type_uri = sub_thesaurus_type_uri
        if isinstance(thesaurus_relation_type_uri, str):
            thesaurus_relation_type_uri = URIRef(thesaurus_relation_type_uri)
        self.thesaurus_relation_type_uri = thesaurus_relation_type_uri
        self.thesaurus_relation_is_specialisation = (
            thesaurus_relation_is_specialisation)
        self.remove_deprecated = remove_deprecated
        self.langs = langs
        self.handle_title_case = handle_title_case
        self.extract_upper_case_from_braces = extract_upper_case_from_braces
        self.extract_any_case_from_braces = extract_any_case_from_braces
        self.expand_ampersand_with_spaces = expand_ampersand_with_spaces
        self.expand_abbreviation_with_punctuation = \
            expand_abbreviation_with_punctuation
        self.simple_english_plural_rules = simple_english_plural_rules

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
        self.concept_map_ = dict(zip(map(str, concepts), range(len(concepts))))
        thesaurus_features = ThesaurusFeatureTransformation(
            self.graph,
            concepts,
            thesauri,
            self.thesaurus_relation_type_uri,
            self.thesaurus_relation_is_specialisation
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
        expansion_funs = expansion.collect_expansion_functions(
            extract_upper_case_from_braces=self.extract_upper_case_from_braces,
            extract_any_case_from_braces=self.extract_any_case_from_braces,
            expand_ampersand_with_spaces=self.expand_ampersand_with_spaces,
            expand_abbreviation_with_punctuation=(
                self.expand_abbreviation_with_punctuation),
        )
        if self.simple_english_plural_rules:
            plural_fun = expansion.simple_english_plural_fun
        else:
            def plural_fun(x):
                return x
        for concept, label in labels:
            expanded = label
            for f in expansion_funs:
                expanded = f(expanded)
            construction.ConstructionState(
                nfautomat,
                plural_fun(case_handler(expanded)),
                str(concept)
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

    def fit(self, X, y=None, **kwargs):
        self._init()
        return self._fit_after_init(X, y=y)

    def _fit_after_init(self, X, y=None):
        matches, train_y = self.match_and_extend(X, y)
        self.pipeline_.fit(matches, y=train_y)
        return self

    def predict_proba(self, X) -> csr_matrix:
        match_X, doc_counts = self.match_and_extend(X)
        if match_X:
            predictions = self.pipeline_.predict_proba(match_X)[:, 1]
        else:
            predictions = []
        return self._create_sparse_matrix(
            predictions,
            match_X,
            doc_counts
        )

    def suggest_proba(
            self,
            texts
            ) -> List[List[Tuple[str, float]]]:
        """For a given list of texts,
        this method returns the matched concepts and their scores."""
        match_X, doc_counts = self.match_and_extend(texts)
        if match_X:
            predictions = self.pipeline_.predict_proba(match_X)[:, 1]
        else:
            predictions = []
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
        if match_X:
            predictions = self.pipeline_.predict(match_X)
        else:
            predictions = []
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
            ) -> Tuple[List[Tuple[str, str]], List[int]]:
        """Retrieves concepts by their labels from text.
        If ground truth values are present,
        it will also return a list of labels for scoring matches.
        If no ground truth values are present, a list
        with the number of matched concepts for each document is returned."""
        concepts = []
        if truth_refss is not None:
            ret_y = []
            for text, truth_refs in zip(texts, map(str, truth_refss)):
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

    def store(self, path):
        with ZipFile(path, 'w') as zfile:
            with zfile.open(_NAME_PREDICTOR_FILE, 'w') as fp:
                fp.write(
                    dumps({
                        _KEY_DFA: self.dfa_.to_dict(str),
                        _KEY_CONCEPT_MAP: self.concept_map_,
                        _KEY_CONCEPT_TYPE_URI: _store_uri_ref(
                            self.concept_type_uri),
                        _KEY_THESAURUS_TYPE_URI: _store_uri_ref(
                            self.sub_thesaurus_type_uri),
                        _KEY_THESAURUS_RELATION_TYPE_URI: _store_uri_ref(
                            self.thesaurus_relation_type_uri),
                        _KEY_THESAURUS_RELATION_IS_SPECIALISATION: (
                                self.thesaurus_relation_is_specialisation),
                        _KEY_REMOVE_DEPRECATED: self.remove_deprecated,
                        _KEY_LANGS: list(self.langs),
                        _KEY_HANDLE_TITLE_CASE: self.handle_title_case,
                        _KEY_EXTRACT_UPPER_CASE_FROM_BRACES: (
                            self.extract_upper_case_from_braces),
                        _KEY_EXTRACT_ANY_CASE_FROM_BRACES: (
                            self.extract_any_case_from_braces),
                        _KEY_EXPAND_AMPERSAND_WITH_SPACES: (
                            self.expand_ampersand_with_spaces),
                        _KEY_EXPAND_ABBREVIATION_WITH_PUNCTUATION: (
                            self.expand_abbreviation_with_punctuation),
                        _KEY_SIMPLE_ENGLISH_PLURAL_RULES: (
                            self.simple_english_plural_rules),
                        },
                        ensure_ascii=False
                    ).encode('utf-8')
                )
            with zfile.open(_NAME_PIPELINE_FILE, 'w') as fp:
                # No good way to serialize sk-learn classifier,
                # apart from insecure pickling
                pkl.dump(self.pipeline_, fp)
            with zfile.open(_NAME_GRAPH_FILE, 'w') as fp:
                fp.write(self.graph.serialize(encoding='utf-8'))

    @staticmethod
    def load(path):
        with ZipFile(path, 'r') as zfile:
            with zfile.open(_NAME_PREDICTOR_FILE, 'r') as fp:
                conf = loads(fp.read().decode('utf-8'))
            with zfile.open(_NAME_GRAPH_FILE, 'r') as fp:
                graph = Graph()
                graph.parse(data=fp.read().decode('utf-8'))
            with zfile.open(_NAME_PIPELINE_FILE, 'r') as fp:
                pipeline = pkl.load(fp)
        pred = StwfsapyPredictor(
            graph=graph,
            concept_type_uri=_load_uri_ref(
                conf[_KEY_CONCEPT_TYPE_URI]),
            sub_thesaurus_type_uri=_load_uri_ref(
                conf[_KEY_THESAURUS_TYPE_URI]),
            thesaurus_relation_type_uri=_load_uri_ref(
                conf[_KEY_THESAURUS_RELATION_TYPE_URI]),
            thesaurus_relation_is_specialisation=(
                conf[_KEY_THESAURUS_RELATION_IS_SPECIALISATION]),
            remove_deprecated=conf[_KEY_REMOVE_DEPRECATED],
            langs=frozenset(conf[_KEY_LANGS]),
            handle_title_case=conf[_KEY_HANDLE_TITLE_CASE],
            extract_upper_case_from_braces=conf[
                _KEY_EXTRACT_UPPER_CASE_FROM_BRACES],
            extract_any_case_from_braces=conf[
                _KEY_EXTRACT_ANY_CASE_FROM_BRACES],
            expand_ampersand_with_spaces=conf[
                _KEY_EXPAND_AMPERSAND_WITH_SPACES],
            expand_abbreviation_with_punctuation=conf[
                _KEY_EXPAND_ABBREVIATION_WITH_PUNCTUATION],
            simple_english_plural_rules=conf[
                _KEY_SIMPLE_ENGLISH_PLURAL_RULES]
        )
        pred.dfa_ = dfa.Dfa.from_dict(conf[_KEY_DFA], str)
        pred.pipeline_ = pipeline
        pred.concept_map_ = conf[_KEY_CONCEPT_MAP]
        return pred


def _store_uri_ref(ref: URIRef) -> str:
    return ref.toPython()


def _load_uri_ref(uri: str) -> URIRef:
    return URIRef(uri)
