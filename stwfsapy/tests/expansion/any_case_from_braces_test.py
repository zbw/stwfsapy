# Copyright 2020-2025 Leibniz Information Centre for Economics
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

replacement_fun_any = e._replace_by_pattern_fun(
    e._any_case_from_braces_expression)


def test_pattern_match():
    match = e._any_case_from_braces_expression.search(
        c.test_string_any
        )
    assert match.group(0) == "\\({}\\)".format(c.test_abbreviation_any)
    assert match.group(1) == c.test_abbreviation_any


def test_replacement():
    assert replacement_fun_any(c.test_string_any) == \
        c.test_abbreviation_any


def test_no_replacement():
    some_string = "some string\\)"
    assert replacement_fun_any(some_string) == some_string
