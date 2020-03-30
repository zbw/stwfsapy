from stwfsapy.tests.thesaurus.common import *
from rdflib import Graph
from rdflib.term import Literal
from rdflib.namespace import SKOS, OWL


@pytest.fixture
def tuples():
    return[
        (concept_ref_printed, concept_prefLabel_printed_en),
        (concept_ref_media, concept_prefLabel_media_en),
        (concept_ref_printed, concept_prefLabel_printed_missing)
    ]


@pytest.fixture
def tuples_with_thsys(tuples):
    tuples.append((thsys_ref_print, thsys_prefLabel_print_en))
    return tuples


@pytest.fixture
def label_graph():
    g = Graph()
    g.add((
        concept_ref_printed,
        SKOS.prefLabel,
        concept_prefLabel_printed_en))
    g.add((
        concept_ref_printed,
        SKOS.altLabel,
        concept_altLabel_printed_en))
    return g


@pytest.fixture
def full_graph(label_graph):
    g = label_graph
    g.add((
        concept_ref_printed,
        SKOS.prefLabel,
        concept_prefLabel_printed_de))
    g.add((
        thsys_ref_print,
        SKOS.prefLabel,
        thsys_prefLabel_print_en))
    return g
