# Copyright 2020 Leibniz Information Centre for Economics
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
from stwfsapy.tests.thesaurus.common import *
from rdflib import Graph
from rdflib.namespace import SKOS


@pytest.fixture
def tuples():
    return[
        (concept_ref_printed, concept_prefLabel_printed_en),
        (concept_ref_media, concept_prefLabel_media_en),
        (concept_ref_printed, concept_prefLabel_printed_missing)
    ]


@pytest.fixture
def tuples_with_thsys(tuples):
    tuples.append((thsys_ref_print, thsys_prefLabel_print_en))
    return tuples


@pytest.fixture
def label_graph():
    g = Graph()
    g.add((
        concept_ref_printed,
        SKOS.prefLabel,
        concept_prefLabel_printed_en))
    g.add((
        concept_ref_printed,
        SKOS.altLabel,
        concept_altLabel_printed_en))
    return g


@pytest.fixture
def full_graph(label_graph):
    g = label_graph
    g.add((
        concept_ref_printed,
        SKOS.prefLabel,
        concept_prefLabel_printed_de))
    g.add((
        thsys_ref_print,
        SKOS.prefLabel,
        thsys_prefLabel_print_en))
    return g
