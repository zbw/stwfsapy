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


from stwfsapy import text_features as tf
from sklearn.exceptions import NotFittedError
from stwfsapy.tests.upper_case_letters import upper_case_letters
import pytest

_text = "abcdefghijklmnopqrstuvwxyzäöü" + \
    "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ" + \
    " " + \
    "0123456789" + \
    "\"'?!()&%$"


def test_count_char():
    assert tf._count_char(_text) == 78


def test_count_words():
    assert tf._count_word(_text) == 1


def test_count_special():
    assert tf._count_special(_text) == 6


def test_count_upper():
    assert tf._count_upper(_text) == 29


def test_count_digit():
    assert tf._count_digit(_text) == 10


def test_raises_when_not_fit():
    c_feature = tf.CountFeature(tf.CountType.N_CHAR)
    with pytest.raises(NotFittedError):
        c_feature.transform([])


def test_transform():
    c_feature = tf.CountFeature(tf.CountType.N_DIGIT)
    c_feature.fit([])
    transformed = c_feature.transform(["0123456789abc"[:i] for i in range(14)])
    assert len(transformed) == 14
    for i in range(10):
        assert list(transformed[i]) == [i]
    for i in range(10, 14):
        assert list(transformed[i]) == [10]


def test_config_char():
    c_feature = tf.CountFeature(tf.CountType.N_CHAR)
    c_feature.fit([])
    assert c_feature.function_ == tf._count_char


def test_config_word():
    c_feature = tf.CountFeature(tf.CountType.N_WORD)
    c_feature.fit([])
    assert c_feature.function_ == tf._count_word


def test_config_special():
    c_feature = tf.CountFeature(tf.CountType.N_SPECIAL)
    c_feature.fit([])
    assert c_feature.function_ == tf._count_special


def test_config_upper():
    c_feature = tf.CountFeature(tf.CountType.N_UPPER)
    c_feature.fit([])
    assert c_feature.function_ == tf._count_upper


def test_config_digit():
    c_feature = tf.CountFeature(tf.CountType.N_DIGIT)
    c_feature.fit([])
    assert c_feature.function_ == tf._count_digit


def test_feature_creation():
    union = tf.mk_text_features()
    assert [t[0] for t in union.transformer_list] == [
        tf._NAME_CHAR_FEATURE,
        tf._NAME_WORD_FEATURE,
        tf._NAME_SPECIAL_CHARS_FEATURE,
        tf._NAME_UPPER_FEATURE,
        tf._NAME_DIGIT_FEATURE,
    ]


def test_international_upper_case_recall():
    count = tf._count_upper(upper_case_letters)
    assert count == len(upper_case_letters)


def test_international_upper_case_precision():
    for c in upper_case_letters:
        assert 1 == tf._count_upper(f'xy{c}z')
