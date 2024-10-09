# Copyright 2020-2024 Leibniz Information Centre for Economics
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import pytest
import stwfsapy.thesaurus as t
import stwfsapy.tests.thesaurus.common as c


@pytest.fixture
def patch_module(mocker):
    thesaurus_module = t
    mocker.patch.object(
        thesaurus_module, "_filter_by_langs")
    mocker.patch.object(
        thesaurus_module, "filter_subject_tuples_from_set")
    mocker.patch.object(
        thesaurus_module, "_unwrap_labels")
    # return mocker


@pytest.fixture
def concept_set():
    return {
        c.concept_ref_insurance,
        c.concept_ref_it
    }


def test_no_language_option(label_graph, patch_module):
    t.retrieve_concept_labels(label_graph, langs=set())
    t._filter_by_langs.assert_not_called()


def test_none_language_option(label_graph, patch_module):
    t.retrieve_concept_labels(label_graph, langs=None)
    t._filter_by_langs.assert_not_called()


def test_language_option(label_graph, patch_module):
    t.retrieve_concept_labels(label_graph, langs={"en"})
    t._filter_by_langs.assert_called()


def test_no_prefix_option(label_graph, patch_module):
    t.retrieve_concept_labels(label_graph)
    t.filter_subject_tuples_from_set.assert_not_called()


def test_none_prefix_option(label_graph, patch_module):
    t.retrieve_concept_labels(label_graph, allowed=None)
    t.filter_subject_tuples_from_set.assert_not_called()


def test_prefix_option(label_graph, concept_set, patch_module):
    t.retrieve_concept_labels(
        label_graph,
        concept_set
    )
    t.filter_subject_tuples_from_set.assert_called()


def test_integration(typed_label_graph, concept_set):
    result = list(t.retrieve_concept_labels(
        typed_label_graph,
        allowed=concept_set,
        langs={"en"},
    ))
    assert (
        c.concept_ref_insurance,
        c.concept_prefLabel_insurance_en.value) in result
    assert (
        c.concept_ref_insurance,
        c.concept_altLabel_insurance_en.value) in result
    assert (
        c.concept_ref_insurance,
        c.concept_prefLabel_insurance_de.value) not in result
    assert c.thsys_ref_insurance not in map(lambda t: t[0], result)
