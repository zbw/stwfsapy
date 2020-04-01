import pytest
from rdflib.term import URIRef, Literal


test_URI_prefix = "http://zbw.eu/stw/descriptor"

_thsys_uri_print = "http://zbw.eu/stw/thsys/70265"

thsys_ref_print = URIRef(_thsys_uri_print)

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
