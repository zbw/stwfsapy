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


from stwfsapy.expansion import base_expansion


def test_curly_open():
    input = 'some { thing'
    out = base_expansion(input)
    assert out == 'some \\{ thing'


def test_curly_close():
    input = 'some } thing'
    out = base_expansion(input)
    assert out == 'some \\} thing'


def test_curly_both():
    input = 'some {thing}'
    out = base_expansion(input)
    assert out == 'some \\{thing\\}'


def test_round_open():
    input = 'some ( thing'
    out = base_expansion(input)
    assert out == 'some \\( thing'


def test_round_close():
    input = 'some ) thing'
    out = base_expansion(input)
    assert out == 'some \\) thing'


def test_round_both():
    input = 'some (thing)'
    out = base_expansion(input)
    assert out == 'some \\(thing\\)'


def test_square_open():
    input = 'some [ thing'
    out = base_expansion(input)
    assert out == 'some \\[ thing'


def test_square_close():
    input = 'some ] thing'
    out = base_expansion(input)
    assert out == 'some \\] thing'


def test_square_both():
    input = 'some [thing]'
    out = base_expansion(input)
    assert out == 'some \\[thing\\]'


def test_asterisk():
    input = 'Something text with * inside'
    out = base_expansion(input)
    assert out == 'Something text with \\* inside'


def test_question_mark():
    input = 'Something text with ? inside'
    out = base_expansion(input)
    assert out == 'Something text with \\? inside'
