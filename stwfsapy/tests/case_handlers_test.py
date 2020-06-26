import stwfsapy.case_handlers as handlers

_inp = 'foo bar'
_inp_upper = 'F.?O.?O.?'


def test_uncase_first_char_lower():
    res = handlers.uncase_first_char('lower')
    assert res == '(L|l)ower'


def test_uncase_first_char_upper():
    res = handlers.uncase_first_char('Upper')
    assert res == '(U|u)pper'


def test_sentence_case_handles_upper():
    assert _inp_upper == handlers.sentence_case_handler(_inp_upper)


def test_title_case_handles_upper():
    assert _inp_upper == handlers.title_case_handler(_inp_upper)


def test_sentence_case_handler():
    res = handlers.sentence_case_handler(_inp)
    assert res == '(F|f)oo bar'


def test_title_case_handler():
    res = handlers.title_case_handler(_inp)
    assert res == '(F|f)oo (B|b)ar'
