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


from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np


class PositionFeatures(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        out = np.zeros((len(X), 3))
        for idx, x in enumerate(X):
            positions = x[1]
            min_pos = min(positions)
            max_pos = max(positions)
            spread = max_pos - min_pos
            txt_len = x[0]
            out[idx][0] = min_pos / txt_len
            out[idx][1] = max_pos / txt_len
            out[idx][2] = spread / txt_len
        return out
