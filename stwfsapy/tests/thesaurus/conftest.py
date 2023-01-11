# Copyright 2020-2023 Leibniz Information Centre for Economics
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
from stwfsapy.tests.thesaurus import common as c
from rdflib import Graph
from rdflib.namespace import SKOS, RDF


@pytest.fixture
def tuples():
    return [
        (c.concept_ref_printed, c.concept_prefLabel_printed_en),
        (c.concept_ref_media, c.concept_prefLabel_media_en),
        (c.concept_ref_printed, c.concept_prefLabel_printed_missing)
    ]


@pytest.fixture
def label_graph():
    g = Graph()
    g.add((
        c.concept_ref_printed,
        SKOS.prefLabel,
        c.concept_prefLabel_printed_en))
    g.add((
        c.concept_ref_printed,
        SKOS.altLabel,
        c.concept_altLabel_printed_en))
    g.add((
        c.concept_ref_media,
        SKOS.altLabel,
        c.concept_altLabel_printed_en))
    return g


@pytest.fixture
def typed_label_graph(label_graph):
    g = label_graph
    g.add((
        c.concept_ref_printed,
        SKOS.prefLabel,
        c.concept_prefLabel_printed_de))
    g.add((
        c.thsys_ref_print,
        SKOS.prefLabel,
        c.thsys_prefLabel_print_en))
    g.add((
        c.concept_ref_media,
        RDF.type,
        c.test_ref_type))
    g.add((
        c.concept_ref_printed,
        RDF.type,
        c.test_ref_type))
    return g
