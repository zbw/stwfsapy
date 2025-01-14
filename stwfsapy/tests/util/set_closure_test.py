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


from stwfsapy.util.set_closure import set_closure, RelationLoopException
from pytest import fixture, raises

_branching_k = 3
_depth = 5
_internal_nodes = sum(_branching_k**i for i in range(_depth))
_leafs = _branching_k ** _depth


@fixture
def tree_relation():
    return {
        i: {i * _branching_k + j for j in range(1, _branching_k+1)}
        for
        i
        in range(_internal_nodes)
    }


def _add_edge_to_tree_relation(relation, start, end, additionals=set()):
    relation[start].add(end)
    ret = additionals.copy()
    hlp_start = start
    # add all relations that should end up in the closure
    while hlp_start > 0:
        ret.add((hlp_start, end))
        hlp_start = (hlp_start-1) // _branching_k
    return relation, ret


@fixture
def single_diamond(tree_relation):
    diamond_top = _branching_k+1
    diamond_left = diamond_top*_branching_k+(_branching_k-1)
    diamond_right = diamond_top*_branching_k+_branching_k
    diamond_bottom = diamond_left*_branching_k+_branching_k
    return _add_edge_to_tree_relation(
        tree_relation,
        diamond_right,
        diamond_bottom)


@fixture
def double_diamond(single_diamond):
    tree_relation, additionals = single_diamond
    diamond_top = 1
    diamond_left = diamond_top*_branching_k+(_branching_k-1)
    diamond_right = diamond_top*_branching_k+_branching_k
    diamond_bottom = diamond_left*_branching_k+_branching_k
    tree_relation[diamond_right].add(diamond_bottom)
    additionals.add((diamond_right, diamond_bottom))
    return _add_edge_to_tree_relation(
        tree_relation,
        diamond_right,
        diamond_bottom,
        additionals)


@fixture
def double_diamond_reflexive(double_diamond):
    tree_relation, additionals = double_diamond
    for n in tree_relation:
        tree_relation, additionals = _add_edge_to_tree_relation(
            tree_relation,
            n,
            n,
            additionals
        )
    return tree_relation, additionals


def check_closure_edge(closures, start, end):
    hlp_start = start
    while hlp_start > 0:
        assert end in closures[hlp_start]
        hlp_start = (hlp_start-1) // _branching_k
    assert end in closures[0]


def check_tree_closure(closures, additional_relations={}):
    totals = _internal_nodes+_leafs
    assert len(closures) == totals
    for start in range(_internal_nodes):
        for end in range(1, _branching_k+1):
            check_closure_edge(closures, start, start*_branching_k + end)
    for start in range(totals):
        for end in closures[start]:
            ancestor = (end-1) // _branching_k
            assert ancestor == start or (
                ancestor in closures[start]) or (
                (start, end) in additional_relations) or (
                    end == start)


def test_closure_of_tree(tree_relation):
    closures = set_closure(tree_relation)
    check_tree_closure(closures)


def test_closure_diamond(single_diamond):
    p_order, additionals = single_diamond
    closures = set_closure(p_order)
    check_tree_closure(closures, additionals)


def test_closure_double_diamond(double_diamond):
    p_order, additionals = double_diamond
    closures = set_closure(p_order)
    check_tree_closure(closures, additionals)


def test_closure_double_diamond_reflexive(double_diamond_reflexive):
    p_order, additionals = double_diamond_reflexive
    closures = set_closure(p_order)
    check_tree_closure(closures, additionals)
    for n in p_order:
        assert n in closures[n]


def test_exception_on_cycle(tree_relation):
    tree_relation[_internal_nodes-2].add(_branching_k)
    with raises(RelationLoopException):
        set_closure(tree_relation)


def test_no_exception_on_non_cycle_backedge(tree_relation):
    tree_relation, additionals = _add_edge_to_tree_relation(
        tree_relation,
        _internal_nodes-2,
        1)
    closures = set_closure(tree_relation)
    check_tree_closure(closures, additionals)
