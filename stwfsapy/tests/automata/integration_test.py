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


from stwfsapy.automata import nfa
from stwfsapy.automata import construction as const
from stwfsapy.automata import conversion as conv
from stwfsapy.tests.automata.data import accept


def test_alternation():
    graph = nfa.Nfa()
    construction = const.ConstructionState(graph, 'a|b|c', accept)
    construction.construct()
    graph.remove_empty_transitions()
    dfa_graph = conv.NfaToDfaConverter(graph).start_conversion()

    res = list(dfa_graph.search('a'))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search('b'))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search('c'))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search('d'))
    assert len(res) == 0


def test_alternation_center_kleene():
    graph = nfa.Nfa()
    construction = const.ConstructionState(graph, 'a|b*|c', accept)
    construction.construct()
    graph.remove_empty_transitions()
    dfa_graph = conv.NfaToDfaConverter(graph).start_conversion()

    res = list(dfa_graph.search(''))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search('bbbbb'))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search('a'))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search('c'))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search('aa'))
    assert len(res) == 0
    res = list(dfa_graph.search('cc'))
    assert len(res) == 0
    res = list(dfa_graph.search('ba'))
    assert len(res) == 0


def test_alternation_left_kleene():
    graph = nfa.Nfa()
    construction = const.ConstructionState(graph, 'a*|b|c', accept)
    construction.construct()
    graph.remove_empty_transitions()
    dfa_graph = conv.NfaToDfaConverter(graph).start_conversion()

    res = list(dfa_graph.search(''))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search('aaaaa'))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search('c'))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search('b'))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search('bb'))
    assert len(res) == 0
    res = list(dfa_graph.search('cc'))
    assert len(res) == 0
    res = list(dfa_graph.search('ac'))
    assert len(res) == 0


def test_alternation_right_kleene():
    graph = nfa.Nfa()
    construction = const.ConstructionState(graph, 'a|b|c*', accept)
    construction.construct()
    graph.remove_empty_transitions()
    dfa_graph = conv.NfaToDfaConverter(graph).start_conversion()

    res = list(dfa_graph.search(''))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search('ccccc'))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search('a'))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search('b'))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search('bb'))
    assert len(res) == 0
    res = list(dfa_graph.search('aa'))
    assert len(res) == 0
    res = list(dfa_graph.search('ca'))
    assert len(res) == 0
