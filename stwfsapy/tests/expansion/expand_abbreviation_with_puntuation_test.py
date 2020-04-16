import stwfsapy.expansion as e

lower_string = "lower case"
with_hyphen_string = "WITH-HYPHEN"
upper_case_string = "UCS"


def test_does_not_change_lower():
    assert lower_string == \
        e._expand_abbreviation_with_punctuation_fun(lower_string)


def test_does_not_change_with_symbol():
    assert with_hyphen_string == \
        e._expand_abbreviation_with_punctuation_fun(with_hyphen_string)


def test_inserts_punctuation():
    result = e._expand_abbreviation_with_punctuation_fun(upper_case_string)
    assert len(result) == 3 * len(upper_case_string) + 2
    for i in range(len(upper_case_string)):
        assert result[3*i] == upper_case_string[i]
        assert result[3*i+1] == '.'
        assert result[3*i+2] == '?'
    assert result[-2:] == "\\W"
