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

from stwfsapy.text_features import mk_text_features
from scipy.sparse import lil_matrix
from stwfsapy import predictor as p
import stwfsapy.thesaurus as t
from stwfsapy.automata.dfa import Dfa
import stwfsapy.tests.common as c
from stwfsapy.automata.construction import ConstructionState
import pytest
from scipy.sparse import csr_matrix
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.compose import ColumnTransformer
from stwfsapy import case_handlers as handlers
from unittest.mock import call
from rdflib import Graph
from rdflib.namespace import SKOS
from rdflib.term import Literal

_doc_counts = [2, 4, 3]
_concepts = list(range(9, 18))
_concepts_with_text = [(c, str(c)) for c in _concepts]
_proto_preds = list(range(2, 11))
_predictions = np.array([[0, i/10] for i in _proto_preds])
_classifications = np.array([i % 2 for i in _proto_preds])
_concept_map = dict(zip(reversed(range(23)), range(23)))
_collection_result = [
    ([9, 10], [0.2, 0.3]),
    ([11, 12, 13, 14], [0.4, 0.5, 0.6, 0.7]),
    ([15, 16, 17], [0.8, 0.9, 1.0])
]
train_texts = [
    "concept-0_0",
    "nothing",
    "concept",
    "has Concept-100_00 in the middle",
    "concept-10_0 and concept-01_00 and concept-10_0",
    ]
train_labels = [
    [c.test_concept_ref_0_0],
    [c.test_concept_ref_01_0],
    [],
    [c.test_concept_ref_01_00],
    [c.test_concept_ref_10_0, c.test_concept_ref_01_00],
    ]
expected_matches = [
    ("9", [0], 1), ("9", [0], 0),
    ("11", [0, 1], 0), ("13", [0, 1, 2], 1),
    ("9", [0], 0), ("11", [0, 1], 1)]


def make_test_result_matrix(values):
    return csr_matrix((
        values,
        (
            [
                i
                for i, count
                in enumerate(_doc_counts)
                for _
                in range(count)],
            [22-c for c in _concepts])),
            shape=(3, 23))


@pytest.fixture
def patched_dfa(mocker):
    dfa = Dfa()

    def mock_search(text):
        for i in range(len(text)):
            for j in range(i+1):
                yield (str(i*2+9), text, j)

    mocker.patch.object(dfa, "search", mock_search)
    return dfa


@pytest.fixture
def mocked_predictor(mocker, mock_vectorizer):
    predictor = p.StwfsapyPredictor(None, None, None, None)
    predictor.concept_map_ = _concept_map
    predictor.match_and_extend = mocker.Mock(
        return_value=(_concepts_with_text, _doc_counts))
    predictor.text_vectorizer_ = mock_vectorizer
    predictor.text_features_ = mk_text_features()
    predictor.pipeline_ = mocker.MagicMock()
    predictor.pipeline_.predict_proba = mocker.Mock(return_value=_predictions)
    predictor.pipeline_.predict = mocker.Mock(return_value=_classifications)
    return predictor


@pytest.fixture
def no_match_predictor(mocker):
    predictor = p.StwfsapyPredictor(None, None, None, None)
    predictor.concept_map_ = _concept_map
    predictor.match_and_extend = mocker.Mock(
        return_value=([], [0, 0, 0]))
    return predictor


def mock_vec_transform(X):
    ret = lil_matrix((len(X), 5000))
    for idx, x in enumerate(X):
        ret[idx] = len(x)
    return ret


@pytest.fixture
def mock_vectorizer(mocker):
    mock_vec = mocker.MagicMock()
    mock_vec.transform = mock_vec_transform
    return mock_vec


@pytest.fixture
def case_graph():
    g = Graph()
    g.add((
        c.test_concept_ref_0_0,
        SKOS.prefLabel,
        Literal("Three word label")))
    return g


def test_result_collection():
    res = p.StwfsapyPredictor._collect_prediction_results(
        _predictions[:, 1],
        [c[0] for c in _concepts_with_text],
        _doc_counts
    )
    assert [(r[0], list(r[1])) for r in res] == _collection_result


def test_sparse_matrix_creation():
    predictor = p.StwfsapyPredictor(None, None, None, None)
    predictor.concept_map_ = _concept_map
    res = predictor._create_sparse_matrix(
        _predictions[:, 1],
        [c[0] for c in _concepts_with_text],
        _doc_counts
    )
    assert res.shape[0] == len(_doc_counts)
    assert res.shape[1] == 23
    for i, count in enumerate(_doc_counts):
        row = res.getrow(i)
        slice_start = sum(_doc_counts[:i])
        assert row.getnnz() == count
        # reverse slices because of mapping.
        assert list(row.nonzero()[1]) == list(reversed([
            22-i for i in _concepts[slice_start: slice_start+count]]))
        assert list(row.data) == list(reversed(
            _predictions[slice_start:slice_start+count, 1]))


def test_match_and_extend_with_truth_with_vec(patched_dfa, mock_vectorizer):
    predictor = p.StwfsapyPredictor(None, None, None, None, use_txt_vec=True)
    predictor.dfa_ = patched_dfa
    predictor.text_features_ = mk_text_features().fit([])
    predictor.text_vectorizer_ = mock_vectorizer
    in_txts = ["a", "bbb", "xx"]
    matches, ys = predictor.match_and_extend(
        in_txts,
        [[], [11, 14], [9]]
    )
    txt_indices = [
        idx
        for idx, txt
        in enumerate(in_txts)
        for _ in range(len(txt))
    ]
    for txt_idx, match, expected in zip(
            txt_indices,
            matches,
            expected_matches):
        check_fit_arg(
            predictor.text_vectorizer_,
            predictor.text_features_,
            in_txts[txt_idx],
            match,
            expected
        )
    assert ys == [0, 0, 1, 0, 1, 0]


def test_match_and_extend_without_truth_with_vec(patched_dfa, mock_vectorizer):
    predictor = p.StwfsapyPredictor(None, None, None, None, use_txt_vec=True)
    predictor.dfa_ = patched_dfa
    predictor.text_features_ = mk_text_features().fit([])
    predictor.text_vectorizer_ = mock_vectorizer
    in_txts = ["a", "bbb", "xx"]
    matches, counts = predictor.match_and_extend(in_txts)
    txt_indices = [
        idx
        for idx, txt
        in enumerate(in_txts)
        for _ in range(len(txt))
    ]
    for txt_idx, match, expected in zip(
            txt_indices,
            matches,
            expected_matches):
        check_fit_arg(
            predictor.text_vectorizer_,
            predictor.text_features_,
            in_txts[txt_idx],
            match,
            expected
        )
    assert counts == [1, 3, 2]


def test_init_and_fit_with_vec(full_graph, mocker):
    predictor = p.StwfsapyPredictor(
        full_graph,
        c.test_type_concept,
        c.test_type_thesaurus,
        SKOS.broader,
        use_txt_vec=True)
    spy_deprecated = mocker.spy(t, "extract_deprecated")
    spy_case = mocker.spy(handlers, 'title_case_handler')
    predictor._init()
    assert predictor.text_vectorizer_ is not None
    spy_deprecated.assert_called_once_with(full_graph)
    assert len(spy_case.mock_calls) == len(c.test_labels)
    for _, label in c.test_labels:
        assert call(label.toPython()) in spy_case.mock_calls
    assert isinstance(
        predictor.pipeline_.named_steps['Classifier'],
        DecisionTreeClassifier)
    combined = predictor.pipeline_.named_steps['Combined Features']
    assert isinstance(
        combined,
        ColumnTransformer)
    assert len(combined.transformers) == 5
    assert combined.transformers[0][0] == 'Thesaurus Features'
    assert combined.transformers[1][0] == 'Text Features'
    assert combined.transformers[2][0] == 'Position Features'
    assert combined.transformers[3][0] == 'Frequency Features'
    assert combined.transformers[4][0] == 'Text Vector'
    assert combined.transformers[0][1].thesaurus_relation == SKOS.broader
    spy_fit_pipeline = mocker.spy(predictor.pipeline_, "fit")
    spy_fit_vec = mocker.spy(predictor.text_vectorizer_, "fit")
    predictor._fit_after_init(train_texts, y=train_labels)
    spy_fit_pipeline.assert_called_once()

    pipe_fit_arg_list = spy_fit_pipeline.call_args_list[0]
    assert len(pipe_fit_arg_list) == 2
    pipe_fit_args = pipe_fit_arg_list[0]
    assert pipe_fit_arg_list[1].get('y') == [1, 0, 1, 1]
    expected_features = [
            (c.test_concept_uri_0_0, [0], 1),
            (
                c.test_concept_uri_100_00,
                [4],
                1),
            (c.test_concept_uri_10_0, [0, 35], 0),
            (c.test_concept_uri_01_00, [17], 1),
            ]
    assert len(expected_features) == len(pipe_fit_args[0])
    txt_indices = [0, 3, 4, 4]
    for txt_idx, actual, expected in zip(
            txt_indices,
            pipe_fit_args[0],
            expected_features):
        check_fit_arg(
            predictor.text_vectorizer_,
            predictor.text_features_,
            train_texts[txt_idx],
            actual,
            expected)

    spy_fit_vec.assert_called_once_with(
        train_texts
    )


def test_match_and_extend_with_truth_without_vec(patched_dfa):
    predictor = p.StwfsapyPredictor(None, None, None, None, use_txt_vec=False)
    predictor.dfa_ = patched_dfa
    predictor.text_features_ = mk_text_features().fit([])
    in_txts = ["a", "bbb", "xx"]
    matches, ys = predictor.match_and_extend(
        in_txts,
        [[], [11, 14], [9]]
    )
    txt_indices = [
        idx
        for idx, txt
        in enumerate(in_txts)
        for _ in range(len(txt))
    ]
    for txt_idx, match, expected in zip(
            txt_indices,
            matches,
            expected_matches):
        check_fit_arg(
            None,
            predictor.text_features_,
            in_txts[txt_idx],
            match,
            expected
        )
    assert ys == [0, 0, 1, 0, 1, 0]


def test_match_and_extend_without_truth_without_vec(patched_dfa):
    predictor = p.StwfsapyPredictor(None, None, None, None, use_txt_vec=False)
    predictor.dfa_ = patched_dfa
    predictor.text_features_ = mk_text_features().fit([])
    in_txts = ["a", "bbb", "xx"]
    matches, counts = predictor.match_and_extend(in_txts)
    txt_indices = [
        idx
        for idx, txt
        in enumerate(in_txts)
        for _ in range(len(txt))
    ]
    for txt_idx, match, expected in zip(
            txt_indices,
            matches,
            expected_matches):
        check_fit_arg(
            None,
            predictor.text_features_,
            in_txts[txt_idx],
            match,
            expected
        )
    assert counts == [1, 3, 2]


def test_init_and_fit_without_vec(full_graph, mocker):
    predictor = p.StwfsapyPredictor(
        full_graph,
        c.test_type_concept,
        c.test_type_thesaurus,
        SKOS.broader,
        use_txt_vec=False)
    spy_deprecated = mocker.spy(t, "extract_deprecated")
    spy_case = mocker.spy(handlers, 'title_case_handler')
    predictor._init()
    assert predictor.text_vectorizer_ is None
    spy_deprecated.assert_called_once_with(full_graph)
    assert len(spy_case.mock_calls) == len(c.test_labels)
    for _, label in c.test_labels:
        assert call(label.toPython()) in spy_case.mock_calls
    assert isinstance(
        predictor.pipeline_.named_steps['Classifier'],
        DecisionTreeClassifier)
    combined = predictor.pipeline_.named_steps['Combined Features']
    assert isinstance(
        combined,
        ColumnTransformer)
    assert len(combined.transformers) == 4
    assert combined.transformers[0][0] == 'Thesaurus Features'
    assert combined.transformers[1][0] == 'Text Features'
    assert combined.transformers[2][0] == 'Position Features'
    assert combined.transformers[3][0] == 'Frequency Features'
    assert combined.transformers[0][1].thesaurus_relation == SKOS.broader
    spy_fit_pipeline = mocker.spy(predictor.pipeline_, "fit")
    predictor._fit_after_init(train_texts, y=train_labels)
    spy_fit_pipeline.assert_called_once()

    pipe_fit_arg_list = spy_fit_pipeline.call_args_list[0]
    assert len(pipe_fit_arg_list) == 2
    pipe_fit_args = pipe_fit_arg_list[0]
    assert pipe_fit_arg_list[1].get('y') == [1, 0, 1, 1]
    expected_features = [
            (c.test_concept_uri_0_0, [0], 1),
            (
                c.test_concept_uri_100_00,
                [4],
                1),
            (c.test_concept_uri_10_0, [0, 35], 0),
            (c.test_concept_uri_01_00, [17], 1),
            ]
    assert len(expected_features) == len(pipe_fit_args[0])
    txt_indices = [0, 3, 4, 4]
    for txt_idx, actual, expected in zip(
            txt_indices,
            pipe_fit_args[0],
            expected_features):
        check_fit_arg(
            None,
            predictor.text_features_,
            train_texts[txt_idx],
            actual,
            expected)


def check_fit_arg(vec_fun, text_feature_fun, txt, actual, expected):
    assert actual[0] == expected[0]
    assert (actual[1] == text_feature_fun.transform([txt])[0]).all()
    if vec_fun:
        assert (actual[2].toarray() ==
                vec_fun.transform([txt]).toarray()).all()
    else:
        assert actual[2] == 0
    assert actual[3] == len(txt)
    assert actual[4] == expected[1]
    assert actual[5] == expected[-1]


def test_predict(mocked_predictor):
    res = mocked_predictor.predict([])
    assert (
        res.toarray() == make_test_result_matrix(_classifications).toarray()
        ).all()
    mocked_predictor.match_and_extend.assert_called_once_with(
        []
    )
    mocked_predictor.pipeline_.predict.assert_called_once_with(
        _concepts_with_text
    )


def test_predict_proba(mocked_predictor):
    res = mocked_predictor.predict_proba([])
    assert (
        res.toarray() == make_test_result_matrix(
            _predictions[:, 1]).toarray()).all()
    mocked_predictor.match_and_extend.assert_called_once_with(
        []
    )
    mocked_predictor.pipeline_.predict_proba.assert_called_once_with(
        _concepts_with_text
    )


def test_suggest(mocked_predictor):
    res = mocked_predictor.suggest_proba([])
    assert res == [
        [(9, 0.2), (10, 0.3)],
        [(11, 0.4), (12, 0.5), (13, 0.6), (14, 0.7)],
        [(15, 0.8), (16, 0.9), (17, 1.0)],
        ]
    mocked_predictor.match_and_extend.assert_called_once_with(
        []
    )
    mocked_predictor.pipeline_.predict_proba.assert_called_once_with(
        _concepts_with_text
    )


def test_predict_no_match(no_match_predictor):
    res = no_match_predictor.predict([])
    assert res.getnnz() == 0
    assert res.shape == (3, len(_concept_map))


def test_predict_proba_no_match(no_match_predictor):
    res = no_match_predictor.predict_proba([])
    assert res.getnnz() == 0
    assert res.shape == (3, len(_concept_map))


def test_suggest_no_match(no_match_predictor):
    res = no_match_predictor.suggest_proba([])
    assert res == [[], [], []]


def test_fit(mocker):
    predictor = p.StwfsapyPredictor(None, None, None, None)
    predictor._init = mocker.Mock()
    predictor._fit_after_init = mocker.Mock()
    X = [list(range(i)) for i in range(13)]
    y = [i % 2 for i in range(13)]
    predictor.fit(X, y)
    predictor._init.assert_called_once()
    predictor._fit_after_init.assert_called_once_with(X, y=y)


def test_set_sentence_case(case_graph):
    predictor = p.StwfsapyPredictor(
        case_graph,
        c.test_type_concept,
        c.test_type_thesaurus,
        SKOS.broader,
        handle_title_case=False)
    predictor._init()
    assert 1 == len(list(predictor.dfa_.search("three word label")))
    assert 0 == len(list(predictor.dfa_.search("Three Word label")))


def test_set_title_case(case_graph):
    predictor = p.StwfsapyPredictor(
        case_graph,
        c.test_type_concept,
        c.test_type_thesaurus,
        SKOS.broader,
        handle_title_case=True)
    predictor._init()
    assert 1 == len(list(predictor.dfa_.search("three word label")))
    assert 1 == len(list(predictor.dfa_.search("Three Word label")))


def test_no_english_plural(case_graph):
    predictor = p.StwfsapyPredictor(
        case_graph,
        c.test_type_concept,
        c.test_type_thesaurus,
        SKOS.broader,
        simple_english_plural_rules=False,
    )
    predictor._init()
    assert 0 == len(list(predictor.dfa_.search('three word labels')))
    assert 1 == len(list(predictor.dfa_.search('three word label')))


def test_english_plural(case_graph):
    predictor = p.StwfsapyPredictor(
        case_graph,
        c.test_type_concept,
        c.test_type_thesaurus,
        SKOS.broader,
        simple_english_plural_rules=True,
    )
    predictor._init()
    assert 1 == len(list(predictor.dfa_.search('three word labels')))
    assert 1 == len(list(predictor.dfa_.search('three word labels')))


def test_english_plural_with_case(case_graph):
    predictor = p.StwfsapyPredictor(
        case_graph,
        c.test_type_concept,
        c.test_type_thesaurus,
        SKOS.broader,
        simple_english_plural_rules=True,
        handle_title_case=True
    )
    predictor._init()
    assert 1 == len(list(predictor.dfa_.search('three word labels')))
    assert 1 == len(list(predictor.dfa_.search('three word labels')))
    assert 1 == len(list(predictor.dfa_.search('Three Word Labels')))


def test_expansion(full_graph, mocker):
    stub = mocker.stub(name='expansion_stub')

    def mock_expander(**kwargs):
        return [stub]

    mocker.patch(
        'stwfsapy.expansion.collect_expansion_functions',
        mock_expander)
    predictor = p.StwfsapyPredictor(
        full_graph,
        c.test_type_concept,
        c.test_type_thesaurus,
        SKOS.broader,
        True,
        extract_upper_case_from_braces=False,
        extract_any_case_from_braces=True,
        expand_ampersand_with_spaces=False,
        expand_abbreviation_with_punctuation=False,
        simple_english_plural_rules=True)
    predictor._init()
    for _, label in c.test_labels:
        label_text = label.toPython()
        assert call(label_text) in stub.mock_calls


def test_mark_doc_end():
    predictor = p.StwfsapyPredictor(None, None, None, None)
    matches = [('a', None, None, [0], 5, 0), ('b', None, None, [2, 5], 7, 0)]
    predictor._mark_last_concept_in_doc(matches)
    assert matches == [
        ('a', None, None, [0], 5, 0),
        ('b', None, None, [2, 5], 7, 1)]


def test_mark_doc_end_empty():
    predictor = p.StwfsapyPredictor(None, None, None, None)
    lst = []
    predictor._mark_last_concept_in_doc(lst)
    assert lst == []


def test_uriref_str_inversion():
    ref = c.test_type_concept
    assert ref == p._load_uri_ref(p._store_uri_ref(ref))


def test_serialization_inversion_without_vec(tmpdir, full_graph):
    predictor = p.StwfsapyPredictor(
        full_graph,
        c.test_type_concept,
        c.test_type_thesaurus,
        SKOS.broader,
        use_txt_vec=False
    )
    predictor.fit(train_texts, train_labels)
    pth = tmpdir.mkdir("tmp").join("model.zip")
    predictor.store(pth.strpath)
    loaded = p.StwfsapyPredictor.load(pth.strpath)
    assert loaded.input == predictor.input
    assert not loaded.use_txt_vec
    assert loaded.extract_any_case_from_braces == (
        predictor.extract_any_case_from_braces)
    assert loaded.extract_upper_case_from_braces == (
        predictor.extract_upper_case_from_braces)
    assert loaded.expand_ampersand_with_spaces == (
        predictor.expand_ampersand_with_spaces)
    assert loaded.expand_abbreviation_with_punctuation == (
        predictor.expand_abbreviation_with_punctuation)
    assert loaded.simple_english_plural_rules == (
        predictor.simple_english_plural_rules)
    assert loaded.concept_type_uri == predictor.concept_type_uri
    assert loaded.sub_thesaurus_type_uri == predictor.sub_thesaurus_type_uri
    assert loaded.thesaurus_relation_type_uri == (
        predictor.thesaurus_relation_type_uri)
    assert loaded.thesaurus_relation_is_specialisation == (
        predictor.thesaurus_relation_is_specialisation)
    assert loaded.concept_map_ == predictor.concept_map_
    assert loaded.dfa_ == predictor.dfa_
    assert len(loaded.graph) == len(predictor.graph)
    assert loaded.concept_map_ == predictor.concept_map_
    assert loaded.dfa_ == predictor.dfa_
    assert len(loaded.graph) == len(predictor.graph)
    assert loaded.pipeline_[0].transformers[0][1].mapping_ == (
        predictor.pipeline_[0].transformers[0][1].mapping_)
    assert loaded.text_vectorizer_ is None
    loaded_txt_feat_names = [
        name
        for name, _
        in loaded.text_features_.transformer_list
    ]
    pred_txt_feat_names = [
        name
        for name, _
        in predictor.text_features_.transformer_list
    ]
    assert loaded_txt_feat_names == pred_txt_feat_names
    for triple in loaded.graph:
        assert triple in predictor.graph


def test_serialization_inversion_with_vec(tmpdir, full_graph):
    predictor = p.StwfsapyPredictor(
        full_graph,
        c.test_type_concept,
        c.test_type_thesaurus,
        SKOS.broader,
        use_txt_vec=True
    )
    predictor.fit(train_texts, train_labels)
    pth = tmpdir.mkdir("tmp").join("model.zip")
    predictor.store(pth.strpath)
    loaded = p.StwfsapyPredictor.load(pth.strpath)
    assert loaded.input == predictor.input
    assert loaded.use_txt_vec
    assert loaded.extract_any_case_from_braces == (
        predictor.extract_any_case_from_braces)
    assert loaded.extract_upper_case_from_braces == (
        predictor.extract_upper_case_from_braces)
    assert loaded.expand_ampersand_with_spaces == (
        predictor.expand_ampersand_with_spaces)
    assert loaded.expand_abbreviation_with_punctuation == (
        predictor.expand_abbreviation_with_punctuation)
    assert loaded.simple_english_plural_rules == (
        predictor.simple_english_plural_rules)
    assert loaded.concept_type_uri == predictor.concept_type_uri
    assert loaded.sub_thesaurus_type_uri == predictor.sub_thesaurus_type_uri
    assert loaded.thesaurus_relation_type_uri == (
        predictor.thesaurus_relation_type_uri)
    assert loaded.thesaurus_relation_is_specialisation == (
        predictor.thesaurus_relation_is_specialisation)
    assert loaded.concept_map_ == predictor.concept_map_
    assert loaded.dfa_ == predictor.dfa_
    assert len(loaded.graph) == len(predictor.graph)
    assert loaded.concept_map_ == predictor.concept_map_
    assert loaded.dfa_ == predictor.dfa_
    assert len(loaded.graph) == len(predictor.graph)
    assert loaded.pipeline_[0].transformers[0][1].mapping_ == (
        predictor.pipeline_[0].transformers[0][1].mapping_)
    assert loaded.text_vectorizer_ is not None
    assert loaded.text_vectorizer_.vocabulary_ == (
        predictor.text_vectorizer_.vocabulary_)
    loaded_txt_feat_names = [
        name
        for name, _
        in loaded.text_features_.transformer_list
    ]
    pred_txt_feat_names = [
        name
        for name, _
        in predictor.text_features_.transformer_list
    ]
    assert loaded_txt_feat_names == pred_txt_feat_names
    for triple in loaded.graph:
        assert triple in predictor.graph


def test_warning(mocker):
    logging_spy = mocker.spy(p, '_logger')
    con_state = ConstructionState(None, '', '')
    con_state.construct = mocker.Mock(side_effect=Exception())
    p._handle_construction(
        con_state,
        'test_concept',
        'invalid_label')
    logging_spy.warning.assert_called_once_with(
        'Could not process label "invalid_label" of concept "test_concept".'
    )
