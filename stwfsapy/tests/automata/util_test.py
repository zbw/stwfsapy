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


from stwfsapy.automata import util

key = 'a'


def test_can_add_to_existing_set():
    mapping = {key: {1, 2, 3}}
    util.safe_set_add_in_dict(mapping, key, 4)
    assert len(mapping) == 1
    assert mapping[key] == {1, 2, 3, 4}


def test_add_creates_new_set():
    mapping = dict()
    util.safe_set_add_in_dict(mapping, key, 4)
    assert len(mapping) == 1
    assert mapping[key] == {4}


def test_can_update_existing_set():
    mapping = {key: {1, 2, 3}}
    util.safe_set_update_in_dict(mapping, key, {3, 4, 5})
    assert len(mapping) == 1
    assert mapping[key] == {1, 2, 3, 4, 5}


def test_update_creates_new_set():
    mapping = dict()
    util.safe_set_update_in_dict(mapping, key, {3, 4, 5})
    assert len(mapping) == 1
    assert mapping[key] == {3, 4, 5}
