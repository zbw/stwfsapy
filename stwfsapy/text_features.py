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


from enum import Enum
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import FeatureUnion
from sklearn.exceptions import NotFittedError
import numpy as np
import re


_NAME_VECTOR_FEATURE = "vectorizer"
_NAME_CHAR_FEATURE = "n_chars"
_NAME_WORD_FEATURE = "n_words"
_NAME_SPECIAL_CHARS_FEATURE = "n_special"
_NAME_UPPER_FEATURE = "n_upper"
_NAME_DIGIT_FEATURE = "n_digits"


def mk_text_features():
    return FeatureUnion([
        (_NAME_VECTOR_FEATURE, CountVectorizer(lowercase=False)),
        (_NAME_CHAR_FEATURE, CountFeature(CountType.N_CHAR)),
        (_NAME_WORD_FEATURE, CountFeature(CountType.N_WORD)),
        (_NAME_SPECIAL_CHARS_FEATURE, CountFeature(CountType.N_SPECIAL)),
        (_NAME_UPPER_FEATURE, CountFeature(CountType.N_UPPER)),
        (_NAME_DIGIT_FEATURE, CountFeature(CountType.N_DIGIT)),
    ])


class CountType(Enum):
    N_CHAR = 0
    N_WORD = 1
    N_SPECIAL = 2
    N_UPPER = 3
    N_DIGIT = 4


class CountFeature(BaseEstimator, TransformerMixin):
    def __init__(self, ctype: CountType):
        self.ctype = ctype
        self.function_ = None

    def fit(self, X, y=None):
        self.function_ = self.fun_from_type(self.ctype)
        return self

    def transform(self, X):
        if not self.function_:
            raise NotFittedError
        ret = np.empty((len(X), 1))
        for i, x in enumerate(X):
            ret[i, 0] = self.function_(x)
        return ret

    @staticmethod
    def fun_from_type(ctype: CountType):
        if ctype == CountType.N_CHAR:
            return _count_char
        elif ctype == CountType.N_WORD:
            return _count_word
        elif ctype == CountType.N_SPECIAL:
            return _count_special
        elif ctype == CountType.N_UPPER:
            return _count_upper
        elif ctype == CountType.N_DIGIT:
            return _count_digit


_re_upper = re.compile(r"[A-ZÄÖÜ]")
_re_special = re.compile(r"""["'?!()]""")
_re_digit = re.compile(r"\d")


def _count_char(txt: str):
    return len(txt)


def _count_word(txt: str):
    return txt.count(" ")


def _count_special(txt: str):
    return len(_re_special.findall(txt))


def _count_upper(txt: str):
    return len(_re_upper.findall(txt))


def _count_digit(txt: str):
    return len(_re_digit.findall(txt))
