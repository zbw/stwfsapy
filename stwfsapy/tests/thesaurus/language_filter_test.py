import pytest
from stwfsapy import thesaurus as t
import stwfsapy.tests.thesaurus.common as c


@pytest.fixture
def multi_lang_tuples():
    return [
        (c.concept_ref_printed, c.concept_prefLabel_printed_en),
        (c.concept_ref_printed, c.concept_prefLabel_printed_de),
        (c.concept_ref_printed, c.concept_prefLabel_printed_missing)
    ]


def test_filter_multiple_languages(multi_lang_tuples):
    langs = {"de", "en"}
    filtered = list(t._filter_by_langs(multi_lang_tuples, langs))
    assert len(filtered) == 2
    for ref, label in filtered:
        assert label.language in langs


def test_filter_single_language(multi_lang_tuples):
    lang = "de"
    langs = {lang}
    filtered = list(t._filter_by_langs(multi_lang_tuples, langs))
    assert len(filtered) == 1
    for ref, label in filtered:
        assert label.language == lang


def test_filter_none_language(multi_lang_tuples):
    lang = None
    langs = {lang}
    filtered = list(t._filter_by_langs(multi_lang_tuples, langs))
    assert len(filtered) == 1
    for ref, label in filtered:
        assert label.language == lang
