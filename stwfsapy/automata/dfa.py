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


from typing import List, Dict, Iterable, Tuple, Any


class State:

    def __init__(self):
        self.symbol_transitions: Dict[str, int] = dict()
        """Transitions consuming a symbol."""
        self.non_word_char_transition: int
        """Transition consuming a non word character symbol."""
        self.accepts: List[Any] = []
        """What is accepted by this state."""

    def set_symbol_transition(self, symbol: str, idx: int):
        self.symbol_transitions[symbol] = idx

    def set_non_word_char_transition(self, idx: int):
        self.non_word_char_transition = idx

    def add_acceptances(self, accepts: Iterable):
        self.accepts.extend(accepts)


class Dfa:

    def __init__(self):
        self.states: List[State] = []
        """All the states of this Automaton."""

    def add_state(self) -> int:
        """Creates a new state and returns its index."""
        idx = len(self.states)
        state = State()
        self.states.append(state)
        return idx

    def add_acceptances(self, idx: int, accepts: Iterable):
        """Adds new acceptances to a state.
        The state is given by its index."""
        self.states[idx].add_acceptances(accepts)

    def set_symbol_transition(self, start_idx: int, end_idx: int, symbol: str):
        """Add a new symbol consuming transition between to states.
        The states are given by their index."""
        self.states[start_idx].set_symbol_transition(symbol, end_idx)

    def set_non_word_char_transition(self, start_idx: int, end_idx: int):
        """Add a new non word char consuming transition between two states.
        The states are given by their index."""
        self.states[start_idx].set_non_word_char_transition(end_idx)

    def search(self, text: str) -> Iterable[Tuple[Any, str, int, int]]:
        """ Process a string, yielding acceptances of all substrings."""
        for start in range(len(text)):
            stack = [(0, start)]
            while len(stack) > 0:
                state_idx, position = stack.pop()
                state = self.states[state_idx]
                for accept in state.accepts:
                    # subtract one from position,
                    # as the match is without consuming the next symbol
                    yield (accept, text, start, position-1)
                try:
                    symbol = text[position]
                except IndexError:
                    continue
                try:
                    transition = state.symbol_transitions[text[position]]
                    stack.append((transition, position+1))
                except KeyError:
                    pass
                if not symbol.isalpha():
                    try:
                        stack.append(
                            (state.non_word_char_transition, position+1))
                    except AttributeError:
                        pass
