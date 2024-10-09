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


from stwfsapy import expansion as e
import common as c

replacement_fun_upper = e._replace_by_pattern_fun(
    e._upper_case_abbreviation_from_braces_expression)


def test_pattern_match():
    match = e._upper_case_abbreviation_from_braces_expression.match(
        c.test_string_upper
        )
    assert match.group(0) == c.test_string_upper
    assert match.group(1) == c.test_abbreviation_upper


def test_replacement():
    assert replacement_fun_upper(c.test_string_upper) == \
        c.test_abbreviation_upper


def test_no_replacement():
    assert replacement_fun_upper(c.test_string_any) == c.test_string_any


def test_no_match_when_not_at_beginning():
    test_string = " " + c.test_abbreviation_upper
    assert e._upper_case_abbreviation_from_braces_expression.search(
        test_string
    ) is None
