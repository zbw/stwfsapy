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


from typing import Set, Dict, Hashable, Tuple, List


def set_closure(
        sets: Dict[Hashable, Set[Hashable]]
        ) -> Dict[Hashable, Set[Hashable]]:
    """Computes the closure for each element of a antisymmetric relation.
    The relation is given by a mapping from elements
    to a set of related elements.
    Raises a RelationLoopException if the relation has circles."""
    closure: Dict[Hashable, Set[Hashable]] = dict()
    for key in sets:
        stack: List[Tuple[Hashable, Set[Hashable]]] = [(key, set())]
        while len(stack) > 0:
            top = stack[-1]
            current = top[0]
            ancestors = top[1]
            if current in closure:
                stack.pop()
            else:
                if current not in sets:
                    stack.pop()
                    closure[current] = set()
                else:
                    all_known = True
                    for child in sets[current]:
                        if child not in closure and child != current:
                            if child in ancestors:
                                raise RelationLoopException()
                            all_known = False
                            new_ancestors = ancestors.copy()
                            new_ancestors.add(current)
                            stack.append((child, new_ancestors))
                    if all_known:
                        element_closure = set()
                        for child in sets[current]:
                            element_closure.add(child)
                            try:
                                for closure_object in closure[child]:
                                    element_closure.add(closure_object)
                            except KeyError:
                                pass
                        closure[current] = element_closure
                        stack.pop()
    return closure


class RelationLoopException(Exception):
    pass
