"""Следим за состоянием партии и соблюдением правил игры"""
from words import WORD_LENGTH, check_word_validity
from checker import ABSENT, PRESENT, CORRECT, check_guess


COUNT_TRIES = 6

STATE_PLAYING = "playing"
STATE_WON = "won"
STATE_LOST = "lost"

STATUS_PRIORITY = {ABSENT: 1, PRESENT: 2, CORRECT: 3}

class InvalidMoveError(Exception):
    """Ошибка для неправильного хода"""

class GameOverError(Exception):
    """Ошибка если игру уже окончена но хотят сделать ход"""

class Game:

    def __init__(self, answer, allowed):
        self.answer = answer
        self.allowed = allowed
        self.attempts = []

    @property
    def attempts_left(self):
        return COUNT_TRIES - len(self.attempts)

    @property
    def state(self):
        if self.is_win():
            return STATE_WON
        if self.attempts_left <= 0:
            return STATE_LOST
        return STATE_PLAYING

    @property
    def letter_states(self):
        states = {}
        for word, statuses in self.attempts:
            for letter, status in zip(word, statuses):
                if letter not in states or STATUS_PRIORITY[status] > STATUS_PRIORITY[states[letter]]:
                    states[letter] = status
        return states

    def make_guess(self, guess):
        if self.is_over():
            raise GameOverError("Игра окончена, ходы делать нельзя")
        
        guess = guess.strip().lower()

        if len(guess) != WORD_LENGTH:
            raise InvalidMoveError(f"Слово должно быть ровно длины {WORD_LENGTH}")
        if not (guess.isalpha() and guess.isascii()):
            raise InvalidMoveError("Символы в слове должны быть исключительно буквами английского алфавита")
        if not check_word_validity(guess, self.allowed):
            raise InvalidMoveError("Такого слова нет в словаре, попробуйте другое")
        
        attempt = check_guess(guess, self.answer)
        self.attempts.append(tuple([guess,attempt]))

        return attempt

    
    def is_win(self):
        if self.attempts:
            return self.attempts[-1][1] == [CORRECT] * WORD_LENGTH
        return False
            
            
    def is_over(self):
        return self.state != STATE_PLAYING