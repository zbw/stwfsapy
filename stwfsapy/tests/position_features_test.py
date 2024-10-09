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


from stwfsapy.position_features import PositionFeatures
import numpy as np


position_feature_data = [
    (3, [3, 4, 0, 2]),
    (6, [1, 8, 23, 12]),
    (15, [12, 36, 25, 7]),
    (12, [8, 102, 17, 9, 20]),
    (70, [13]),
]


def test_handle_empty():
    features = PositionFeatures()
    assert features.transform([]).tolist() == np.zeros((0, 3)).tolist()


def test_convert_docs():
    features = PositionFeatures()
    res = features.transform(position_feature_data)
    assert res.tolist() == [
        [0/3, 4/3, 4/3],
        [1/6, 23/6, 22/6],
        [7/15, 36/15, 29/15],
        [8/12, 102/12, 94/12],
        [13/70, 13/70, 0]]
