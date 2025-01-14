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


import stwfsapy.expansion as e

lower_string = "lower case"
with_hyphen_string = "WITH-HYPHEN"
upper_case_string = "UCS"


def test_does_not_change_lower():
    assert lower_string == \
        e._expand_abbreviation_with_punctuation_fun(lower_string)


def test_does_not_change_with_symbol():
    assert with_hyphen_string == \
        e._expand_abbreviation_with_punctuation_fun(with_hyphen_string)


def test_inserts_punctuation():
    result = e._expand_abbreviation_with_punctuation_fun(upper_case_string)
    assert len(result) == 4 * len(upper_case_string)
    for i in range(len(upper_case_string)):
        assert result[4*i] == upper_case_string[i]
        assert result[4*i+1] == '\\'
        assert result[4*i+2] == '.'
        assert result[4*i+3] == '?'
