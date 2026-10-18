"""Работает со словарем(есть слово или нет и т.д)"""
import random
from pathlib import Path

WORD_LENGTH = 5
DATA_DIR = Path(__file__).parent/"data" #путь до data, универсальный
PATH_ANSWERS = DATA_DIR/"answers.txt" #путь до answers
PATH_ALLOWED = DATA_DIR/"allowed.txt" #путь до allowed

class WordListError(Exception):
    """Проблема со словарём: файла нет, он нечитаем или в нём нет подходящих слов."""


def load_words(path: str | Path) -> list[str]:

    try:
        text = Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        raise WordListError(f"Файл словаря не найден: {path}")
    except (OSError, UnicodeDecodeError):
        raise WordListError(f"Не удалось прочитать файл словаря: {path}")

    text = [w.strip().lower() for w in text.splitlines()]
    words = [w for w in text if (w.isalpha() and w.isascii() and len(w)==WORD_LENGTH)]

    if not words:
        raise WordListError(f"В файле не нашлось подходящих слов: {path}")

    return words

def assign_secret(answers:list[str]) -> str:
    return random.choice(answers)

def check_word_validity(word:str, allowed:set[str]) -> bool:
    return word.lower() in allowed