from typing import List
from random import shuffle
from time import sleep
from threading import Thread

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

    def get_name(self):
        return self.name
    
    def play_turn(self):
        """A team playing his allocated time for the current turn."""
        print(f"C'est à {self.guesser} de deviner, {self.spy}, t'es prêt ?!")
        self.ctr.start(duration=3)

        def time_bomb(ctr):
            while True:
                if ctr.get_remaining_time() > 0:
                    pass
                else:
                    break

        score : int = 0

        def get_inputs(result):
            print('[P] Passer le mot, [V] Valider le mot ')
            result.append(input())
            return result

        timer = Thread(target=time_bomb, args=(self.ctr,))
        timer.start()
        while self.words.nb_remaining_words() > 0:
            to_guess : str = self.words.pick_word()
            print(f'Le mot à deviner est : {to_guess}')
            result = list()
            play = Thread(target=get_inputs, args=(result,))
            play.start()

            # If we received the input, we can take it into account and ask for another input
            while timer.is_alive() and play.is_alive():
                pass

            if self.ctr.get_remaining_time() == 0:
                print("Time's up!")
                break

            ret = result[0]
            if ret.upper() == 'P':
                self.words.pass_current_word()
            elif ret.upper() == 'V':
                self.words.validate_current_word()
                score += 1
            else:
                print('Error.')
                exit(1)

        if self.ctr.get_remaining_time() > 0:
            print(f'EZ, tout a été deviné et il restait {self.ctr.get_remaining_time()}s.')

        print(f'{self.name} a scoré {score} !')
        self.score += score
        self.ctr.reset()

        self.spy, self.guesser = self.guesser, self.spy
