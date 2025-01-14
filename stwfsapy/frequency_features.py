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


from collections import defaultdict, OrderedDict
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.exceptions import NotFittedError
from math import log
import numpy as np


class FrequencyFeatures(BaseEstimator, TransformerMixin):

    def __init__(self):
        self.idfs_ = None
        self.log_doc_count_ = None

    def fit(self, X, y=None):
        concept_counts = defaultdict(int)
        concepts = []
        # count one doc more to cover case where a concept does not appear.
        doc_count = 1
        for x in X:
            concepts.append(x[0])
            if x[-1] == 1:
                for concept in concepts:
                    concept_counts[concept] += 1
                doc_count += 1
                concepts = []
        self.log_doc_count_ = log(doc_count)
        idfs = dict()
        for concept, count in concept_counts.items():
            idfs[concept] = log(doc_count/(count+1))
        self.idfs_ = idfs
        return self

    def transform(self, X, y=None):
        if self.idfs_ is None:
            raise NotFittedError
        ret = np.zeros((len(X), 3))
        concept_counts = OrderedDict()
        ret_ptr = 0
        doc_concept_sum = 0
        for x in X:
            concept = x[0]
            concept_count = len(x[1])
            concept_counts[concept] = concept_count
            doc_concept_sum += concept_count
            if x[-1] == 1:
                for concept, count in concept_counts.items():
                    tf = count/doc_concept_sum
                    idf = self.idfs_.get(concept, self.log_doc_count_)
                    ret[ret_ptr, 0] = tf
                    ret[ret_ptr, 1] = idf
                    ret[ret_ptr, 2] = tf*idf
                    ret_ptr += 1
                doc_concept_sum = 0
                concept_counts = OrderedDict()
        return ret
