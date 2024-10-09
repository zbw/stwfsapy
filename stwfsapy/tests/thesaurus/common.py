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


from rdflib.term import URIRef, Literal
from rdflib.namespace import Namespace


test_ref_type = URIRef("http://zbw.eu/stw/descriptor")
ZBWEXT = Namespace("http://zbw.eu/namespaces/zbw-extensions/")

_thsys_uri_insurance = "http://zbw.eu/stw/thsys/70892"
_thsys_uri_it = "https://zbw.eu/stw/thsys/73341"

thsys_ref_insurance = URIRef(_thsys_uri_insurance)
thsys_ref_it = URIRef(_thsys_uri_it)

thsys_prefLabel_insurance_en = Literal("Insurance industry", lang="en")


_concept_uri_insurance = "http://zbw.eu/stw/descriptor/13811-5"
_concept_uri_it = "http://zbw.eu/stw/descriptor/30373-6"

concept_ref_insurance = URIRef(_concept_uri_insurance)
concept_ref_it = URIRef(_concept_uri_it)

concept_prefLabel_insurance_en = Literal("Private insurance", lang="en")
concept_prefLabel_insurance_de = Literal("Privatversicherung", lang="de")
concept_prefLabel_insurance_missing = Literal("Privatversicherung")

concept_altLabel_insurance_en = Literal("Mutual insurance", lang="en")
concept_altLabelRelated_insurance_en = Literal(
    "Insurance cooperative",
    lang="en")

concept_prefLabel_it_en = Literal("Electronic identification", lang="en")
concept_altLabelNarrower_it_en = Literal("Digital signature", lang="en")
