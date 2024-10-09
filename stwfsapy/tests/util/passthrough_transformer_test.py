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

from stwfsapy.util.passthrough_transformer import PassthroughTransformer
import numpy as np
import scipy.sparse as sp


def test_array_input():
    in_feat = [
        np.array([1, 0, 0]),
        np.array([0, 7, 0]),
        np.array([0, 0, -3])
    ]
    pt = PassthroughTransformer()
    out_feat = pt.transform(in_feat)
    assert isinstance(out_feat, np.ndarray)
    assert (sp.diags([[1, 7, -3]], [0]).toarray() == out_feat).all()


def test_sparse_input():
    in_feat = [
        sp.lil_matrix(np.array([[1, 0, 0]])),
        sp.lil_matrix(np.array([[0, 7, 0]])),
        sp.lil_matrix(np.array([[0, 0, -3]]))
    ]
    pt = PassthroughTransformer()
    out_feat = pt.transform(in_feat)
    assert sp.issparse(out_feat)
    assert (sp.diags([[1, 7, -3]], [0]).toarray() == out_feat.toarray()).all()
