import stwfsapy.expansion as e

first = 'R'
second = 'D'
ampersand_string = "{}&{}".format(first, second)
multi_ampersand_string = "A&" + ampersand_string


def test_matches():
    match = e._ampersand_abbreviation_matcher.search(ampersand_string)
    assert match is not None
    assert match.group(0) == ampersand_string
    assert match.group(1) == first
    assert match.group(2) == second


def test_no_match_at_end_of_string():
    match = e._ampersand_abbreviation_matcher.search(" "+ampersand_string)
    assert match is None


def test_no_match_at_start_of_string():
    match = e._ampersand_abbreviation_matcher.search(ampersand_string + " ")
    assert match is None


def test_no_match_multiple_ampersand():
    match = e._ampersand_abbreviation_matcher.search(multi_ampersand_string)
    assert match is None


def test_replacement():
    replaced = e._expand_ampersand_with_spaces_fun(ampersand_string)
    assert len(replaced) == len(ampersand_string) + 6
    for i in range(len(ampersand_string)-1):
        offset = i * 3
        assert replaced[offset] == ampersand_string[i]
        assert replaced[offset+1] == ' '
        assert replaced[offset+2] == '?'
    assert replaced[-3] == ampersand_string[-1]
    assert replaced[-2] == '\\'
    assert replaced[-1] == 'W'


def test_no_replacement_multiple_ampersand():
    replaced = e._expand_ampersand_with_spaces_fun(multi_ampersand_string)
    assert replaced == multi_ampersand_string
