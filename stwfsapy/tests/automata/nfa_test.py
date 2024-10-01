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


import pytest
from stwfsapy.automata import nfa
from stwfsapy.tests.automata.data import symbol0


@pytest.fixture
def two_state_graph():
    graph = nfa.Nfa()
    graph.add_state()
    graph.add_state()
    return graph


@pytest.fixture
def epsilon_tree():
    graph = nfa.Nfa()
    for _ in range(17):
        graph.add_state()
    for i in range(8):
        graph.add_empty_transition(i, 2*i+1)
        graph.add_empty_transition(i, 2*i+2)
        graph.add_symbol_transition(i, 2*i+1, symbol0)
        graph.add_symbol_transition(i, 2*i+2, symbol0)
        graph.add_non_word_char_transition(i, 2*i+1)
        graph.add_non_word_char_transition(i, 2*i+2)
    return graph


@pytest.fixture
def epsilon_circle(epsilon_tree):
    epsilon_tree.add_empty_transition(16, 3)
    return epsilon_tree


def test_add_state(two_state_graph):
    two_state_graph.add_state()
    assert len(two_state_graph.states) == 3


def test_add_start(two_state_graph):
    two_state_graph.add_start(1)
    assert 1 in two_state_graph.starts


def test_add_acceptance(two_state_graph):
    acc = "Acceptance!"
    two_state_graph.add_acceptance(1, acc)
    assert acc in two_state_graph.states[1].accepts


def test_add_symbol_transition(two_state_graph):
    two_state_graph.add_symbol_transition(0, 1, symbol0)
    assert 1 in two_state_graph.states[0].symbol_transitions[symbol0]


def test_add_empty_transition(two_state_graph):
    two_state_graph.add_empty_transition(0, 1)
    assert 1 in two_state_graph.states[0].empty_transitions
    assert 0 in two_state_graph.states[1].incoming_empty_transitions


def test_add_non_word_char_transition(two_state_graph):
    two_state_graph.add_non_word_char_transition(0, 1)
    assert 1 in two_state_graph.states[0].non_word_char_transitions


def test_remove_epsilons(epsilon_tree):
    epsilon_tree.remove_empty_transitions()
    state = epsilon_tree.states[0]
    assert len(state.empty_transitions) == 0
    assert len(state.incoming_empty_transitions) == 0
    for idx in range(1, 16):
        assert idx in epsilon_tree.states[0].symbol_transitions[symbol0]
        assert idx in epsilon_tree.states[0].non_word_char_transitions
        state = epsilon_tree.states[idx]
        assert len(state.empty_transitions) == 0
        assert len(state.incoming_empty_transitions) == 0


def test_recognizes_empty_loops(epsilon_circle):
    with pytest.raises(Exception) as exc:
        epsilon_circle.remove_empty_transitions()
    assert exc.value.args[0] == "There is an empty transition loop in the NFA."
