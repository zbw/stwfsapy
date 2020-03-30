import stwfsapy.thesaurus as t
import stwfsapy.tests.thesaurus.common as c


def test_extract_labels(label_graph):
    extracted = list(t.extract_labels(label_graph))
    assert (c.concept_ref_printed, c.concept_prefLabel_printed_en) in extracted
    assert (c.concept_ref_printed, c.concept_altLabel_printed_en) in extracted
