from pytest import fixture
from rdflib.graph import Graph
from rdflib.namespace import RDF, SKOS
from stwfsapy.tests import common as c


@fixture
def full_graph():
    g = Graph()
    for t in c.test_thesauri:
        g.add((t, RDF.type, c.test_type_thesaurus))
    for cncpt in c.test_concepts:
        g.add((cncpt, RDF.type, c.test_type_concept))
    for narrow, broader in c.thsrs_broader:
        g.add((narrow, SKOS.broader, broader))
    for narrow, broader in c.cncpt_broaders:
        g.add((narrow, SKOS.broader, broader))
    for cncpt, label in c.test_labels:
        g.add((cncpt, SKOS.prefLabel, label))
    return g
