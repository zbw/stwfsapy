from stwfsapy import expansion as e
import common as c

replacement_fun_any = e._replace_by_pattern_fun(
    e._any_case_from_braces_expression)


def test_pattern_match():
    match = e._any_case_from_braces_expression.search(
        c.test_string_any
        )
    assert match.group(0) == "({})".format(c.test_abbreviation_any)
    assert match.group(1) == c.test_abbreviation_any


def test_replacement():
    assert replacement_fun_any(c.test_string_any) == \
        c.test_abbreviation_any


def test_no_replacement():
    some_string = "some string)"
    assert replacement_fun_any(some_string) == some_string
