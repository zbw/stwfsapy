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


import pytest

from stwfsapy.automata import dfa

symbol = 's'


@pytest.fixture
def two_state_graph():
    graph = dfa.Dfa()
    graph.add_state()
    graph.add_state()
    return graph


@pytest.fixture
def foo_graph(two_state_graph):
    two_state_graph.set_non_word_char_transition(0, 1)
    two_state_graph.add_state()
    two_state_graph.set_symbol_transition(1, 2, 'f')
    two_state_graph.add_state()
    two_state_graph.set_symbol_transition(2, 3, 'o')
    two_state_graph.set_symbol_transition(3, 3, 'o')
    two_state_graph.add_state()
    two_state_graph.set_non_word_char_transition(3, 4)
    two_state_graph.add_acceptances(4, ["bar"])
    return two_state_graph


def test_add_state(two_state_graph):
    old_len = len(two_state_graph.states)
    two_state_graph.add_state()
    assert len(two_state_graph.states) == old_len + 1


def test_add_acceptance(two_state_graph):
    accept = "Acceptance!"
    idx = 1
    two_state_graph.add_acceptances(idx, [accept])
    assert accept in two_state_graph.states[idx].accepts


def test_set_symbol_transition(two_state_graph):
    two_state_graph.set_symbol_transition(0, 1, symbol)
    assert two_state_graph.states[0].symbol_transitions[symbol] == 1


def test_override_symbol_transition(two_state_graph):
    two_state_graph.set_symbol_transition(0, 1, symbol)
    idx = two_state_graph.add_state()
    two_state_graph.set_symbol_transition(0, idx, symbol)
    assert two_state_graph.states[0].symbol_transitions[symbol] == idx


def test_set_non_word_char_transition(two_state_graph):
    two_state_graph.set_non_word_char_transition(0, 1)
    assert two_state_graph.states[0].non_word_char_transition == 1


def test_search(foo_graph):
    text = "fooo"
    res = list(foo_graph.search(text))
    assert len(res) == 1
    assert res[0][0] == 'bar'
    assert res[0][1] == text
    assert res[0][2] == 0
    assert res[0][3] == 4


def test_serialization_inversion(foo_graph):
    assert foo_graph == dfa.Dfa.from_dict(
        foo_graph.to_dict(lambda x: x), lambda x: x)
