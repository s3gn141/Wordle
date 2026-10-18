import pytest

from words import WordListError, check_word_validity, load_words


def test_load_words_filters_and_normalizes(tmp_path):
    file = tmp_path / "words.txt"
    file.write_text("Apple\n  grape \n\ntoolong\nab1de\nlemon\n", encoding="utf-8")
    assert load_words(file) == ["apple", "grape", "lemon"]


def test_load_words_missing_file(tmp_path):
    with pytest.raises(WordListError):
        load_words(tmp_path / "nope.txt")