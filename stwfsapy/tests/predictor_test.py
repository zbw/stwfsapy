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

from stwfsapy import predictor as p
import stwfsapy.thesaurus as t
from stwfsapy.automata.dfa import Dfa
import stwfsapy.tests.common as c
import pytest
from scipy.sparse import csr_matrix

_doc_counts = [2, 4, 3]
_concepts = list(range(9, 18))
_proto_preds = list(range(2, 11))
_predictions = [i/10 for i in _proto_preds]
_classifications = [i % 2 for i in _proto_preds]
_concept_map = dict(zip(reversed(range(23)), range(23)))
_collection_result = [
    ([9, 10], [0.2, 0.3]),
    ([11, 12, 13, 14], [0.4, 0.5, 0.6, 0.7]),
    ([15, 16, 17], [0.8, 0.9, 1.0])
]


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
        # subtract 2 for spaces in search
        for i in range(len(text)-2):
            yield (i*2+9,)
    mocker.patch.object(dfa, "search", mock_search)
    return dfa


@pytest.fixture
def mocked_predictor(mocker):
    predictor = p.StwfsapyPredictor(None, None, None)
    predictor.concept_map_ = _concept_map
    predictor.match_and_extend = mocker.Mock(
        return_value=(_concepts, _doc_counts))
    predictor.pipeline_ = mocker.MagicMock()
    predictor.pipeline_.predict_proba = mocker.Mock(return_value=_predictions)
    predictor.pipeline_.predict = mocker.Mock(return_value=_classifications)
    return predictor


def test_result_collection():
    res = p.StwfsapyPredictor._collect_prediction_results(
        _predictions,
        _concepts,
        _doc_counts
    )
    assert res == _collection_result


def test_sparse_matrix_creation():
    predictor = p.StwfsapyPredictor(None, None, None)
    predictor.concept_map_ = _concept_map
    res = predictor._create_sparse_matrix(
        _predictions,
        _concepts,
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
            _predictions[slice_start:slice_start+count]))


def test_match_and_extend_with_truth(patched_dfa):
    predictor = p.StwfsapyPredictor(None, None, None)
    predictor.dfa_ = patched_dfa
    concepts, ys = predictor.match_and_extend(
        ["a", "bbb", "xx"],
        [[], [11, 14], [9]]
    )
    assert concepts == [9, 9, 11, 13, 9, 11]
    assert ys == [0, 0, 1, 0, 1, 0]


def test_match_and_extend_without_truth(patched_dfa):
    predictor = p.StwfsapyPredictor(None, None, None)
    predictor.dfa_ = patched_dfa
    concepts, counts = predictor.match_and_extend(["a", "bbb", "xx"])
    assert concepts == [9, 9, 11, 13, 9, 11]
    assert counts == [1, 3, 2]


def test_init_and_fit(full_graph, mocker):
    predictor = p.StwfsapyPredictor(
        full_graph,
        c.test_type_concept,
        c.test_type_thesaurus)
    spy_deprecated = mocker.spy(t, "extract_deprecated")
    predictor._init()
    spy_deprecated.assert_called_once_with(full_graph)
    spy_fit = mocker.spy(predictor.pipeline_, "fit")
    train_texts = [
        "concept-0_0",
        "nothing",
        "concept",
        "has concept-100_00 in the middle",
        "concept-10_0 and concept-01_00",
        ]
    train_labels = [
        [c.test_concept_ref_0_0],
        [c.test_concept_ref_01_0],
        [],
        [c.test_concept_ref_01_00],
        [c.test_concept_ref_10_0, c.test_concept_ref_01_00],
        ]
    predictor._fit_after_init(train_texts, y=train_labels)
    spy_fit.assert_called_once_with(
        [
            c.test_concept_ref_0_0,
            c.test_concept_ref_100_00,
            c.test_concept_ref_10_0,
            c.test_concept_ref_01_00,
            ],
        [1, 0, 1, 1]
    )


def test_predict(mocked_predictor):
    res = mocked_predictor.predict([])
    assert (
        res.toarray() == make_test_result_matrix(_classifications).toarray()
        ).all()
    mocked_predictor.match_and_extend.assert_called_once_with(
        []
    )
    mocked_predictor.pipeline_.predict.assert_called_once_with(
        _concepts
    )


def test_predict_proba(mocked_predictor):
    # TODO check calls
    res = mocked_predictor.predict_proba([])
    assert (
        res.toarray() == make_test_result_matrix(_predictions).toarray()).all()
    mocked_predictor.match_and_extend.assert_called_once_with(
        []
    )
    mocked_predictor.pipeline_.predict_proba.assert_called_once_with(
        _concepts
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
        _concepts
    )


def test_fit(mocker):
    predictor = p.StwfsapyPredictor(None, None, None)
    predictor._init = mocker.Mock()
    predictor._fit_after_init = mocker.Mock()
    X = [list(range(i)) for i in range(13)]
    y = [i % 2 for i in range(13)]
    predictor.fit(X, y)
    predictor._init.assert_called_once()
    predictor._fit_after_init.assert_called_once_with(X, y=y)
