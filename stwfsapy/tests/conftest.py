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

from pytest import fixture
from rdflib.graph import Graph
from rdflib.namespace import RDF, SKOS
from stwfsapy.tests import common as c


@fixture
def full_graph():
    g = Graph()
    for t in c.test_thesauri:
        g.add((t, RDF.type, c.test_type_thesaurus))
    for cncpt in c.test_concepts:
        g.add((cncpt, RDF.type, c.test_type_concept))
    for narrow, broader in c.thsrs_broader:
        g.add((narrow, SKOS.broader, broader))
    for narrow, broader in c.cncpt_broaders:
        g.add((narrow, SKOS.broader, broader))
    for cncpt, label in c.test_labels:
        g.add((cncpt, SKOS.prefLabel, label))
    return g
