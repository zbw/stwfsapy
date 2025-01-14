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

from stwfsapy import thesaurus as t
from stwfsapy.tests.thesaurus import common as c


def test_filter_subject_tuples_from_set(tuples):
    res = list(
        t.filter_subject_tuples_from_set(tuples, {c.concept_ref_insurance}))
    assert len(res) == 2
    assert res[0][0] == c.concept_ref_insurance
    assert res[1][0] == c.concept_ref_insurance


def test_filter_refs_from_set_complement():
    res = list(
        t._filter_refs_from_set_complement(
            [c.concept_ref_insurance, c.concept_ref_it],
            {c.concept_ref_it}
        )
    )
    assert res == [c.concept_ref_insurance]
