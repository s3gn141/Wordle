"""Ответственнен за весь ввод и вывод"""
import tkinter as tk
from words import WORD_LENGTH
from game import COUNT_TRIES
from checker import ABSENT,PRESENT,CORRECT

COLOR_BG = "black"
COLOR_CELL_BG = "black"
COLOR_CELL_FRAME = "white"
COLOR_CELL_ABSENT = "grey"
COLOR_CELL_PRESENT = "yellow"
COLOR_CELL_CORRECT = "green"
COLOR_TEXT = "white"

FONT_FAMILY = "Helvetica"
FONT_CELL = (FONT_FAMILY, 28, "bold")
FONT_TITLE = (FONT_FAMILY, 28, "bold")
FONT_MESSAGE = (FONT_FAMILY, 14)

SIZE_CELL = 62
CELL_GAP = 4
FRAME_THICKNESS = 2

COUNT_COLUMNS = WORD_LENGTH
COUNT_LINES = COUNT_TRIES

COND_TO_COLOR = {ABSENT:COLOR_CELL_ABSENT, PRESENT:COLOR_CELL_PRESENT, CORRECT:COLOR_CELL_CORRECT}

class WordlyApp:
    def __init__(self, root, answers, allowed):
        self.root = root
        self.answers = answers
        self.allowed = allowed
        self.cells = []

        self.root.title("WORDLY")
        self.root.configure(background=COLOR_BG)
        self.root.resizable(False,False)

        self.build_title()
        self.build_message_label()
        self.build_board()

    def build_title(self):
        title = tk.Label(self.root, text="WORDLY", font=FONT_TITLE, bg=COLOR_BG, fg=COLOR_TEXT)
        title.pack(pady=(20, 5))

    def build_message_label(self):
        self.message_label = tk.Label(self.root, text="", font=FONT_MESSAGE, bg=COLOR_BG, fg=COLOR_TEXT, height=1)
        self.message_label.pack(pady=(0, 10))

    def build_board(self):
        board = tk.Frame(self.root, bg=COLOR_BG)
        board.pack(padx=30, pady=(0, 30))

        for line in range(COUNT_LINES):
            line_cells = []
            for column in range(COUNT_COLUMNS):
                line_cells.append(self.make_cell(board, line, column))
            self.cells.append(line_cells)
    
    def make_cell(self, master, line, column):
        frame = tk.Frame(
            master,
            width=SIZE_CELL,
            height=SIZE_CELL,
            bg=COLOR_CELL_BG,
            highlightbackground=COLOR_CELL_FRAME,
            highlightthickness=FRAME_THICKNESS,
        )
        frame.grid(row=line, column=column, padx=CELL_GAP, pady=CELL_GAP)
        frame.pack_propagate(False)
        label = tk.Label(frame, text="", font=FONT_CELL, bg=COLOR_CELL_BG, fg=COLOR_TEXT)
        label.pack(fill="both", expand=True)
        return label
