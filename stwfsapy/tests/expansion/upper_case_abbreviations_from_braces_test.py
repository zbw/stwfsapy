from stwfsapy import expansion as e
import common as c

replacement_fun_upper = e._replace_by_pattern_fun(
    e._upper_case_abbreviation_from_braces_expression)


def test_pattern_match():
    match = e._upper_case_abbreviation_from_braces_expression.match(
        c.test_string_upper
        )
    assert match.group(0) == c.test_string_upper
    assert match.group(1) == c.test_abbreviation_upper


def test_replacement():
    assert replacement_fun_upper(c.test_string_upper) == \
        c.test_abbreviation_upper


def test_no_replacement():
    assert replacement_fun_upper(c.test_string_any) == c.test_string_any


def test_no_match_when_not_at_beginning():
    test_string = " " + c.test_abbreviation_upper
    assert e._upper_case_abbreviation_from_braces_expression.search(
        test_string
    ) is None
