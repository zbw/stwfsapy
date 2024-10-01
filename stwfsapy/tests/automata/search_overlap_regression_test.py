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

""" The tests in this file compare the behaviors of
stwfsapy and zaptain-stwfsa regarding overlap of potential matches."""
from stwfsapy.automata import nfa
import stwfsapy.automata.construction as const
import stwfsapy.automata.conversion as conv
import pytest


label_global = 'global'
id_global = 'id_global'
label_economic = 'economic'
id_economic = 'id_economic'
label_crisis = 'crisis'
id_crisis = 'id_crisis'
label_global_economic = 'global economic'
id_global_economic = 'id_global_economic'
label_economic_crisis = 'economic crisis'
id_economic_crisis = 'id_economic_crisis'
label_global_economic_crisis = 'global economic crisis'
id_global_economic_crisis = 'id_global_economic_crisis'


@pytest.fixture
def regression_test_graph():
    automaton = nfa.Nfa()
    concept_tuples = [
        (label_global, id_global),
        (label_economic, id_economic),
        (label_crisis, id_crisis),
        (label_global_economic, id_global_economic),
        (label_economic_crisis, id_economic_crisis),
        (label_global_economic_crisis, id_global_economic_crisis),
    ]
    for label, concept_id in concept_tuples:
        const.ConstructionState(automaton, label, concept_id).construct()
    automaton.remove_empty_transitions()
    dfa = conv.NfaToDfaConverter(automaton).start_conversion()
    return dfa


def test_regression_0(regression_test_graph):
    phrase = "global economic crisis unfolds"
    res = list(regression_test_graph.search(phrase))
    assert res == [
        (id_global_economic_crisis, label_global_economic_crisis, 0, 22)
    ]


def test_regression_1(regression_test_graph):
    phrase = "bank collapse threatens global economic system"
    res = list(regression_test_graph.search(phrase))
    assert res == [
        (id_global_economic, label_global_economic, 24, 39)
    ]


def test_regression_2(regression_test_graph):
    phrase = "regulatory bodies react to economic crisis"
    res = list(regression_test_graph.search(phrase))
    assert res == [
        (id_economic_crisis, label_economic_crisis, 27, 42)
    ]


def test_regression_3(regression_test_graph):
    phrase = "global trends in economic policy during the crisis"
    res = list(regression_test_graph.search(phrase))
    assert res == [
        (id_global, label_global, 0, 6),
        (id_economic, label_economic, 17, 25),
        (id_crisis, label_crisis, 44, 50),
    ]
