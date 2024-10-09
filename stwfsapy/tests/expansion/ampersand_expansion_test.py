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


import stwfsapy.expansion as e

first = 'R'
second = 'D'
ampersand_string = "{}&{}".format(first, second)
multi_ampersand_string = "A&" + ampersand_string


def test_matches():
    match = e._ampersand_abbreviation_matcher.search(ampersand_string)
    assert match is not None
    assert match.group(0) == ampersand_string
    assert match.group(1) == first
    assert match.group(2) == second


def test_no_match_at_end_of_string():
    match = e._ampersand_abbreviation_matcher.search(" "+ampersand_string)
    assert match is None


def test_no_match_at_start_of_string():
    match = e._ampersand_abbreviation_matcher.search(ampersand_string + " ")
    assert match is None


def test_no_match_multiple_ampersand():
    match = e._ampersand_abbreviation_matcher.search(multi_ampersand_string)
    assert match is None


def test_replacement():
    replaced = e._expand_ampersand_with_spaces_fun(ampersand_string)
    assert len(replaced) == len(ampersand_string) + 4
    for i in range(len(ampersand_string)-1):
        offset = i * 3
        assert replaced[offset] == ampersand_string[i]
        assert replaced[offset+1] == ' '
        assert replaced[offset+2] == '?'
    assert replaced[-1] == ampersand_string[-1]


def test_no_replacement_multiple_ampersand():
    replaced = e._expand_ampersand_with_spaces_fun(multi_ampersand_string)
    assert replaced == multi_ampersand_string
