from typing import Tuple, Set, Iterator
from rdflib import Graph
from rdflib.term import Literal, URIRef
from rdflib.namespace import SKOS, OWL


def extract_labels(g: Graph,) -> Iterator[Tuple[URIRef, Literal]]:
    """
    Extracts SKOS.prefLabels and SKOS.altLabels from a rdflib.Graph
    """
    return g[:SKOS.prefLabel | SKOS.altLabel]


def _predicate_deprecated(ref: URIRef, g: Graph):
    return not g.value(ref, OWL.deprecated, default=False)


def _filter_not_deprecated(
        tuples: Iterator[Tuple[URIRef, Literal]],
        g: Graph
        ) -> Iterator[Tuple[URIRef, Literal]]:
    return filter(lambda t: _predicate_deprecated(t[0], g), tuples)


def _predicate_prefix(uri: URIRef, prefix: str) -> bool:
    """Checks whether a string starts with the given prefix."""
    return uri.toPython().startswith(prefix)


def _filter_by_prefix(
        tuples: Iterator[Tuple[URIRef, str]],
        prefix: str
        ) -> Iterator[Tuple[URIRef, str]]:
    """
    Consumes an interator of (URI string, _) tuples.
    Removes any items where the URI string
    does not start with the given prefix.
    """
    return filter(lambda t: _predicate_prefix(t[0], prefix), tuples)


def _predicate_langs(lit: Literal, langs: Set[str]) -> bool:
    return lit.language in langs


def _filter_by_langs(
        tuples: Iterator[Tuple[URIRef, Literal]],
        langs: Set[str]
        ) -> Iterator[Tuple[URIRef, Literal]]:
    return filter(lambda t: _predicate_langs(t[1], langs), tuples)


def _unwrap_label(tuple: Tuple[URIRef, Literal]) -> Tuple[URIRef, str]:
    return (tuple[0], tuple[1].value)


def _unwrap_labels(
        tuples: Iterator[Tuple[URIRef, Literal]]
        ) -> Iterator[Tuple[URIRef, str]]:
    return map(_unwrap_label, tuples)


def retrieve_concept_labels(
        g: Graph,
        concept_URI_prefix: str="",
        langs: Set[str]={}
        ) -> Iterator[Tuple[URIRef, str]]:
    """Extracts altLabels and prefLabels from a SKOS graph.

    Only the labels that are in one of the specified language will be reported.
    In addition the concept URIs are filtered by a prefix.
    Args:
        g: The SKOS graph whose labels are extracted.

        concept_URI_prefix: Only concepts whose URI starts with this prefix
            will appear in the output.


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
    if concept_URI_prefix is not None and len(concept_URI_prefix) > 0:
        filtered_by_prefix = _filter_by_prefix(
            filtered_by_language,
            concept_URI_prefix)
    else:
        filtered_by_prefix = filtered_by_language
    without_deprecated = _filter_not_deprecated(filtered_by_prefix, g)
    unwrapped_labels = _unwrap_labels(without_deprecated)
    return unwrapped_labels
