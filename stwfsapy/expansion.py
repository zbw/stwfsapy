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


from typing import Callable, Pattern, List
import re


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
        r"\g<1> ?& ?\g<2>", label)


def _expand_abbreviation_with_punctuation_fun(label: str) -> str:
    if label.isupper() and label.isalpha():
        return _upper_case_matcher.sub(r"\g<0>\\.?", label)
    return label


def simple_english_plural_fun(label: str):
    last = label[-1]
    if last == 'y':
        return label[:-1]+'(y|ies)'
    if last.isalpha() and not (last == 's' or last == 'S'):
        return label + 's?'
    return label


def collect_expansion_functions(
        extract_upper_case_from_braces: bool = True,
        extract_any_case_from_braces: bool = False,
        expand_ampersand_with_spaces: bool = True,
        expand_abbreviation_with_punctuation: bool = True,
        ) -> List[Callable[[str], str]]:
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
        ),
    )
    return [fun for flag, fun in options if flag]
