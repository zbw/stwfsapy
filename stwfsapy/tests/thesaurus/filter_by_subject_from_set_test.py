from stwfsapy import thesaurus as t
from stwfsapy.tests.thesaurus import common as c


def test_subject_from_set_filter():
    in0 = c.thsys_ref_print
    in1 = c.concept_ref_printed
    out = c.concept_ref_media
    allowed = {in0, in1}
    in_tuple0 = (in0, "")
    in_tuple1 = (in1, "")
    out_tuple = (out, "")
    iterable = [in_tuple0, out_tuple, in_tuple1]
    result = t._filter_subject_from_set(iterable, allowed)
    assert list(result) == [in_tuple0, in_tuple1]
