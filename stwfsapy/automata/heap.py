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


from typing import List, Dict, Tuple, Any, SupportsFloat


class BinaryMinHeap:
    """Can be used as a priority queue.
    Allows changing priorities."""

    def __init__(self):
        self.heap: List[Tuple[SupportsFloat, Any]] = []
        """The actual heap structure."""
        self.mapping: Dict[Any, int] = dict()
        """Maps objects to positions in the heap."""

    def push(self, val, priority):
        idx = len(self.heap)
        self.heap.append((priority, val))
        self.mapping[val] = idx
        self._sift_up(idx)

    def pop(self):
        head = self.heap[0][1]
        self.mapping.pop(head)
        tmp_head = self.heap.pop()
        if len(self.heap) > 0:
            self.heap[0] = tmp_head
            self.mapping[tmp_head[1]] = 0
            self._sift_down(0)
        return head

    def change_priority(self, val, priority):
        idx = self.mapping[val]
        old_priority = self.heap[idx][0]
        if old_priority == priority:
            return
        self.heap[idx] = (priority, val)
        if priority < old_priority:
            self._sift_up(idx)
        else:
            self._sift_down(idx)

    def _sift_up(self, idx):
        ptr_idx = idx
        ptr = self.heap[ptr_idx]
        while ptr_idx > 0:
            parent_idx = _parent_index(ptr_idx)
            parent = self.heap[parent_idx]
            if ptr[0] < parent[0]:
                self.heap[parent_idx] = ptr
                self.mapping[ptr[1]] = parent_idx
                self.heap[ptr_idx] = parent
                self.mapping[parent[1]] = ptr_idx
                ptr_idx = parent_idx
            else:
                return

    def _sift_down(self, idx):
        ptr_idx = idx
        ptr = self.heap[ptr_idx]
        while True:
            child_idx = _lchild_index(ptr_idx)
            if child_idx >= len(self.heap):
                return
            child = self.heap[child_idx]
            rchild_idx = _rchild_index(ptr_idx)
            if rchild_idx < len(self.heap):
                rchild = self.heap[rchild_idx]
                if rchild[0] < child[0]:
                    child_idx = rchild_idx
                    child = rchild
            if ptr[0] <= child[0]:
                return
            self.heap[child_idx] = ptr
            self.heap[ptr_idx] = child
            self.mapping[child[1]] = ptr_idx
            self.mapping[ptr[1]] = child_idx
            ptr_idx = child_idx


def _parent_index(idx: int):
    return (idx-1) // 2


def _lchild_index(idx: int):
    return 2*idx+1


def _rchild_index(idx: int):
    return 2*idx+2
