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


from typing import List, Dict, Iterable
import array


class State:

    def __init__(self):
        self.symbol_transitions: Dict[str, int] = dict()
        self.non_word_char_transition: State
        self.accepts: array.array = []

    def set_symbol_transition(self, symbol: str, idx: int):
        self.symbol_transitions[symbol] = idx

    def set_non_word_char_transition(self, idx: int):
        self.non_word_char_transition = idx

    def add_acceptances(self, accepts: Iterable):
        self.accepts.extend(accepts)


class Dfa:

    def __init__(self):
        self.states: List[State] = []

    def add_state(self)-> int:
        idx = len(self.states)
        state = State()
        self.states.append(state)
        return idx

    def add_acceptances(self, idx: int, accepts: Iterable):
        self.states[idx].add_acceptances(accepts)

    def set_symbol_transition(self, start_idx: int, end_idx: int, symbol: str):
        self.states[start_idx].set_symbol_transition(symbol, end_idx)

    def set_non_word_char_transition(self, start_idx: int, end_idx: int):
        self.states[start_idx].set_non_word_char_transition(end_idx)

    def search(self, text):
        for start in range(len(text)):
            stack = [(0, start)]
            while len(stack) > 0:
                state_idx, position = stack.pop()
                state = self.states[state_idx]
                for accept in state.accepts:
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
