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

from rdflib import URIRef
from rdflib.term import Literal


test_type_thesaurus = URIRef("http://type.org/thesaurus")
test_type_concept = URIRef("http://type.org/concept")


test_thesaurus_ref_0 = URIRef("http://test.org/thesaurus/0")
test_thesaurus_ref_00 = URIRef("http://test.org/thesaurus/00")
test_thesaurus_ref_01 = URIRef("http://test.org/thesaurus/01")
test_thesaurus_ref_1 = URIRef("http://test.org/thesaurus/1")
test_thesaurus_ref_10 = URIRef("http://test.org/thesaurus/10")
test_thesaurus_ref_100 = URIRef("http://test.org/thesaurus/100")


test_thesauri = [
    test_thesaurus_ref_0,
    test_thesaurus_ref_00,
    test_thesaurus_ref_01,
    test_thesaurus_ref_1,
    test_thesaurus_ref_10,
    test_thesaurus_ref_100,

    ]
thsrs_broader = [
    (test_thesaurus_ref_00, test_thesaurus_ref_0),
    (test_thesaurus_ref_01, test_thesaurus_ref_0),
    (test_thesaurus_ref_10, test_thesaurus_ref_1),
    (test_thesaurus_ref_100, test_thesaurus_ref_10),
    ]

test_concept_uri_0_0 = "http://test.org/concept/0_0"
test_concept_uri_01_0 = "http://test.org/concept/01_0"
test_concept_uri_01_00 = "http://test.org/concept/01_00"
test_concept_uri_10_0 = "http://test.org/concept/10_0"
test_concept_uri_10_1 = "http://test.org/concept/10_1"
test_concept_uri_100_0 = "http://test.org/concept/100_0"
test_concept_uri_100_00 = "http://test.org/concept/100_00"
test_concept_uri_100_01 = "http://test.org/concept/100_01"
test_concept_uri_100_02 = "http://test.org/concept/100_02"

test_concept_ref_0_0 = URIRef(test_concept_uri_0_0)
test_concept_ref_01_0 = URIRef(test_concept_uri_01_0)
test_concept_ref_01_00 = URIRef(test_concept_uri_01_00)
test_concept_ref_10_0 = URIRef(test_concept_uri_10_0)
test_concept_ref_10_1 = URIRef(test_concept_uri_10_1)
test_concept_ref_100_0 = URIRef(test_concept_uri_100_0)
test_concept_ref_100_00 = URIRef(test_concept_uri_100_00)
test_concept_ref_100_01 = URIRef(test_concept_uri_100_01)
test_concept_ref_100_02 = URIRef(test_concept_uri_100_02)

test_labels = [
    (test_concept_ref_0_0, Literal("concept-0_0", lang="en")),
    (test_concept_ref_01_0, Literal("concept-01_0", lang="en")),
    (test_concept_ref_01_00, Literal("concept-01_00", lang="en")),
    (test_concept_ref_10_0, Literal("concept-10_0", lang="en")),
    (test_concept_ref_10_1, Literal("concept-10_1", lang="en")),
    (test_concept_ref_100_0, Literal("concept-100_0", lang="en")),
    (test_concept_ref_100_00, Literal("concept-100_00", lang="en")),
    (test_concept_ref_100_01, Literal("concept-100_01", lang="en")),
    (test_concept_ref_100_02, Literal("concept-100_02", lang="en")),
    ]

test_concepts = [
    test_concept_ref_0_0,
    test_concept_ref_01_0,
    test_concept_ref_01_00,
    test_concept_ref_10_0,
    test_concept_ref_10_1,
    test_concept_ref_100_0,
    test_concept_ref_100_00,
    test_concept_ref_100_01,
    test_concept_ref_100_02,
    ]

cncpt_broaders = [
    (test_concept_ref_0_0, test_thesaurus_ref_0),
    (test_concept_ref_01_0, test_thesaurus_ref_01),
    (test_concept_ref_01_00, test_thesaurus_ref_01),
    (test_concept_ref_01_00, test_concept_ref_01_0),
    (test_concept_ref_10_0, test_thesaurus_ref_10),
    (test_concept_ref_10_1, test_thesaurus_ref_10),
    (test_concept_ref_100_0, test_thesaurus_ref_100),
    (test_concept_ref_100_00, test_thesaurus_ref_100),
    (test_concept_ref_100_01, test_thesaurus_ref_100),
    (test_concept_ref_100_02, test_thesaurus_ref_100),
    (test_concept_ref_100_00, test_concept_ref_100_0),
    (test_concept_ref_100_01, test_concept_ref_100_0),
    (test_concept_ref_100_02, test_concept_ref_100_0),
    ]


doc_feature_data = [
    ('cncpt_1', 'f'*3, [3, 4, 0, 2], 0),
    ('cncpt_2', 'f'*6, [1, 8, 23, 12], 1),
    ('cncpt_1', 'f'*15, [12, 36, 25, 7], 0),
    ('cncpt_2', 'f'*12, [8, 102, 17, 9, 20], 0),
    ('cncpt_3', 'f'*70, [13], 1)
]
