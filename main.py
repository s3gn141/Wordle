"""Запуск работы всей игры"""
import tkinter as tk
import sys
from words import *
from game import *
from ui import WordlyApp

WINDOW_SIZE = "650x650"

def main():
    try:
        answers = load_words(PATH_ANSWERS)
        allowed = load_words(PATH_ALLOWED)
    except WordListError as error:
        print(error)
        sys.exit(1)

    allowed = set(allowed) | set(answers)
    root = tk.Tk()
    root.geometry(WINDOW_SIZE)
    app = WordlyApp(root,answers,allowed)
    root.mainloop()


if __name__ == '__main__':
    main()