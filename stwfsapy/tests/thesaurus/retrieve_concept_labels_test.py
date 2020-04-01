import pytest
import stwfsapy.thesaurus as t
import stwfsapy.tests.thesaurus.common as c


@pytest.fixture
def patch_module(mocker):
    thesaurus_module = t
    mocker.patch.object(
        thesaurus_module, "_filter_by_langs")
    mocker.patch.object(
        thesaurus_module, "_filter_by_prefix")
    mocker.patch.object(
        thesaurus_module, "_filter_not_deprecated")
    mocker.patch.object(
        thesaurus_module, "_unwrap_labels")
    # return mocker


def test_no_language_option(label_graph, patch_module):
    labels = t.retrieve_concept_labels(
        label_graph,
        langs=set()
    )
    t._filter_by_langs.assert_not_called()


def test_none_language_option(label_graph, patch_module):
    labels = t.retrieve_concept_labels(
        label_graph,
        langs=None
    )
    t._filter_by_langs.assert_not_called()


def test_language_option(label_graph, patch_module):
    labels = t.retrieve_concept_labels(
        label_graph,
        langs={"en"}
    )
    t._filter_by_langs.assert_called()


def test_no_prefix_option(label_graph, patch_module):
    labels = t.retrieve_concept_labels(
        label_graph,
    )
    t._filter_by_prefix.assert_not_called()


def test_none_prefix_option(label_graph, patch_module):
    labels = t.retrieve_concept_labels(
        label_graph,
        concept_URI_prefix=None
    )
    t._filter_by_prefix.assert_not_called()


def test_prefix_option(label_graph, patch_module):
    labels = t.retrieve_concept_labels(
        label_graph,
        concept_URI_prefix=c.test_URI_prefix
    )
    t._filter_by_prefix.assert_called()


def test_integration(full_graph):
    result = list(t.retrieve_concept_labels(
        full_graph,
        concept_URI_prefix=c.test_URI_prefix,
        langs={"en"},
    ))
    assert (
        c.concept_ref_printed,
        c.concept_prefLabel_printed_en.value) in result
    assert (
        c.concept_ref_printed,
        c.concept_altLabel_printed_en.value) in result
    assert (
        c.concept_ref_printed,
        c.concept_prefLabel_printed_de.value) not in result
    assert c.thsys_ref_print not in map(lambda t: t[0], result)
