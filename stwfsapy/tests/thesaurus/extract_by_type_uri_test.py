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


def test_extract_by_type_uri(typed_label_graph):
    res = list(t.extract_by_type_uri(typed_label_graph, c.test_ref_type))
    assert len(res) == 2
    assert c.concept_ref_insurance in res
    assert c.concept_ref_it in res


def test_extract_by_type_uri_with_remove(typed_label_graph):
    res = list(t.extract_by_type_uri(
        typed_label_graph,
        c.test_ref_type,
        {c.concept_ref_insurance}))
    assert res == [c.concept_ref_it]
