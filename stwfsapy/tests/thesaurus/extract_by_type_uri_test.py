from stwfsapy import thesaurus as t
from stwfsapy.tests.thesaurus import common as c


def test_extract_by_type_uri(full_graph):
    res = list(t.extract_by_type_uri(full_graph, c.test_ref_type))
    assert len(res) == 2
    assert c.concept_ref_printed in res
    assert c.concept_ref_media in res


def test_extract_by_type_uri_with_remove(full_graph):
    res = list(t.extract_by_type_uri(
        full_graph,
        c.test_ref_type,
        {c.concept_ref_printed}))
    assert res == [c.concept_ref_media]
