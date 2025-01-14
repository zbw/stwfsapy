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


from stwfsapy.expansion import simple_english_plural_fun


def test_trailing_non_alpha():
    label = 'fo0'
    assert simple_english_plural_fun(label) == label


def test_trailing_s():
    label = 'bas'
    assert simple_english_plural_fun(label) == label


def test_default_endingn():
    label = 'bar'
    assert simple_english_plural_fun(label) == 'bars?'


def test_trailing_y():
    label = 'daily'
    prefix_idx = len(label)-1
    res = simple_english_plural_fun(label)
    assert len(res) == len(label) + 6
    assert label[:prefix_idx] == res[:prefix_idx]
    assert res[prefix_idx:] == '(y|ies)'
