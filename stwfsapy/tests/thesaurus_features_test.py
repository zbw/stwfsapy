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


from numpy import array
from rdflib.namespace import SKOS
from stwfsapy import thesaurus as t
from stwfsapy import thesaurus_features as tf
from stwfsapy.tests.thesaurus import common as tc
from stwfsapy.tests import common as c
from scipy.sparse import coo_matrix, csr_matrix
from sklearn.exceptions import NotFittedError
import pytest


def test_collect_po_from_tuples():
    tuples = [
        (tc.concept_ref_insurance, tc.concept_ref_it),
        (tc.concept_ref_it, tc.thsys_ref_it),
        (tc.concept_ref_insurance, tc.thsys_ref_insurance)
    ]
    po = tf._collect_po_from_tuples(tuples)
    assert po == {
        tc.concept_ref_insurance: {tc.concept_ref_it, tc.thsys_ref_insurance},
        tc.concept_ref_it: {tc.thsys_ref_it}
    }


def test_unfitted_raises():
    feat = tf.ThesaurusFeatureTransformation(None, None, None, None)
    with pytest.raises(NotFittedError):
        feat.transform([])


def test_transform():
    trans = tf.ThesaurusFeatureTransformation(None, None, None, None)
    trans.mapping_ = {
        'a': coo_matrix([[1]]), 'b': coo_matrix([[2]]), 'c': coo_matrix([[3]])}
    res = trans.transform(['c', 'c', 'a'])
    assert (res.toarray() == array([[3], [3], [1]])).all()


def test_fit(full_graph):
    concepts = set(t.extract_by_type_uri(
        full_graph,
        c.test_type_concept))
    thesauri = set(t.extract_by_type_uri(
        full_graph,
        c.test_type_thesaurus))
    trans = tf.ThesaurusFeatureTransformation(
        full_graph,
        concepts,
        thesauri,
        SKOS.broader)
    trans.fit()
    mapping = trans.mapping_
    assert len(mapping) == len(c.test_concepts)
    for x in mapping.values():
        assert x.shape[1] == 6
    # Can not test positions because retrieval from graph is not deterministic.
    # Therefore, test non zero entries only.
    assert mapping[c.test_concept_uri_0_0].getnnz() == 1
    assert mapping[c.test_concept_uri_01_0].getnnz() == 2
    assert mapping[c.test_concept_uri_01_00].getnnz() == 2
    assert mapping[c.test_concept_uri_10_0].getnnz() == 2
    assert mapping[c.test_concept_uri_10_1].getnnz() == 2
    assert mapping[c.test_concept_uri_100_0].getnnz() == 3
    assert mapping[c.test_concept_uri_100_00].getnnz() == 3
    assert mapping[c.test_concept_uri_100_01].getnnz() == 3
    assert mapping[c.test_concept_uri_100_02].getnnz() == 3


def test_transform_unknown():
    trans = tf.ThesaurusFeatureTransformation(
        None,
        None,
        None,
        None,)

    feature_dim = 12
    trans.feature_dim_ = feature_dim
    known = csr_matrix(([1], ([0], [4])), shape=(1, feature_dim))
    trans.mapping_ = {'key': known}
    random_results = trans.transform([
        'some random stuff edsfysdfhjsedf',
        'key'])
    assert random_results.shape == (2, feature_dim)
    assert random_results.getrow(0).getnnz() == 0
    assert random_results.getrow(1).getnnz() == 1


def test_empty_relation(full_graph):
    trans = tf.ThesaurusFeatureTransformation(
        full_graph,
        set(t.extract_by_type_uri(full_graph, c.test_type_concept)),
        set(),
        "",
    )
    trans.fit([], [])
    features = trans.transform(['empty'])
    assert features.shape == (1, 1)
    assert features.getnnz() == 0
