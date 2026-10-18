"""Запуск работы всей игры"""
import sys
from words import *
from game import *

def main():
    try:
        answers = load_words(PATH_ANSWERS)
        allowed = load_words(PATH_ALLOWED)
    except WordListError as error:
        print(error)
        sys.exit(1)

    allowed = set(allowed) | set(answers)
    answer = assign_secret(answers)

    game = Game(answer, allowed)

    print("Make interface")

if __name__ == '__main__':
    main()