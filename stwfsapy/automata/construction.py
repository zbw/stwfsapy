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


from typing import List
from stwfsapy.automata import nfa


class ConstructionState:

    def __init__(self, graph: nfa.Nfa, expression: str, accept):
        self.graph = graph
        self.expression = expression
        self.accept = accept

    def _set_up(self):
        start = self.graph.add_state()
        self.expression_start = self.graph.add_state()
        self.graph.add_start(start)
        self.graph.add_non_word_char_transition(
            start,
            self.expression_start)
        self.append_to = [self.expression_start]
        self.before_braces = [[self.expression_start]]
        self.after_braces = [self.expression_start]
        self.dangling_alternations = _AlternationManager(self.expression_start)
        self.escape_next = False

    def construct(self):
        self._set_up()
        for i in range(len(self.expression)):
            self._perform_step(i)
        ends = self.append_to
        danglings = self.dangling_alternations.pop()
        if danglings != [self.expression_start]:
            ends.extend(danglings)
        for end_idx in ends:
            acceptance_idx = self.graph.add_state()
            self.graph.add_acceptance(acceptance_idx, self.accept)
            self.graph.add_non_word_char_transition(end_idx, acceptance_idx)

    def _perform_step(self, idx: int):
        symbol = self.expression[idx]
        if self.escape_next:
            self.escape_next = False
            self._process_symbol(symbol)
        elif symbol == "(":
            self._process_opening_brace()
        elif symbol == ")":
            self._process_closing_brace()
        elif symbol == "?":
            self._process_optional()
        elif symbol == "*":
            self._process_kleene_closure()
        elif symbol == "\\":
            self.escape_next = True
        elif symbol == "|":
            self._process_alternation()
        else:
            self._process_symbol(symbol)

    def _process_symbol(self, symbol):
        new_state_idx = self.graph.add_state()
        for state_idx in self.append_to:
            self.graph.add_symbol_transition(state_idx, new_state_idx, symbol)
        self.before_braces[-1] = self.append_to
        self.append_to = [new_state_idx]

    def _process_opening_brace(self):
        new_state_idx = self.graph.add_state()
        for state_idx in self.append_to:
            self.graph.add_empty_transition(state_idx, new_state_idx)
        tmp = self.before_braces.pop()
        self.after_braces.append(new_state_idx)
        self.dangling_alternations.push_empty()
        for state_idx in self.append_to:
            self.before_braces.append([state_idx])
        self.before_braces.append(tmp)
        self.append_to = [new_state_idx]

    def _process_alternation(self):
        self.dangling_alternations.push(self.append_to)
        self.append_to = [self.after_braces[-1]]

    def _process_closing_brace(self):
        danglings = self.dangling_alternations.pop()
        self.append_to.extend(danglings)
        self.before_braces.pop()
        self.after_braces.pop()

    def _process_optional(self):
        before_idxs = self.before_braces[-1]
        for before_idx in before_idxs:
            for state_idx in self.append_to:
                self.graph.add_empty_transition(before_idx, state_idx)

    def _process_kleene_closure(self):
        before_idxs = self.before_braces[-1]
        for before_idx in before_idxs:
            for state_idx in self.append_to:
                self.graph.add_empty_transition(state_idx, before_idx)


class _AlternationManager():

    def __init__(self, start: int):
        self.stack = []

    def pop(self) -> [int]:
        return self.stack.pop()

    def push(self, states: List[int]):
        try:
            self.stack[-1].extend(states)
        except IndexError:
            self.stack.append(states)

    def push_empty(self):
        self.stack.append([])
