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


from typing import Tuple, FrozenSet, Iterable, Any, Optional
from rdflib import Graph
from rdflib.term import Literal, URIRef
from rdflib.namespace import SKOS, OWL, RDF


def extract_labels(g: Graph) -> Iterable[Tuple[URIRef, Literal]]:
    """
    Extracts SKOS.prefLabels and SKOS.altLabels from a rdflib.Graph
    """
    return g[: SKOS.prefLabel | SKOS.altLabel]


def extract_by_type_uri(
        g: Graph,
        type_URI: URIRef,
        remove: Optional[FrozenSet[URIRef]] = None) -> Iterable[URIRef]:
    """Extract all elements of a specific type from a rdflib graph.
    Allows to exclude the elements that are in a specified set."""
    by_type = g[:RDF.type:type_URI]
    if not remove:
        return by_type
    else:
        return _filter_refs_from_set_complement(by_type, remove)


def extract_deprecated(g: Graph):
    return g[:OWL.deprecated: Literal(True)]


def extract_relation_by_uri(g: Graph, uri: URIRef, reverse: bool):
    subj_objs = g[:uri:]
    if reverse:
        return map(lambda x: (x[1], x[0]), subj_objs)
    else:
        return subj_objs


def _predicate_uri_from_set(uri: URIRef, uri_set: FrozenSet[URIRef]):
    return uri in uri_set


def filter_subject_tuples_from_set(
        tuples: Iterable[Tuple[URIRef, Any]],
        uri_set: FrozenSet[URIRef]
        ) -> Iterable[Tuple[URIRef, Any]]:
    """Filters an iterable of tuples.
    Keeps only tuples where the first element is
    present in the provided set."""
    return filter(lambda t: _predicate_uri_from_set(t[0], uri_set), tuples)


def _predicate_refs_from_set_complement(
        uri: URIRef,
        uri_set: FrozenSet[URIRef]):
    return uri not in uri_set


def _filter_refs_from_set_complement(
        tuples: Iterable[URIRef],
        uri_set: FrozenSet[URIRef],
        ):
    return filter(
        lambda t: _predicate_refs_from_set_complement(t, uri_set),
        tuples)


def _predicate_langs(lit: Literal, langs: FrozenSet[str]) -> bool:
    return lit.language in langs


def _filter_by_langs(
        tuples: Iterable[Tuple[URIRef, Literal]],
        langs: FrozenSet[str]
        ) -> Iterable[Tuple[URIRef, Literal]]:
    return filter(lambda t: _predicate_langs(t[1], langs), tuples)


def _unwrap_label(tuple: Tuple[URIRef, Literal]) -> Tuple[URIRef, str]:
    return (tuple[0], tuple[1].value)


def _unwrap_labels(
        tuples: Iterable[Tuple[URIRef, Literal]]
        ) -> Iterable[Tuple[URIRef, str]]:
    return map(_unwrap_label, tuples)


def retrieve_concept_labels(
        g: Graph,
        allowed: Optional[FrozenSet[URIRef]] = frozenset(),
        langs: FrozenSet[str] = frozenset()
        ) -> Iterable[Tuple[URIRef, str]]:
    """Extracts altLabels and prefLabels from a SKOS graph.

    Only the labels that are in one of the specified language will be reported.
    In addition the concept URIs can be limited by a set.
    Args:
        g: The SKOS graph whose labels are extracted.

        allowed: Only concepts present in the set are retained.
            If None or the set is empty
            all concepts will be present in the result.


        langs: Only retain labels that are in the given language.
            Add None to the set if you want to keep labels
            without a language annotation.


    Returns:
        An iterator of pairs. The first element is a URIRef,
        representing a concept.
        The second element is a label for the concept.

        """
    refs_with_labels = extract_labels(g)
    if langs is not None and len(langs) > 0:
        filtered_by_language = _filter_by_langs(refs_with_labels, langs)
    else:
        filtered_by_language = refs_with_labels
    if allowed:
        filtered_by_set = filter_subject_tuples_from_set(
            filtered_by_language,
            allowed)
    else:
        filtered_by_set = filtered_by_language
    unwrapped_labels = _unwrap_labels(filtered_by_set)
    return unwrapped_labels
