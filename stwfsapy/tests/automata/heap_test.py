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


from stwfsapy.automata import heap
import pytest


def check_heap(queue):
    for i in range(1, len(queue.heap)):
        assert queue.heap[i][0] >= queue.heap[heap._parent_index(i)][0]
    for key in queue.mapping:
        assert key == queue.heap[queue.mapping[key]][1]


@pytest.fixture
def some_heap():
    queue = heap.BinaryMinHeap()
    for i in range(12):
        key = 2 * i
        val = 3 * i
        queue.heap.append((key, val))
        queue.mapping[val] = i
    return queue


def test_sift_up(some_heap):
    check_heap(some_heap)
    idx = 7
    old_key, old_val = some_heap.heap[idx]
    some_heap.heap[idx] = (0, old_val)
    some_heap._sift_up(idx)
    check_heap(some_heap)
    assert some_heap.heap[0] == (0, 0)
    assert some_heap.heap[1] == (0, old_val)


def test_sift_down(some_heap):
    idx = 1
    old_key, old_val = some_heap.heap[idx]
    some_heap.heap[idx] = (17, old_val)
    some_heap._sift_down(idx)
    check_heap(some_heap)
    assert some_heap.heap[7] == (17, old_val)


def test_sift_down_already_correct(some_heap):
    idx = 1
    old_key, old_val = some_heap.heap[1]
    some_heap._sift_down(idx)
    check_heap(some_heap)
    assert some_heap.heap[1] == (old_key, old_val)


def test_parent_idx():
    for i in range(200):
        assert heap._parent_index(heap._lchild_index(i)) == i
        assert heap._parent_index(heap._rchild_index(i)) == i


def test_push_empty():
    queue = heap.BinaryMinHeap()
    queue.push(5, 0)
    assert len(queue.heap) == 1
    assert len(queue.mapping) == 1
    assert queue.heap[0] == (0, 5)
    assert queue.mapping[5] == 0


def test_push(some_heap, mocker):
    spy = mocker.spy(some_heap, "_sift_up")
    some_heap.push(15, 13)
    spy.assert_called_once_with(len(some_heap.heap)-1)


def test_pop_(some_heap, mocker):
    spy = mocker.spy(some_heap, "_sift_down")
    head = some_heap.pop()
    assert head == 0
    spy.assert_called_once_with(0)
    check_heap(some_heap)


def test_pop_empty():
    empty = heap.BinaryMinHeap()
    with pytest.raises(IndexError):
        empty.pop()


def test_can_increase_key(some_heap, mocker):
    spy_down = mocker.spy(some_heap, "_sift_down")
    spy_up = mocker.spy(some_heap, "_sift_up")
    top = some_heap.heap[0]
    some_heap.change_priority(top[1], 256)
    check_heap(some_heap)
    spy_down.assert_called_once_with(0)
    spy_up.assert_not_called()


def test_can_decrease_key(some_heap, mocker):
    spy_down = mocker.spy(some_heap, "_sift_down")
    spy_up = mocker.spy(some_heap, "_sift_up")
    last = some_heap.heap[-1]
    some_heap.change_priority(last[1], 0)
    check_heap(some_heap)
    spy_up.assert_called_once_with(len(some_heap.heap)-1)
    spy_down.assert_not_called()


def test_can_set_equal_key(some_heap, mocker):
    spy_down = mocker.spy(some_heap, "_sift_down")
    spy_up = mocker.spy(some_heap, "_sift_up")
    middle = some_heap.heap[5]
    some_heap.change_priority(middle[1], middle[0])
    spy_up.assert_not_called()
    spy_down.assert_not_called()
