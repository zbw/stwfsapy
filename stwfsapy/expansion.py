from typing import Iterator, Callable, Pattern
import re
from functools import reduce


_upper_case_abbreviation_from_braces_expression = re.compile(
   r"^([A-Z-]{2,})\s*\(.{3,}?\)"
)

_any_case_from_braces_expression = re.compile(
    r"\((.{3,}?)\)"
)

_ampersand_abbreviation_matcher = re.compile(r"^([A-Z])&([A-Z])$")
"""Matches terms like R&D.
Assumes that there are not multiple ampersands and only single
capital letters at each side."""


_upper_case_matcher = re.compile(r"([A-Z])")
"""Matches capital letters.
This is used for inserting optional dots between the letters."""


def _replace_by_pattern_fun(pattern: Pattern[str]) -> Callable[[str], str]:
    def replacer(label: str) -> str:
        match = pattern.search(label)
        if match is None:
            return label
        return match[1]
    return replacer


def _expand_ampersand_with_spaces_fun(label: str) -> str:
    return _ampersand_abbreviation_matcher.sub(
        r"\g<1> ?& ?\g<2>\\W", label)


def _expand_abbreviation_with_punctuation_fun(label: str) -> str:
    if label.isupper() and label.isalpha():
        return _upper_case_matcher.sub(r"\g<0>.?", label) + "\\W"
    return label


def collect_expansion_functions(
        extract_upper_case_from_braces: bool=True,
        extract_any_case_from_braces: bool=False,
        expand_ampersand_with_spaces: bool=True,
        expand_abbreviation_with_punctuation: bool=True
        ) -> Callable[[str], str]:
    options = (
        (
            extract_upper_case_from_braces,
            _replace_by_pattern_fun(
                _upper_case_abbreviation_from_braces_expression)
        ),
        (
            extract_any_case_from_braces,
            _replace_by_pattern_fun(_any_case_from_braces_expression)
        ),
        (
            expand_ampersand_with_spaces,
            _expand_ampersand_with_spaces_fun
        ),
        (
            expand_abbreviation_with_punctuation,
            _expand_abbreviation_with_punctuation_fun
        )
    )
    return [fun for flag, fun in options if flag]
