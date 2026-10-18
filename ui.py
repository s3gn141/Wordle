"""Ответственнен за весь ввод и вывод"""
import tkinter as tk
from words import WORD_LENGTH, assign_secret
from game import COUNT_TRIES, Game, InvalidMoveError, GameOverError
from checker import ABSENT,PRESENT,CORRECT
from functools import partial


ALPHABET = 'abcdefghijklnmopqrstuvwxyz'
COLOR_BG = "black"
COLOR_CELL_BG = "black"
COLOR_CELL_FRAME = "white"
COLOR_CELL_ABSENT = "#3a3a3c"
COLOR_CELL_PRESENT = "#b59f3b"
COLOR_CELL_CORRECT = "#538d4e"
COLOR_TEXT = "white"
COLOR_KEY_BG = "#818384"

FONT_FAMILY = "Helvetica"
FONT_CELL = (FONT_FAMILY, 28, "bold")
FONT_TITLE = (FONT_FAMILY, 28, "bold")
FONT_MESSAGE = (FONT_FAMILY, 14)
FONT_KEY = (FONT_FAMILY, 14, "bold")

KEYBOARD_ROWS = ("qwertyuiop", "asdfghjkl", "zxcvbnm")  
SIZE_KEY_WIDTH = 40  
SIZE_KEY_HEIGHT = 52  
KEY_GAP = 3

SIZE_CELL = 62
CELL_GAP = 4
FRAME_THICKNESS = 2

COUNT_COLUMNS = WORD_LENGTH
COUNT_LINES = COUNT_TRIES

COND_TO_COLOR = {ABSENT:COLOR_CELL_ABSENT, PRESENT:COLOR_CELL_PRESENT, CORRECT:COLOR_CELL_CORRECT}
STATUS_PRIORITY = {ABSENT: 1, PRESENT: 2, CORRECT: 3}

class WordlyApp:
    def __init__(self, root, answers, allowed):
        self.root = root
        self.answers = answers
        self.allowed = allowed
        self.cells = []
        self.keys = {}
        self.letter_states = {}

        self.root.title("WORDLY")
        self.root.configure(background=COLOR_BG)
        self.root.resizable(False,False)
        self.root.bind("<Key>", self.process_input)

        self.current_line = 0
        self.input_word = []
        self.game = None

        self.build_title()
        self.build_message_label()
        self.build_board()
        self.build_keyboard()
        self.start_new_game()
        

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

    def build_keyboard(self):
        keyboard = tk.Frame(self.root, bg=COLOR_BG)
        keyboard.pack(pady=(0, 20))

        for row_letters in KEYBOARD_ROWS:
            row_frame = tk.Frame(keyboard, bg=COLOR_BG)
            row_frame.pack(pady=KEY_GAP)
            for letter in row_letters:
                self.keys[letter] = self.make_key(row_frame, letter)

    def make_key(self, master, letter):
        frame = tk.Frame(master, width=SIZE_KEY_WIDTH, height=SIZE_KEY_HEIGHT, bg=COLOR_BG)
        frame.pack(side="left", padx=KEY_GAP)
        frame.pack_propagate(False)
        label = tk.Label(frame, text=letter.upper(), font=FONT_KEY, bg=COLOR_KEY_BG, fg=COLOR_TEXT)
        label.pack(fill="both", expand=True)
        return label

    def update_keyboard(self, word, statuses):
        for letter, status in zip(word, statuses):
            old_status = self.letter_states.get(letter)
            if old_status is None or STATUS_PRIORITY[status] > STATUS_PRIORITY[old_status]:
                self.letter_states[letter] = status
                self.keys[letter].configure(bg=COND_TO_COLOR[status])

    def start_new_game(self):
        answer = assign_secret(self.answers)
        self.game = Game(answer,self.allowed)
        self.current_line = 0
        self.input_word = []
        self.message_label.configure(text="")
        for row in range(len(self.cells)):
            for col in range(WORD_LENGTH):
                self.cells[row][col].configure(text="")

        print("New game started")
        print(f"Answer is: {self.game.answer}")

    def process_input(self, event):
        #print(f"Key pressed: {event.char} | Keysym: {event.keysym}")
        if event.keysym == "BackSpace":
            self.delete_letter()
        elif event.keysym == "Return":
            self.send_word()
        elif event.keysym.lower() in ALPHABET:
            self.add_letter(event.keysym.lower())

    def add_letter(self,letter):
        if len(self.input_word) < WORD_LENGTH and not self.game.is_over():
            self.input_word.append(letter)
            self.cells[self.current_line][len(self.input_word)-1].configure(text=letter)

    def delete_letter(self):
        if self.input_word:
            self.cells[self.current_line][len(self.input_word)-1].configure(text="")
            self.input_word.pop()
    
    def send_word(self):
        if not self.game.is_over():
            try:
                word = "".join(self.input_word) 
                attempt = self.game.make_guess(word)
            except InvalidMoveError as error:
                self.message_label.configure(text=error)
            else:
                self.message_label.configure(text="")
                self.paint_row(self.current_line, attempt)
                self.update_keyboard(word, attempt)
                self.current_line+=1
                if self.game.is_win():
                    self.message_label.configure(text="Вы отгадали слово, поздравляем!!!")
                elif self.game.is_over():
                    self.message_label.configure(text=f"Вы проиграли( Загаданное слово было {self.game.answer}")
                self.input_word = []
                print(self.game.count_tries)
        else:
            self.message_label.configure(text=f"Игра окончена, вы не можете делать ходы")

    def paint_row(self, row, statuses):
        for i,status in enumerate(statuses):
            self.cells[row][i].configure(bg=COND_TO_COLOR[status])