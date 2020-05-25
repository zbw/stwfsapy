from rdflib.namespace import OWL
from rdflib.term import Literal
from stwfsapy import thesaurus as t
from stwfsapy.tests.thesaurus import common as c


def test_extract_deprecated(label_graph):
    label_graph.add((c.concept_ref_printed, OWL.deprecated, Literal(True)))
    res = list(t.extract_deprecated(label_graph))
    assert res == [c.concept_ref_printed]