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


from stwfsapy.automata import nfa
from stwfsapy.automata import construction as c

from stwfsapy.tests.automata.data import accept

expression = 'test'


def test_init_with_empty_graph():
    graph = nfa.Nfa()
    construction = c.ConstructionState(graph, expression, accept)
    construction._set_up()
    assert len(graph.states) == 3
    assert graph.starts == []
    assert graph.states[0].non_word_char_transitions == {1}
    assert graph.states[1].empty_transitions == {2}
    assert construction.append_to == [2]
    assert construction.expression == expression
    assert construction.before_braces == [[1], [2]]
    assert construction.dangling_alternations.stack == []
    assert not construction.escape_next
    assert construction.accept == accept


def test_init_with_existing_graph(input_graph):
    construction = c.ConstructionState(input_graph, expression, accept)
    construction._set_up()
    assert len(input_graph.states) == 9
    assert input_graph.starts == [0, 1]
    assert input_graph.states[6].non_word_char_transitions == {7}
    assert input_graph.states[7].empty_transitions == {8}
    assert construction.append_to == [8]
    assert construction.expression == expression
    assert construction.before_braces == [[7], [8]]
    assert construction.dangling_alternations.stack == []
    assert not construction.escape_next
    assert construction.accept == accept


def test_adds_acceptance():
    graph = nfa.Nfa()
    construction = c.ConstructionState(graph, "a|b", accept)
    construction.construct()
    assert graph.starts == [0]
    assert graph.states[-1].accepts == [accept]
    assert graph.states[-2].accepts == [accept]
    assert graph.states[3].non_word_char_transitions == {7}
    assert graph.states[5].non_word_char_transitions == {6}
    assert graph.states[1].non_word_char_transitions == set()
    assert graph.states[1].empty_transitions == {2, 4}


def test_handles_multiple_alternations():
    graph = nfa.Nfa()
    construction = c.ConstructionState(graph, 'a|b|c', accept)
    construction.construct()
    assert graph.starts == [0]
    assert graph.states[-1].accepts == [accept]
    assert graph.states[-2].accepts == [accept]
    assert graph.states[-3].accepts == [accept]


def test_registers_escape():
    graph = nfa.Nfa()
    construction = c. ConstructionState(graph, '\\', accept)
    construction._set_up()
    construction._perform_step(0)
    assert graph.starts == []
    assert construction.escape_next


def test_handles_escaped_symbol(mocker):
    graph = nfa.Nfa()
    construction = c.ConstructionState(graph, '?', accept)
    construction._set_up()
    assert graph.starts == []
    construction.escape_next = True
    spy = mocker.spy(construction, "_process_symbol")
    construction._perform_step(0)
    spy.assert_called_once_with('?')


def test_handles_opening_brace(input_graph):
    append_to = [2, 4, 5]
    before_braces = [[0], [1, 3]]
    construction = c.ConstructionState(input_graph, '(', accept)
    construction._set_up()
    construction.append_to = append_to.copy()
    construction.before_braces = before_braces.copy()
    construction._perform_step(0)
    assert input_graph.starts == [0, 1]
    new_state_idx = len(input_graph.states) - 1
    assert construction.dangling_alternations.pop() == []
    assert construction.before_braces[:-2] == before_braces[:-1]
    assert construction.before_braces[-2] == append_to
    assert construction.before_braces[-1] == [new_state_idx]
    assert construction.append_to == [new_state_idx]
    for idx in append_to:
        assert new_state_idx in input_graph.states[idx].empty_transitions


def test_handles_closing_brace(input_graph, mocker):
    append_to = [2, 4, 5]
    old_append_len = len(append_to)
    before_braces = [[0], [1, 3]]
    ret = [12, 14]
    construction = c.ConstructionState(input_graph, ')', accept)
    construction._set_up()
    mocker.patch.object(
        construction.dangling_alternations,
        "pop",
        lambda: ret)
    construction.append_to = append_to.copy()
    construction.before_braces = before_braces.copy()
    construction._perform_step(0)
    assert input_graph.starts == [0, 1]
    assert construction.append_to[:old_append_len] == append_to
    assert construction.append_to[old_append_len:] == ret
    assert construction.before_braces == before_braces[:-1]


def test_handles_alternation(input_graph):
    append_to = [2, 4, 5]
    before_braces = [[0], [1, 3]]
    after_braces = [6, 7]
    construction = c.ConstructionState(input_graph, '|', accept)
    construction._set_up()
    construction.append_to = append_to.copy()
    construction.before_braces = before_braces.copy()
    construction.after_braces = after_braces.copy()
    construction._perform_step(0)
    assert input_graph.starts == [0, 1]
    assert construction.append_to == [len(construction.graph.states)-1]
    assert construction.dangling_alternations.stack[-1] == append_to


def test_handles_optional(input_graph):
    append_to = [2, 4, 5]
    before_braces = [[0], [1, 3]]
    after_braces = [6, 7]
    construction = c.ConstructionState(input_graph, '?', accept)
    construction._set_up()
    construction.append_to = append_to.copy()
    construction.before_braces = before_braces.copy()
    construction.after_braces = after_braces.copy()
    construction._perform_step(0)
    assert input_graph.starts == [0, 1]
    for idx in construction.append_to:
        for bb_idx in construction.before_braces[-1]:
            assert idx in input_graph.states[bb_idx].empty_transitions


def test_handles_kleene_closure(input_graph):
    append_to = [2, 4, 5]
    before_braces = [[0], [1, 3]]
    construction = c.ConstructionState(input_graph, '*', accept)
    construction._set_up()
    construction.append_to = append_to.copy()
    construction.before_braces = before_braces.copy()
    construction._perform_step(0)
    assert input_graph.starts == [0, 1]
    for idx in append_to:
        for bb_idx in construction.before_braces[-1]:
            assert bb_idx in input_graph.states[idx].empty_transitions
    for bb_idx in construction.before_braces[-1]:
        assert len(input_graph.states) - 1 in input_graph.states[
            bb_idx].empty_transitions
