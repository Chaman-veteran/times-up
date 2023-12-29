from typing import List
from random import shuffle
from asyncio import create_task

from words import *
from counter import *

class Team:
    def __init__(self, name : str, playerA : str= 'Alice', playerB : str= 'Bob'):
        self.name : str = name
        self.playerA : str = playerA
        self.playerB : str = playerB
        # guesser : the one trying to guess the word at stake
        self.spy : str = playerA
        self.guesser : str = playerB
        # Initialization of the team's score and timer
        self.score = 0
        self.ctr : Timer = Timer()
    
    def set_words(self, words : Words):
        self.words = words
    
    def get_score(self):
        return self.score
    
    def play_turn(self):
        """A team playing his allocated time for the current turn."""
        print(f"C'est à {self.playerB} de deviner, {self.playerA}, t'es prêt ?!")
        self.ctr.start()

        while self.ctr.get_remaining_time() > 0 and len(self.words) > 0:
            to_guess : str = self.words.pick_word()
            print(f'Le mot à deviner est : {to_guess}')
            taskInput = create_task(input('[P] Passer le mot, [v] Valider le mot'))
            if taskInput.done():
                ret = taskInput.result()
                if ret.upper() == 'P':
                    self.words.pass_current_word()
                elif ret.upper() == 'V':
                    self.words.validate_current_word()
                else:
                    print('Error.')
                    exit(1)

        if self.ctr.get_remaining_time() == 0:
            print("Time's up!")
        else:
            print(f'EZ, tout à été deviné et il restait {self.ctr.get_remaining_time()}s.')

        score : int = len(self.guessed)
        print(f'{self.name} a scoré {score} !')
        self.score += score
        self.ctr.reset()

        self.guesser = self.playerB if self.guesser == self.playerA else self.playerA
