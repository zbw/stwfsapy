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

import stwfsapy.case_handlers as handlers

_inp = 'foo bar'
_inp_upper = 'F.?O.?O.?'


def test_uncase_first_char_lower():
    res = handlers.uncase_first_char('lower')
    assert res == '(L|l)ower'


def test_uncase_first_char_upper():
    res = handlers.uncase_first_char('Upper')
    assert res == '(U|u)pper'


def test_uncase_first_char_symbol():
    input = '\\?something'
    res = handlers.uncase_first_char(input)
    assert res == '\\?something'


def test_uncase_diacritic():
    input = 'ӟ'
    res = handlers.uncase_first_char(input)
    assert res == '(Ӟ|ӟ)'


def test_sentence_case_handles_upper():
    assert _inp_upper == handlers.sentence_case_handler(_inp_upper)


def test_title_case_handles_upper():
    assert _inp_upper == handlers.title_case_handler(_inp_upper)


def test_sentence_case_handler():
    res = handlers.sentence_case_handler(_inp)
    assert res == '(F|f)oo bar'


def test_title_case_handler():
    res = handlers.title_case_handler(_inp)
    assert res == '(F|f)oo (B|b)ar'
