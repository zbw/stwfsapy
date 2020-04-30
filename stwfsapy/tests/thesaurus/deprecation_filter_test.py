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


import pytest
from rdflib import Graph
from rdflib.namespace import OWL
from rdflib.term import Literal
from stwfsapy import thesaurus as t
import stwfsapy.tests.thesaurus.common as c


@pytest.fixture
def empty_graph():
    return Graph()


@pytest.fixture
def graph_deprecated_true():
    g = Graph()
    g.add((c.concept_ref_printed, OWL.deprecated, Literal(True)))
    return g


@pytest.fixture
def graph_deprecated_false():
    g = Graph()
    g.add((c.concept_ref_printed, OWL.deprecated, Literal(False)))
    return g


def test_filter_missing_deprecation(tuples, empty_graph):
    filtered = list(t._filter_not_deprecated(tuples, empty_graph))
    assert len(filtered) == len(tuples)
    for expected, actual in zip(tuples, filtered):
        assert expected == actual


def test_filter_false_deprecation(tuples, graph_deprecated_false):
    filtered = list(t._filter_not_deprecated(tuples, graph_deprecated_false))
    assert len(filtered) == len(tuples)
    for expected, actual in zip(tuples, filtered):
        assert expected == actual


def test_filter_true_deprecation(tuples, graph_deprecated_true):
    filtered = list(t._filter_not_deprecated(tuples, graph_deprecated_true))
    for f in filtered:
        assert f in tuples
    for tpl in tuples:
        if tpl not in filtered:
            assert graph_deprecated_true.value(tpl[0], OWL.deprecated)
