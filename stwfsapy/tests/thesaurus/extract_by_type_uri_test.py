from rdflib import graph
from rdflib.term import URIRef
from rdflib.namespace import OWL
from stwfsapy import thesaurus as t


def test_extract_by_type_uri(mocker):
    g = graph.Graph()
    spy = mocker.spy(graph.Graph, "__getitem__")
    ref = URIRef("http://www.some.org/type")
    t.extract_by_type_uri(g, ref)
    spy.assert_called_once_with(g, slice(None, OWL.type, ref))
