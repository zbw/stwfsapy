import stwfsapy.expansion as e
from inspect import signature

_name_abbreviation_fun = e._expand_abbreviation_with_punctuation_fun.__name__
_name_ampersand_fun = e._expand_ampersand_with_spaces_fun.__name__
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


def test_combination_0000():
    conf = "0000"
    conf_map = _create_config_map(conf)
    assert len(e.collect_expansion_functions(**conf_map)) == 0


def test_combination_0001():
    conf = "0001"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 1
    assert funs[0].__name__ == _name_abbreviation_fun


def test_combination_0010():
    conf = "0010"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 1
    assert funs[0].__name__ == _name_ampersand_fun


def test_combination_0100():
    conf = "0100"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 1
    assert funs[0].__name__ == _name_replacer
    assert funs[0](lower_braces_string) == lower_braces_content


def test_combination_1000():
    conf = "1000"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 1
    assert funs[0].__name__ == _name_replacer
    assert funs[0](lower_braces_string) == lower_braces_string


def test_combination_0011():
    conf = "0011"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 2
    assert funs[0].__name__ == _name_ampersand_fun
    assert funs[1].__name__ == _name_abbreviation_fun


def test_combination_0101():
    conf = "0101"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 2
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_abbreviation_fun
    assert funs[0](lower_braces_string) == lower_braces_content


def test_combination_1001():
    conf = "1001"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 2
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_abbreviation_fun
    assert funs[0](lower_braces_string) == lower_braces_string


def test_combination_0110():
    conf = "0110"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 2
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_ampersand_fun
    assert funs[0](lower_braces_string) == lower_braces_content


def test_combination_1010():
    conf = "1010"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 2
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_ampersand_fun
    assert funs[0](lower_braces_string) == lower_braces_string


def test_combination_1100():
    conf = "1100"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 2
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_replacer
    assert funs[0](lower_braces_string) == lower_braces_string
    assert funs[1](lower_braces_string) == lower_braces_content


def test_combination_0111():
    conf = "0111"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 3
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_ampersand_fun
    assert funs[2].__name__ == _name_abbreviation_fun
    assert funs[0](lower_braces_string) == lower_braces_content


def test_combination_1011():
    conf = "1011"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 3
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_ampersand_fun
    assert funs[2].__name__ == _name_abbreviation_fun
    assert funs[0](lower_braces_string) == lower_braces_string


def test_combination_1101():
    conf = "1101"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 3
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_replacer
    assert funs[2].__name__ == _name_abbreviation_fun
    assert funs[0](lower_braces_string) == lower_braces_string
    assert funs[1](lower_braces_string) == lower_braces_content


def test_combination_1110():
    conf = "1110"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 3
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_replacer
    assert funs[2].__name__ == _name_ampersand_fun
    assert funs[0](lower_braces_string) == lower_braces_string
    assert funs[1](lower_braces_string) == lower_braces_content


def test_combination_1111():
    conf = "1111"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    assert len(funs) == 4
    assert funs[0].__name__ == _name_replacer
    assert funs[1].__name__ == _name_replacer
    assert funs[2].__name__ == _name_ampersand_fun
    assert funs[3].__name__ == _name_abbreviation_fun
    assert funs[0](lower_braces_string) == lower_braces_string
    assert funs[1](lower_braces_string) == lower_braces_content


def test_all_abbreviation_from_braces():
    conf = "1111"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    string = "GDP (gross domestic product)"
    for fun in funs:
        string = fun(string)
    assert string == "G.?D.?P.?\\W"


def test_all_ampersand_from_braces():
    conf = "1111"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    string = "(R&D) research and discovery"
    for fun in funs:
        string = fun(string)
    assert string == "R ?& ?D\\W"


def test_all_lower_braces():
    conf = "1111"
    conf_map = _create_config_map(conf)
    funs = e.collect_expansion_functions(**conf_map)
    string = "(lower) lower case explanation"
    for fun in funs:
        string = fun(string)
    assert string == "lower"
