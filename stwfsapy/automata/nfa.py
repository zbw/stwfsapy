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
from typing import Set, List, Any, DefaultDict
from stwfsapy.automata.heap import BinaryMinHeap


class State:

    def __init__(self):
        self.symbol_transitions: DefaultDict[str, Set[int]] = defaultdict(set)
        """Determines the states that can be reached
        by consuming a character."""
        self.non_word_char_transitions: Set[int] = set()
        """Is not None if there is a transition via a non word symbol."""
        self.empty_transitions: Set[int] = set()
        """What can be reached using the empty String/Symbol."""
        self.incoming_empty_transitions: Set[int] = set()
        """How this state can be reached using the empty String/Symbol."""
        self.accepts: List[Any] = []
        """What is accepted by this State."""


class Nfa:

    def __init__(self):
        self.states: List[State] = []
        """All states of the NFA's graph"""
        self.starts: List[int] = []
        """All start states."""

    def add_state(self) -> int:
        """Creates a new state and returns its index."""
        idx = len(self.states)
        self.states.append(State())
        return idx

    def add_start(self, idx: int):
        """Adds a state, by index to the list of possible start states."""
        self.starts.append(idx)

    def add_acceptance(self, idx, accept):
        """Add acceptance to a state. The state is identified by its index."""
        self.states[idx].accepts.append(accept)

    def add_symbol_transition(self, start: int, end: int, symbol: str):
        """Add a symbol consuming transition between two states.
        The states are represented by their indices."""
        transitions = self.states[start].symbol_transitions
        transitions[symbol].add(end)

    def add_empty_transition(self, start: int, end: int):
        """Add an empty Transition between two states.
        This transition does not consume a symbol.
        The states are represented by their indices."""
        self.states[start].empty_transitions.add(end)
        self.states[end].incoming_empty_transitions.add(start)

    def add_non_word_char_transition(self, start: int, end: int):
        """Add a non word char consuming transition between two states.
        The states are represented by their indices."""
        self.states[start].non_word_char_transitions.add(end)

    def remove_empty_transitions(self):
        """Removes all empty transitions in the NFA.
        Does not support loops of empty transitions."""
        queue = BinaryMinHeap()
        for idx in range(len(self.states)):
            if len(self.states[idx].incoming_empty_transitions) > 0:
                queue.push(idx, len(self.states[idx].empty_transitions))
        while len(queue.heap) > 0:
            ptr_idx = queue.pop()
            ptr = self.states[ptr_idx]
            if len(ptr.empty_transitions) > 0:
                raise Exception(
                    "There is an empty transition loop in the NFA.")
            for incoming_idx in ptr.incoming_empty_transitions.copy():
                incoming = self.states[incoming_idx]
                self._remove_empty_transition(
                    incoming_idx,
                    incoming,
                    ptr_idx,
                    ptr)
                if len(incoming.incoming_empty_transitions) > 0:
                    queue.change_priority(
                        incoming_idx,
                        len(incoming.empty_transitions))

    def _remove_empty_transition(
            self,
            start_idx: int,
            start: State,
            end_idx: int,
            end: State):
        for symbol, states in end.symbol_transitions.items():
            for state_idx in states:
                start.symbol_transitions[symbol].add(state_idx)
        for state_idx in end.non_word_char_transitions:
            start.non_word_char_transitions.add(state_idx)
        start.empty_transitions.discard(end_idx)
        end.incoming_empty_transitions.discard(start_idx)
