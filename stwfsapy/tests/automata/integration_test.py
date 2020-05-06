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

    res = list(dfa_graph.search(' a '))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search(' b '))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search(' c '))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search(' d '))
    assert len(res) == 0


def test_alternation_center_kleene():
    graph = nfa.Nfa()
    construction = const.ConstructionState(graph, 'a|b*|c', accept)
    construction.construct()
    graph.remove_empty_transitions()
    dfa_graph = conv.NfaToDfaConverter(graph).start_conversion()

    res = list(dfa_graph.search(' bbbbb '))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search(' a '))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search(' c '))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search(' aa '))
    assert len(res) == 0
    res = list(dfa_graph.search(' cc '))
    assert len(res) == 0
    res = list(dfa_graph.search(' ba '))
    assert len(res) == 0


def test_alternation_left_kleene():
    graph = nfa.Nfa()
    construction = const.ConstructionState(graph, 'a*|b|c', accept)
    construction.construct()
    graph.remove_empty_transitions()
    dfa_graph = conv.NfaToDfaConverter(graph).start_conversion()

    res = list(dfa_graph.search(' aaaaa '))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search(' c '))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search(' b '))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search(' bb '))
    assert len(res) == 0
    res = list(dfa_graph.search(' cc '))
    assert len(res) == 0
    res = list(dfa_graph.search(' ac '))
    assert len(res) == 0


def test_alternation_right_kleene():
    graph = nfa.Nfa()
    construction = const.ConstructionState(graph, 'a|b|c*', accept)
    construction.construct()
    graph.remove_empty_transitions()
    dfa_graph = conv.NfaToDfaConverter(graph).start_conversion()

    res = list(dfa_graph.search(' ccccc '))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search(' a '))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search(' b '))
    assert len(res) == 1
    assert res[0][0] == accept
    res = list(dfa_graph.search(' bb '))
    assert len(res) == 0
    res = list(dfa_graph.search(' aa '))
    assert len(res) == 0
    res = list(dfa_graph.search(' ca '))
    assert len(res) == 0
