# Copyright 2020-2025 Leibniz Information Centre for Economics
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


from stwfsapy.util.passthrough_transformer import PassthroughTransformer
from stwfsapy.frequency_features import FrequencyFeatures
from stwfsapy.position_features import PositionFeatures
from collections import defaultdict
from typing import Dict, FrozenSet, List, Iterable, \
    Container, Tuple, TypeVar, Union
from scipy.sparse import spmatrix
from numpy import array
from logging import getLogger
from rdflib.term import URIRef
from rdflib import Graph
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix
from stwfsapy import thesaurus as t
from stwfsapy.automata import nfa, construction, conversion, dfa
from stwfsapy.thesaurus_features import ThesaurusFeatureTransformation
from stwfsapy.text_features import mk_text_features
from stwfsapy.util.input_handler import get_input_handler
from stwfsapy import case_handlers
from stwfsapy import expansion
import pickle as pkl
from json import dumps, loads
from zipfile import ZipFile


T = TypeVar('T')
N = TypeVar('N', int, float)
Nl = TypeVar('Nl', List[int], List[float])


_KEY_DFA = 'dfa'
_KEY_CONCEPT_MAP = 'concept_map'
_KEY_CONCEPT_TYPE_URI = 'concept_type_uri'
_KEY_THESAURUS_TYPE_URI = 'thesaurus_type_uri'
_KEY_THESAURUS_RELATION_TYPE_URI = 'thesaurus_relation_type_uri'
_KEY_THESAURUS_RELATION_IS_SPECIALISATION = (
    'thesaurus_relation_is_specialisation')
_KEY_REMOVE_DEPRECATED = 'remove_deprecated'
_KEY_LANGS = 'langs'
_KEY_INPUT = 'input'
_KEY_USE_TXT_VEC = 'use_txt_vec'
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
_NAME_TEXT_FEATURES_FILE = 'text_features.pkl'
_NAME_TEXT_VECTORIZER_FILE = 'text_vectorizer.pkl'

_logger = getLogger('stwfsa')


class StwfsapyPredictor(BaseEstimator, ClassifierMixin):
    """Finds labels of thesaurus concepts in texts
    and assigns them a score."""
    def __init__(
            self,
            graph: Graph,
            concept_type_uri: Union[str, URIRef],
            sub_thesaurus_type_uri: Union[str, URIRef] = "",
            thesaurus_relation_type_uri: Union[str, URIRef] = "",
            thesaurus_relation_is_specialisation: bool = False,
            remove_deprecated: bool = True,
            langs: FrozenSet[str] = frozenset(),
            input: str = 'content',
            use_txt_vec: bool = False,
            handle_title_case: bool = True,
            extract_upper_case_from_braces: bool = True,
            extract_any_case_from_braces: bool = False,
            expand_ampersand_with_spaces: bool = True,
            expand_abbreviation_with_punctuation: bool = True,
            simple_english_plural_rules: bool = False,
            ):
        """Creates the predictor.

        :param graph: The SKOS ontology used to extract the labels.
        :param concept_type_uri:
            The uri of the concept type.
            It is assumed that for every concept c,
            there is a triple (c, RDF.type, concept_type_uri)
            in the graph.
        :param  sub_thesaurus_type_uri: The uri of the concept type.
            It is assumed that for every sub thesaurus t,
            there is a triple (t, RDF.type, sub_thesaurus_type_uri)
            in the graph.
        :param  thesaurus_relation_type_uri:
            Uri of the relation that links concepts to thesauri.
        :param  thesaurus_relation_is_specialisation:
            Indicates whether the thesaurus_relation links thesauri to
            concepts or the other way round.
            E.g., for the relation skos:broader it should be false.
            Conversely it should be true for skos:narrower.
        :param  remove_deprecated:
            When True will discard deprecated subjects.
            Deprecation of a subject has to be indicated by
            a triple (s, OWL.deprecated, Literal(True)) in the graph.
        :param  langs:
            For each language present in the set,
            labels will be extracted from the graph.
            An empy set or None will extract labels regardless of language.
        :param  input:
            What type of input is presented to the fit method:

                * 'content': Input is expected to be an arraylike of string.
                * 'filename': Input is expected to be a list of filenames.
                * 'file': input is expected to be a list of file objects.
        :param  use_txt_vec:
            Whether to use vectorized representations of inputs.
            This can lead to high memory consumption.
        :param  handle_title_case:
            When True, will also match labels in title case.
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
                    "Garbage can is home to grouchy neighbor.".
        :param extract_upper_case_from_braces:
            Removes the explanation in braces from labels.
            I.e., GDP (Gross Domestic Product) will be transformed to GDP.
        :param extract_any_case_from_braces:
            Can extract content of braces in labels.
            I.e., R&D (research and discovery) will be transformed to
            research and discovery.
            In contrast to extract_upper_case_from_braces it will extract
            the part inside the parenthesis and not the part before.
        :param expand_ampersand_with_spaces:
              For labels that contain an ampersand it will also match text
              containing spaces around that symbol.
              I.e., R & D will be matched for label R&D.
        :param expand_abbreviation_with_punctuation:
          For labels containing only uppercase letters it will also
          match text with punctuation added. I.e., G.D.P. for label GDP.
        :param simple_english_plural_rules:
          Can detect simple English plural forms of labels.
        """
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
        self.input = input
        self.use_txt_vec = use_txt_vec
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
            _handle_construction(
                construction.ConstructionState(
                    nfautomat,
                    plural_fun(case_handler(expanded)),
                    str(concept)
                ),
                concept,
                label)
        nfautomat.remove_empty_transitions()
        converter = conversion.NfaToDfaConverter(nfautomat)
        self.dfa_ = converter.start_conversion()
        self.text_features_ = mk_text_features().fit([])
        transformations = [
                    ("Thesaurus Features", thesaurus_features, 0),
                    ('Text Features', PassthroughTransformer(), 1),
                    ('Position Features', PositionFeatures(), [3, 4]),
                    (
                        'Frequency Features',
                        FrequencyFeatures(),
                        [0, 4, 5])
                ]
        if self.use_txt_vec:
            self.text_vectorizer_ = TfidfVectorizer(input=self.input)
            transformations.append(
                ('Text Vector', PassthroughTransformer(), 2),
            )
        else:
            self.text_vectorizer_ = None
        self.pipeline_ = Pipeline([
            ("Combined Features", ColumnTransformer(
                transformations)),
            ("Classifier", DecisionTreeClassifier(
                min_samples_leaf=25,
                max_leaf_nodes=100))
        ])

    def fit(self, X, y=None, **kwargs):
        self._init()
        return self._fit_after_init(X, y=y)

    def _fit_after_init(self, X, y=None):
        if self.use_txt_vec:
            self.text_vectorizer_.fit(X)
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
            [tpl[0] for tpl in match_X],
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
            [tpl[0] for tpl in match_X],
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
            [tpl[0] for tpl in match_X],
            doc_counts
        )

    def _create_sparse_matrix(
            self,
            values: Nl,
            concept_names: List[str],
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
                        self.concept_map_.get(name)
                        for name
                        in concept_names
                    ]
                )),
            shape=(len(doc_counts), len(self.concept_map_))
        )

    @staticmethod
    def _collect_prediction_results(
            values: Nl,
            concept_names: List[T],
            doc_counts: List[int]
            ) -> List[Tuple[List[T], Nl]]:
        ret = []
        start = 0
        for count in doc_counts:
            end = start+count
            ret.append((concept_names[start:end], values[start:end]))
            start = end
        return ret

    def match_and_extend(
            self,
            inputs: Iterable[str],
            truth_refss: Iterable[Container] = None
            ) -> Tuple[List[Tuple[
                str,
                spmatrix,
                array,
                int,
                List[int], int]],
                List[int]]:
        """Retrieves concepts by their labels from text.
        If ground truth values are present,
        it will also return a list of labels for scoring matches.
        If no ground truth values are present, a list
        with the number of matched concepts for each document is returned."""
        concepts = []
        input_handler = get_input_handler(self.input)
        if truth_refss is not None:
            ret_y = []
            for inp, truth_refs in zip(inputs, map(str, truth_refss)):
                text = input_handler(inp)
                if self.use_txt_vec:
                    txt_vec = self.text_vectorizer_.transform([inp])[0]
                else:
                    txt_vec = 0
                txt_feat = self.text_features_.transform([text])[0]
                matched_concepts: Dict[str, List[int]] = defaultdict(list)
                for match in self.dfa_.search(text):
                    concept = match[0]
                    position = match[2]
                    matched_concepts[concept].append(position)
                for concept, positions in matched_concepts.items():
                    concepts.append((
                        concept,
                        txt_feat,
                        txt_vec,
                        len(text),
                        positions,
                        0))
                    ret_y.append(int(concept in truth_refs))
                self._mark_last_concept_in_doc(concepts)
            return concepts, ret_y
        else:
            doc_counts: List[int] = []
            for inp in inputs:
                text = input_handler(inp)
                if self.use_txt_vec:
                    txt_vec = self.text_vectorizer_.transform([inp])[0]
                else:
                    txt_vec = 0
                txt_feat = self.text_features_.transform([text])[0]
                matched_concepts = defaultdict(list)
                for match in self.dfa_.search(text):
                    concept = match[0]
                    position = match[2]
                    matched_concepts[concept].append(position)
                for concept, positions in matched_concepts.items():
                    concepts.append((
                        concept,
                        txt_feat,
                        txt_vec,
                        len(text),
                        positions,
                        0))
                self._mark_last_concept_in_doc(concepts)
                doc_counts.append(len(matched_concepts))
            return concepts, doc_counts

    def _mark_last_concept_in_doc(self, concepts):
        if concepts:
            last = concepts.pop()
            concepts.append((last[0], last[1], last[2], last[3], last[4], 1))

    def store(self, path):
        with ZipFile(path, 'w') as zfile:
            with zfile.open(_NAME_PREDICTOR_FILE, 'w', force_zip64=True) as fp:
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
                        _KEY_INPUT: self.input,
                        _KEY_USE_TXT_VEC: self.use_txt_vec,
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
            with zfile.open(_NAME_PIPELINE_FILE, 'w', force_zip64=True) as fp:
                # No good way to serialize sk-learn classifier,
                # apart from insecure pickling
                pkl.dump(self.pipeline_, fp)
            if self.use_txt_vec:
                with zfile.open(
                        _NAME_TEXT_VECTORIZER_FILE,
                        'w',
                        force_zip64=True) as fp:
                    pkl.dump(self.text_vectorizer_, fp)
            with zfile.open(
                    _NAME_TEXT_FEATURES_FILE,
                    'w',
                    force_zip64=True) as fp:
                pkl.dump(self.text_features_, fp)
            with zfile.open(_NAME_GRAPH_FILE, 'w', force_zip64=True) as fp:
                fp.write(self.graph.serialize(encoding='utf-8'))

    @staticmethod
    def load(path):
        with ZipFile(path, 'r') as zfile:
            with zfile.open(_NAME_PREDICTOR_FILE, 'r') as fp:
                conf = loads(fp.read().decode('utf-8'))
            use_txt_vec = conf[_KEY_USE_TXT_VEC]
            if use_txt_vec:
                with zfile.open(_NAME_TEXT_VECTORIZER_FILE, 'r') as fp:
                    text_vectorizer = pkl.load(fp)
            with zfile.open(_NAME_GRAPH_FILE, 'r') as fp:
                graph = Graph()
                graph.parse(data=fp.read().decode('utf-8'))
            with zfile.open(_NAME_PIPELINE_FILE, 'r') as fp:
                pipeline = pkl.load(fp)
            with zfile.open(_NAME_TEXT_FEATURES_FILE, 'r') as fp:
                text_features = pkl.load(fp)
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
            input=conf[_KEY_INPUT],
            use_txt_vec=use_txt_vec,
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
        pred.text_features_ = text_features
        if use_txt_vec:
            pred.text_vectorizer_ = text_vectorizer
        else:
            pred.text_vectorizer_ = None
        pred.dfa_ = dfa.Dfa.from_dict(conf[_KEY_DFA], str)
        pred.pipeline_ = pipeline
        pred.concept_map_ = conf[_KEY_CONCEPT_MAP]
        return pred


def _store_uri_ref(ref: URIRef) -> str:
    return ref.toPython()


def _load_uri_ref(uri: str) -> URIRef:
    return URIRef(uri)


def _handle_construction(
        con_state: construction.ConstructionState,
        concept: str,
        label: str):
    """Wrapper for construction that logs a warning
    in case of an exception.
    Uses concept and label as arguments for a more detailed message."""
    try:
        con_state.construct()
    except Exception:
        _logger.warning(
            f'Could not process label "{label}" of concept "{concept}".')
