"""Следим за состоянием партии и соблюдением правил игры"""
from words import WORD_LENGTH, check_word_validity
from checker import CORRECT, check_guess

class InvalidMoveError(Exception):
    """Ошибка для неправильного хода"""
class GameOverError(Exception):
    """Ошибка если игру уже окончена но хотят сделать ход"""

COUNT_TRIES = 6

class Game:

    def __init__(self, answer, allowed):
        self.answer = answer
        self.allowed = allowed
        self.count_tries = COUNT_TRIES
        self.attempts = []

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
        
        self.count_tries -= 1
        attempt = check_guess(guess, self.answer)
        self.attempts.append(tuple([guess,attempt]))

        return attempt

    
    def is_win(self):
        if self.attempts:
            return self.attempts[-1][1] == [CORRECT] * WORD_LENGTH
        return False
            
            
    def is_over(self):
        return self.count_tries == 0 or self.is_win()