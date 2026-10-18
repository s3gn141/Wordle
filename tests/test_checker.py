from checker import ABSENT, CORRECT, PRESENT, check_guess


def test_all_correct():
    assert check_guess("apple", "apple") == [CORRECT] * 5


def test_no_common_letters():
    assert check_guess("crumb", "apple") == [ABSENT] * 5


def test_extra_repeated_letters_are_absent():
    assert check_guess("eerie", "plane") == [ABSENT, ABSENT, ABSENT, ABSENT, CORRECT]
    assert check_guess("ppppp", "apple") == [ABSENT, CORRECT, CORRECT, ABSENT, ABSENT]


def test_repeated_letter_partly_in_place():
    assert check_guess("xbxbb", "abbey") == [ABSENT, CORRECT, ABSENT, PRESENT, ABSENT]
    assert check_guess("babes", "abbey") == [PRESENT, PRESENT, CORRECT, CORRECT, ABSENT]