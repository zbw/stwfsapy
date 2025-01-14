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

import scipy.sparse as sp
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class PassthroughTransformer(BaseEstimator, TransformerMixin):
    ''' Helper Class to better handle array input for ColumnTransformer.'''

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        if sp.issparse(X[0]):
            ret = sp.vstack(X, format='csr')
        else:
            ret = np.vstack(X)
        return ret
