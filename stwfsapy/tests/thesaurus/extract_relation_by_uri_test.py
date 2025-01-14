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

from rdflib import graph
from rdflib.namespace import SKOS

from stwfsapy import thesaurus as t


def test_extract_broader(mocker):
    g = graph.Graph()
    spy = mocker.spy(g, "subject_objects")
    t.extract_relation_by_uri(g, SKOS.broader, False)
    spy.assert_called_once_with(SKOS.broader)


def test_can_reverse(mocker):
    def mock_iter(a):
        yield (1, 3)
        yield (2, 4)
    g = graph.Graph()
    mocker.patch.object(g, 'subject_objects', mock_iter)
    res = t.extract_relation_by_uri(g, SKOS.broader, True)
    assert list(res) == [(3, 1), (4, 2)]
