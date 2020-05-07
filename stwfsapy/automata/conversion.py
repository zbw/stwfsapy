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


from collections import defaultdict
from typing import Tuple, Set, Dict, FrozenSet, Iterable, List
from stwfsapy.automata import dfa
from stwfsapy.automata import nfa
from queue import Queue


class NfaToDfaConverter:
    """Converts a nondeterminisitic finite automaton (NFA)
    into a deterministic one.
    The NFA must be free of empty transitions."""

    def __init__(self, nfa_automaton: nfa.Nfa):
        self.nfa: nfa.Nfa = nfa_automaton
        """The input automaton."""
        self.dfa: dfa.Dfa = dfa.Dfa()
        """The resulting automaton."""
        idx0 = self.dfa.add_state()
        self.queue: Queue = Queue()
        """Queue for controlling the processing order."""
        self.queue.put(idx0)
        start_states = frozenset(self.nfa.starts)
        self.state_represents: Dict[int, List[int]] = {
            idx0: list(start_states)}
        """Maps a state index of the DFA to a set of NFA state indices."""
        self.state_cache: Dict[FrozenSet[int], int] = {start_states: 0}
        """Maps a set of NFA state indices to a DFA state index."""

    def start_conversion(self) -> dfa.Dfa:
        while self.queue.qsize() > 0:
            self.perform_step(self.queue.get())
            self.queue.task_done()
        return self.dfa

    def perform_step(self, dfa_start_state_idx: int):
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

    def _collect_nfa_transitions(self, states: Iterable[int]) -> Tuple:
        symbol_transitions = defaultdict(set)
        non_word_char_transitions = set()
        accepts = set()
        for nfa_start_idx in states:
            for (
                symbol,
                nfa_end_state_idxs) in (
                    self.nfa.states[nfa_start_idx].symbol_transitions.items()):
                symbol_transitions[symbol].update(nfa_end_state_idxs)
            non_word_char_transitions.update(
                    self.nfa.states[nfa_start_idx].non_word_char_transitions)
            accepts.update(self.nfa.states[nfa_start_idx].accepts)
        return symbol_transitions, non_word_char_transitions, accepts

    def _create_dfa_transitions(
            self,
            dfa_start_state_idx: int,
            symbol_transitions: Dict[str, Set[int]],
            non_word_char_transitions: Set[int],
            accepts: Set[object]):
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

    def _get_or_create_dfa_state(self, state_idxs: Iterable[int]) -> int:
        """Retrieves a state index of the DFA representing a set of
        state indices in the NFA. If such a state does not exist,
        a new one will be created. The new State will also be added to
        the state lookup tables."""
        frozen_states = frozenset(state_idxs)
        try:
            dfa_state_idx = self.state_cache[frozen_states]
        except KeyError:
            dfa_state_idx = self.dfa.add_state()
            self.queue.put(dfa_state_idx)
            self.state_represents[dfa_state_idx] = list(frozen_states)
            self.state_cache[frozen_states] = dfa_state_idx
            acceptance: Set = set()
            for state_idx in state_idxs:
                acceptance.union(self.nfa.states[state_idx].accepts)
            dfa_state = self.dfa.states[dfa_state_idx]
            dfa_state.accepts = list(acceptance)

        return dfa_state_idx
