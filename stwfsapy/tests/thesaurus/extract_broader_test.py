from rdflib import graph
from rdflib.namespace import SKOS

from stwfsapy import thesaurus as t


def test_extract_broader(mocker):
    g = graph.Graph()
    spy = mocker.spy(g, "subject_objects")
    t.extract_broader(g)
    spy.assert_called_once_with(SKOS.broader)
