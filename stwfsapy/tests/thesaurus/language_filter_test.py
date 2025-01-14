# Copyright 2020-2025 Leibniz Information Centre for Economics
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
from stwfsapy import thesaurus as t
import stwfsapy.tests.thesaurus.common as c


@pytest.fixture
def multi_lang_tuples():
    return [
        (c.concept_ref_insurance, c.concept_prefLabel_insurance_en),
        (c.concept_ref_insurance, c.concept_prefLabel_insurance_de),
        (c.concept_ref_insurance, c.concept_prefLabel_insurance_missing)
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
