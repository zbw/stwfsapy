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


import stwfsapy.expansion as e
from inspect import signature

_name_abbreviation_fun = e._expand_abbreviation_with_punctuation_fun.__name__
_name_ampersand_fun = e._expand_ampersand_with_spaces_fun.__name__
_name_english_plural_fun = e._simple_english_plural_fun.__name__
_name_replacer = "replacer"

lower_braces_content = "foo"
lower_braces_string = "({}) bar".format(lower_braces_content)

_conf_keys = list(signature(e.collect_expansion_functions).parameters)
"""All parameters of the collect_expansion_functions method"""


def _create_config_map(lst):
    return {
        k: bool(int(v))
        for k, v
        in zip(_conf_keys, lst)}


def test_combination_00000():
    conf = "00000"
    conf_map = _create_config_map(conf)
    assert len(e.collect_expansion_functions(**conf_map)) == 0


def test_combination_00001():
    conf = "00001"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 1
    assert funs[0].__name__ == _name_english_plural_fun


def test_combination_00010():
    conf = "00010"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 1
    assert funs[0].__name__ == _name_abbreviation_fun


def test_combination_00100():
    conf = "00100"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 1
    assert funs[0].__name__ == _name_ampersand_fun


def test_combination_01000():
    conf = "01000"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 1
    assert funs[0].__name__ == _name_replacer
    assert funs[0](lower_braces_string) == lower_braces_content


def test_combination_10000():
    conf = "10000"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 1
    assert funs[0].__name__ == _name_replacer
    assert funs[0](lower_braces_string) == lower_braces_string


def test_combination_00011():
    conf = "00011"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 2
    assert funs[0].__name__ == _name_abbreviation_fun
    assert funs[1].__name__ == _name_english_plural_fun


def test_combination_00101():
    conf = "00101"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 2
    assert funs[0].__name__ == _name_ampersand_fun
    assert funs[1].__name__ == _name_english_plural_fun


def test_combination_01001():
    conf = "01001"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 2
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_english_plural_fun
    assert funs[0](lower_braces_string) == lower_braces_content


def test_combination_10001():
    conf = "10001"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 2
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_english_plural_fun
    assert funs[0](lower_braces_string) == lower_braces_string


def test_combination_00110():
    conf = "00110"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 2
    assert funs[0].__name__ == _name_ampersand_fun
    assert funs[1].__name__ == _name_abbreviation_fun


def test_combination_01010():
    conf = "01010"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 2
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_abbreviation_fun
    assert funs[0](lower_braces_string) == lower_braces_content


def test_combination_10010():
    conf = "10010"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 2
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_abbreviation_fun
    assert funs[0](lower_braces_string) == lower_braces_string


def test_combination_01100():
    conf = "01100"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 2
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_ampersand_fun
    assert funs[0](lower_braces_string) == lower_braces_content


def test_combination_10100():
    conf = "10100"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 2
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_ampersand_fun
    assert funs[0](lower_braces_string) == lower_braces_string


def test_combination_11000():
    conf = "11000"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 2
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_replacer
    assert funs[0](lower_braces_string) == lower_braces_string
    assert funs[1](lower_braces_string) == lower_braces_content


def test_combination_00111():
    conf = "00111"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 3
    assert funs[0].__name__ == _name_ampersand_fun
    assert funs[1].__name__ == _name_abbreviation_fun
    assert funs[2].__name__ == _name_english_plural_fun


def test_combination_01011():
    conf = "01011"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 3
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_abbreviation_fun
    assert funs[2].__name__ == _name_english_plural_fun
    assert funs[0](lower_braces_string) == lower_braces_content


def test_combination_01101():
    conf = "01101"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 3
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_ampersand_fun
    assert funs[2].__name__ == _name_english_plural_fun
    assert funs[0](lower_braces_string) == lower_braces_content


def test_combination_10011():
    conf = "10011"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 3
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_abbreviation_fun
    assert funs[2].__name__ == _name_english_plural_fun
    assert funs[0](lower_braces_string) == lower_braces_string


def test_combination_10101():
    conf = "10101"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 3
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_ampersand_fun
    assert funs[2].__name__ == _name_english_plural_fun
    assert funs[0](lower_braces_string) == lower_braces_string


def test_combination_11001():
    conf = "11001"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 3
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_replacer
    assert funs[2].__name__ == _name_english_plural_fun
    assert funs[0](lower_braces_string) == lower_braces_string
    assert funs[1](lower_braces_string) == lower_braces_content


def test_combination_01110():
    conf = "01110"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 3
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_ampersand_fun
    assert funs[2].__name__ == _name_abbreviation_fun
    assert funs[0](lower_braces_string) == lower_braces_content


def test_combination_10110():
    conf = "10110"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 3
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_ampersand_fun
    assert funs[2].__name__ == _name_abbreviation_fun
    assert funs[0](lower_braces_string) == lower_braces_string


def test_combination_11010():
    conf = "11010"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 3
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_replacer
    assert funs[2].__name__ == _name_abbreviation_fun
    assert funs[0](lower_braces_string) == lower_braces_string
    assert funs[1](lower_braces_string) == lower_braces_content


def test_combination_11100():
    conf = "11100"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 3
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_replacer
    assert funs[2].__name__ == _name_ampersand_fun
    assert funs[0](lower_braces_string) == lower_braces_string
    assert funs[1](lower_braces_string) == lower_braces_content


def test_combination_01111():
    conf = "01111"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 4
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_ampersand_fun
    assert funs[2].__name__ == _name_abbreviation_fun
    assert funs[3].__name__ == _name_english_plural_fun
    assert funs[0](lower_braces_string) == lower_braces_content


def test_combination_10111():
    conf = "10111"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 4
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_ampersand_fun
    assert funs[2].__name__ == _name_abbreviation_fun
    assert funs[3].__name__ == _name_english_plural_fun
    assert funs[0](lower_braces_string) == lower_braces_string


def test_combination_11011():
    conf = "11011"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 4
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_replacer
    assert funs[2].__name__ == _name_abbreviation_fun
    assert funs[3].__name__ == _name_english_plural_fun
    assert funs[0](lower_braces_string) == lower_braces_string
    assert funs[1](lower_braces_string) == lower_braces_content


def test_combination_11101():
    conf = "11101"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 4
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_replacer
    assert funs[2].__name__ == _name_ampersand_fun
    assert funs[3].__name__ == _name_english_plural_fun
    assert funs[0](lower_braces_string) == lower_braces_string
    assert funs[1](lower_braces_string) == lower_braces_content


def test_combination_11110():
    conf = "11110"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 4
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_replacer
    assert funs[2].__name__ == _name_ampersand_fun
    assert funs[3].__name__ == _name_abbreviation_fun
    assert funs[0](lower_braces_string) == lower_braces_string
    assert funs[1](lower_braces_string) == lower_braces_content


def test_combination_11111():
    conf = "11111"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 5
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_replacer
    assert funs[2].__name__ == _name_ampersand_fun
    assert funs[3].__name__ == _name_abbreviation_fun
    assert funs[4].__name__ == _name_english_plural_fun
    assert funs[0](lower_braces_string) == lower_braces_string
    assert funs[1](lower_braces_string) == lower_braces_content


def test_all_abbreviation_from_braces():
    conf = "11110"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    string = "GDP (gross domestic product)"
    for fun in funs:
        string = fun(string)
    assert string == "G\\.?D\\.?P\\.?"


def test_all_ampersand_from_braces():
    conf = "11110"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    string = "(R&D) research and discovery"
    for fun in funs:
        string = fun(string)
    assert string == "R ?& ?D"


def test_all_lower_braces():
    conf = "11110"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    string = "(lower) lower case explanation"
    for fun in funs:
        string = fun(string)
    assert string == "lower"
