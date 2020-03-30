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
def graph_deprectated_true():
    g = Graph()
    g.add((c.concept_ref_printed, OWL.deprecated, Literal(True)))
    return g


@pytest.fixture
def graph_deprectated_false():
    g = Graph()
    g.add((c.concept_ref_printed, OWL.deprecated, Literal(False)))
    return g


def test_filter_missing_deprecation(tuples, empty_graph):
    filtered = list(t._filter_deprecated(tuples, empty_graph))
    for expected, actual in zip(tuples, filtered):
        assert expected == actual


def test_filter_false_deprecation(tuples, graph_deprectated_false):
    filtered = list(t._filter_deprecated(tuples, graph_deprectated_false))
    for expected, actual in zip(tuples, filtered):
        assert expected == actual


def test_filter_true_deprecation(tuples, graph_deprectated_true):
    filtered = list(t._filter_deprecated(tuples, graph_deprectated_true))
    for f in filtered:
        assert f in tuples
    for tpl in tuples:
        if tpl not in filtered:
            assert graph_deprectated_true.value(tpl[0], OWL.deprecated)
