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


from rdflib.term import URIRef, Literal


test_ref_type = URIRef("http://zbw.eu/stw/descriptor")

_thsys_uri_print = "http://zbw.eu/stw/thsys/70265"
_thsys_uri_media = "https://zbw.eu/stw/thsys/181994"

thsys_ref_print = URIRef(_thsys_uri_print)
thsys_ref_media = URIRef(_thsys_uri_media)

thsys_prefLabel_print_en = Literal("Printed matters", lang="en")


_concept_uri_printed = "http://zbw.eu/stw/descriptor/14812-5"
_concept_uri_media = "http://zbw.eu/stw/descriptor/18211-4"

concept_ref_printed = URIRef(_concept_uri_printed)
concept_ref_media = URIRef(_concept_uri_media)

concept_prefLabel_printed_en = Literal("Printed Products", lang="en")
concept_prefLabel_printed_de = Literal("Druckerzeugnis", lang="de")
concept_prefLabel_printed_missing = Literal("Druckerzeugnis")

concept_altLabel_printed_en = Literal("Print Media", lang="en")

concept_prefLabel_media_en = Literal("Press media", lang="en")
