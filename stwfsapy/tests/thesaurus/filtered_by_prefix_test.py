import stwfsapy.thesaurus as t
import stwfsapy.tests.thesaurus.common as c


def test_filters_out_thsys_(tuples_with_thsys):
    thsys_tuple = (c.thsys_ref_print, c.thsys_prefLabel_print_en)
    assert thsys_tuple in tuples_with_thsys
    result = list(t._filter_by_prefix(tuples_with_thsys, c.test_URI_prefix))
    assert thsys_tuple not in result
    assert len(result) == len(tuples_with_thsys)-1
    for tpl in result:
        assert tpl in tuples_with_thsys
