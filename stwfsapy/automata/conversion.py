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


from typing import Tuple, Set
from stwfsapy.automata import dfa
from stwfsapy.automata import nfa
from queue import Queue

from stwfsapy.automata.util import safe_set_update_in_dict


class NfaToDfaConverter:

    def __init__(self, nfa_automaton: nfa.Nfa):
        self.nfa = nfa_automaton
        self.dfa = dfa.Dfa()
        idx0 = self.dfa.add_state()
        self.queue = Queue()
        self.queue.put(idx0)
        start_states = frozenset(self.nfa.starts)
        self.state_represents = {idx0: list(start_states)}
        self.state_cache = {start_states: 0}

    def start_conversion(self) -> dfa.Dfa:
        while self.queue.qsize() > 0:
            self.perform_step(self.queue.get())
            self.queue.task_done()
        return self.dfa

    def perform_step(self, dfa_start_state_idx):
        (
            symbol_transitions,
            non_word_char_transitions,
            accepts
        ) = self._collect_nfa_transitions(
            self.state_represents[dfa_start_state_idx])
        self._create_dfa_transitions(
            dfa_start_state_idx,
            symbol_transitions,
            non_word_char_transitions,
            accepts)

    def _collect_nfa_transitions(self, states: Set[nfa.State]) -> Tuple:
        symbol_transitions = dict()
        non_word_char_transitions = set()
        accepts = set()
        for nfa_start_idx in states:
            for (
                symbol,
                nfa_end_state_idxs) in (
                    self.nfa.states[nfa_start_idx].symbol_transitions.items()):
                safe_set_update_in_dict(
                    symbol_transitions,
                    symbol,
                    nfa_end_state_idxs)
            non_word_char_transitions.update(
                    self.nfa.states[nfa_start_idx].non_word_char_transitions)
            accepts.update(self.nfa.states[nfa_start_idx].accepts)
        return symbol_transitions, non_word_char_transitions, accepts

    def _create_dfa_transitions(
            self,
            dfa_start_state_idx,
            symbol_transitions,
            non_word_char_transitions,
            accepts):
        for symbol, nfa_end_state_idxs in symbol_transitions.items():
            dfa_end_state_idx = self._get_or_create_dfa_state(
                nfa_end_state_idxs)
            self.dfa.set_symbol_transition(
                dfa_start_state_idx,
                dfa_end_state_idx,
                symbol)
        if len(non_word_char_transitions) > 0:
            dfa_end_state_idx = self._get_or_create_dfa_state(
                non_word_char_transitions)
            self.dfa.set_non_word_char_transition(
                dfa_start_state_idx,
                dfa_end_state_idx)
        if len(accepts) > 0:
            self.dfa.add_acceptances(dfa_start_state_idx, accepts)

    def _get_or_create_dfa_state(self, state_idxs) -> int:
        frozen_states = frozenset(state_idxs)
        try:
            dfa_state_idx = self.state_cache[frozen_states]
        except KeyError:
            dfa_state_idx = self.dfa.add_state()
            self.queue.put(dfa_state_idx)
            self.state_represents[dfa_state_idx] = list(frozen_states)
            self.state_cache[frozen_states] = dfa_state_idx
            acceptance = set()
            for state_idx in state_idxs:
                acceptance.union(self.nfa.states[state_idx].accepts)
            dfa_state = self.dfa.states[dfa_state_idx]
            dfa_state.accepts = list(acceptance)

        return dfa_state_idx
