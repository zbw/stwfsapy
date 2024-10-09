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


symbol0 = 's'
symbol1 = 't'
accept = "Acceptance!"


@pytest.fixture
def input_graph():
    graph = nfa.Nfa()
    for _ in range(6):
        graph.add_state()
    graph.add_start(0)
    graph.add_start(1)
    graph.add_symbol_transition(0, 2, symbol0)
    graph.add_symbol_transition(1, 0, symbol0)
    graph.add_symbol_transition(0, 3, symbol1)
    graph.add_symbol_transition(1, 3, symbol1)
    graph.add_symbol_transition(2, 4, symbol0)
    graph.add_symbol_transition(4, 5, symbol1)
    graph.add_non_word_char_transition(1, 5)
    graph.add_acceptance(5, accept)
    return graph
