"""Сверяем догадку с самим загаданным словом"""

from collections import Counter
from words import WORD_LENGTH

CORRECT = 'correct'
PRESENT = 'present'
ABSENT = 'absent'



def check_guess(guess:str, answer:str) -> list[str]:
    guess = list(guess)
    answer = list(answer)
    template = [ABSENT] * WORD_LENGTH
    counter = Counter()

    
    #Пример
    #guess = 'eerie',    guess = 'apple'
    #answer= 'plane',    answer= 'plane'
    
    for i,letter in enumerate(guess): # длину guess проверяем в game.py так что тут все норм будет
        if letter == answer[i]:
            template[i] = CORRECT
        else:
            counter[answer[i]] += 1
    
    #counter = {p:1,l:1,a:1,n:1},    counter = {p:1, l:1, a:1, n:1}
    
    
    for i,letter in enumerate(guess): # длину guess проверяем в game.py так что тут все норм будет
        if template[i] != CORRECT:
            if letter in counter and counter[letter] > 0:
                template[i] = PRESENT
                counter[letter] -= 1


    return template # проверку на то что в template все CORRECT произведем в game.py, здесь просто вернем аля булевую маску