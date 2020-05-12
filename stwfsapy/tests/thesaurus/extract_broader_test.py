from rdflib import graph
from rdflib.namespace import SKOS

from stwfsapy import thesaurus as t


def test_extract_broader(mocker):
    g = graph.Graph()
    spy = mocker.spy(graph.Graph, "__getitem__")
    t.extract_broader(g)
    spy.assert_called_once_with(g, slice(None, SKOS.broader, None))
