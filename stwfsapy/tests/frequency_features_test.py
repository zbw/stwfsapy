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


from stwfsapy.frequency_features import FrequencyFeatures
from stwfsapy.tests.common import doc_feature_data
from sklearn.exceptions import NotFittedError
import numpy as np
from math import log

import pytest


def test_handle_empty():
    features = FrequencyFeatures()
    features.fit([])
    assert features.transform([]).tolist() == np.zeros((0, 3)).tolist()


def test_fit():
    features = FrequencyFeatures()
    features.fit(doc_feature_data)
    keyset = {'cncpt_1', 'cncpt_2', 'cncpt_3'}
    assert set(features.idfs_.keys()) == keyset
    assert features.idfs_['cncpt_1'] == 0
    assert features.idfs_['cncpt_2'] == 0
    assert features.idfs_['cncpt_3'] == log(3/2)
    assert features.idfs_['unknown_concept'] == log(3)


def test_not_fitted():
    features = FrequencyFeatures()
    with pytest.raises(NotFittedError):
        features.transform([])


def test_transform():
    features = FrequencyFeatures()
    features.fit(doc_feature_data)
    data = [
        ('cncpt_2', 'b'*3, [2, 5], 0),
        ('cncpt_3', 'b'*8, [17, 11, 22], 1),
        ('cncpt_1', 'b'*17, [13, 2, 1, 9, 8], 0),
        ('cncpt_3', 'b'*2, [6], 0),
        ('unknown', 'b'*9, [4, 3, 26, 39, 7], 1)
    ]
    transformed = features.transform(
        data
    )
    assert transformed.tolist() == [
        [2/5, 0, 0],
        [3/5, log(3/2), 3/5*log(3/2)],
        [5/11, 0, 0],
        [1/11, log(3/2), 1/11 * log(3/2)],
        [5/11, log(3), 5/11 * log(3)]
    ]
