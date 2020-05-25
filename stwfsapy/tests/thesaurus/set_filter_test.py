from stwfsapy import thesaurus as t
from stwfsapy.tests.thesaurus import common as c


def test_filter_subject_tuples_from_set(tuples):
    res = list(
        t._filter_subject_tuples_from_set(tuples, {c.concept_ref_printed}))
    assert len(res) == 2
    assert res[0][0] == c.concept_ref_printed
    assert res[1][0] == c.concept_ref_printed


def test_filter_refs_from_set_complement():
    res = list(
        t._filter_refs_from_set_complement(
            [c.concept_ref_printed, c.concept_ref_media],
            {c.concept_ref_media}
        )
    )
    assert res == [c.concept_ref_printed]
