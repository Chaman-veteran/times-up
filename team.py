import tkinter as tk

from words import *
from counter import *

def word_pass(words):
    words.pass_current_word()
    try:
        to_guess = words.pick_word()
        print(f'Le mot à deviner est : {to_guess}')
    except EndOfWords:
        pass

def word_validate(words):
    words.validate_current_word()
    to_guess = words.pick_word()
    print(f'Le mot à deviner est : {to_guess}')

class Team:
    def __init_gui__(self, window):
        self.window = window

        self.pass_button = tk.Button(self.window,
                                     height=50,
                                     width=50,
                                     background='red',
                                     text='Pass',
                                     command=lambda: word_pass(self.words))
        self.validate_button = tk.Button(self.window,
                                         height=50,
                                         width=50,
                                         background='green',
                                         text='Validate',
                                         command=lambda: word_validate(self.words))

    def __print_buttons__(self):
        self.pass_button.pack(side='left')
        self.validate_button.pack(side='right')
    
    def __remove_buttons__(self):
        self.pass_button.pack_forget()
        self.validate_button.pack_forget()


    def __init__(self, name : str, window, playerA : str= 'Alice', playerB : str= 'Bob'):
        self.name : str = name
        self.playerA : str = playerA
        self.playerB : str = playerB
        # guesser : the one trying to guess the word at stake
        self.spy : str = playerA
        self.guesser : str = playerB
        # Initialization of the team's score and timer
        self.score = 0
        self.ctr : Timer = Timer()
        # GUI
        self.__init_gui__(window)

    
    def set_words(self, words : Words):
        self.words = words
    
    def get_score(self):
        return self.score

    def get_name(self):
        return self.name
    
    def play_turn(self):
        """A team playing his allocated time for the current turn."""
        self.__print_buttons__()
        print(f"C'est à {self.guesser} de deviner, {self.spy}, t'es prêt ?!")
        self.ctr.start(duration=5)

        score : int = 0

        to_guess : str = self.words.pick_word()
        print(f'Le mot à deviner est : {to_guess}')
        while self.ctr.get_remaining_time() > 0 and self.words.nb_remaining_words() > 0:
            self.window.update_idletasks()
            self.window.update()
            pass

        if self.ctr.get_remaining_time() == 0:
            print('Time Out!')
        elif self.ctr.get_remaining_time() > 0:
            print(f'EZ, tout a été deviné et il restait {self.ctr.get_remaining_time()}s.')

        print(f'{self.name} a scoré {score} !')
        self.score += score
        self.ctr.reset()

        self.spy, self.guesser = self.guesser, self.spy
        self.__remove_buttons__()
