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


from stwfsapy.automata import conversion as c
from stwfsapy.tests.automata.data import accept, symbol0, symbol1


def test_conversion(input_graph, mocker):
    converter = c.NfaToDfaConverter(input_graph)
    # Mainly interested in the end result.
    # Still mock to see that there are no unknown elements
    add_spy = mocker.spy(converter.dfa, "add_state")
    symbol_transition_spy = mocker.spy(converter.dfa, "set_symbol_transition")
    nwc_transition_spy = mocker.spy(
        converter.dfa,
        "set_non_word_char_transition")
    acceptance_spy = mocker.spy(converter.dfa, "add_acceptances")
    result = converter.start_conversion()
    assert converter.queue.qsize() == 0
    assert len(converter.state_cache) == 6
    assert len(converter.state_represents) == 6
    # One less call than states in the graph,
    # because the initial state was added during construction.
    assert add_spy.call_count == 5
    assert nwc_transition_spy.call_count == 1
    assert symbol_transition_spy.call_count == 7
    assert acceptance_spy.call_count == 1
    state01 = converter.state_cache[frozenset([0, 1])]
    state02 = converter.state_cache[frozenset([0, 2])]
    assert result.states[state01].symbol_transitions[symbol0] == state02
    state3 = converter.state_cache[frozenset([3])]
    assert result.states[state01].symbol_transitions[symbol1] == state3
    assert result.states[state02].symbol_transitions[symbol1] == state3
    state24 = converter.state_cache[frozenset([2, 4])]
    assert result.states[state02].symbol_transitions[symbol0] == state24
    state5 = converter.state_cache[frozenset([5])]
    assert result.states[state24].symbol_transitions[symbol1] == state5
    state4 = converter.state_cache[frozenset([4])]
    assert result.states[state24].symbol_transitions[symbol0] == state4
    assert result.states[state4].symbol_transitions[symbol1] == state5
    assert result.states[state5].accepts == [accept]


def test_creates_new_state(input_graph):
    converter = c.NfaToDfaConverter(input_graph)
    new_set = frozenset([0, 2])
    converter._get_or_create_dfa_state(new_set)
    assert len(converter.dfa.states) == 2
    assert converter.queue.qsize() == 2
    assert len(converter.state_cache) == 2
    assert len(converter.state_represents) == 2
    assert converter.state_represents[1] == list(new_set)
    assert converter.state_cache[new_set] == 1


def test_retrieves_existing_state(input_graph):
    converter = c.NfaToDfaConverter(input_graph)
    new_set = frozenset(input_graph.starts)
    converter._get_or_create_dfa_state(new_set)
    assert len(converter.dfa.states) == 1
    assert converter.queue.qsize() == 1
    assert len(converter.state_cache) == 1
    assert len(converter.state_represents) == 1


def test_initialization(input_graph):
    converter = c.NfaToDfaConverter(input_graph)
    start_set = frozenset(input_graph.starts)
    assert len(converter.dfa.states) == 1
    assert converter.queue.qsize() == 1
    assert len(converter.state_cache) == 1
    assert len(converter.state_represents) == 1
    assert converter.state_represents[0] == list(start_set)
    assert converter.state_cache[start_set] == 0


def test_transition_collection(input_graph):
    converter = c.NfaToDfaConverter(input_graph)
    state_set = {0, 1, 3, 5}
    (
        symbol_transitions,
        non_word_char_transitions,
        accepts
    ) = converter._collect_nfa_transitions(state_set)
    for state_id in state_set:
        state = input_graph.states[state_id]
        for k, idxs in state.symbol_transitions.items():
            for idx in idxs:
                assert idx in symbol_transitions[k]
        for v in state.non_word_char_transitions:
            assert v in non_word_char_transitions
        for v in state.accepts:
            assert v in accepts
    for k, idxs in symbol_transitions.items():
        for idx in idxs:
            found = False
            for state in state_set:
                nfa_state = input_graph.states[state]
                if idx in nfa_state.symbol_transitions.get(k, []):
                    found = True
            assert found
    for v in non_word_char_transitions:
        found = False
        for state in state_set:
            if v in input_graph.states[state].non_word_char_transitions:
                found = True
        assert found
    for v in accepts:
        found = False
        for state in state_set:
            if v in input_graph.states[state].accepts:
                found = True
        assert found


def test_transition_creation(input_graph):
    converter = c.NfaToDfaConverter(input_graph)
    set13 = frozenset([1, 3])
    set24 = frozenset([2, 4])
    set5 = frozenset([5])
    acceptance = {accept}
    non_word_char_transitions = set(set24)
    symbol_transitions = {
        symbol0: set(set13),
        symbol1: set(set5)
    }
    converter._create_dfa_transitions(
        0,
        symbol_transitions,
        non_word_char_transitions,
        acceptance
    )
    state = converter.dfa.states[0]
    assert state.accepts == [accept]
    assert state.non_word_char_transition == converter.state_cache[set24]
    assert state.symbol_transitions[symbol0] == converter.state_cache[set13]
    assert state.symbol_transitions[symbol1] == converter.state_cache[set5]
