def uncase_first_char(text: str) -> str:
    return "({}|{}){}".format(
        text[0].upper(),
        text[0].lower(),
        text[1:]
        )


def sentence_case_handler(text: str) -> str:
    if text.isupper():
        return text
    return uncase_first_char(text)


def title_case_handler(text: str) -> str:
    if text.isupper():
        return text
    return ' '.join(map(uncase_first_char, text.split()))
