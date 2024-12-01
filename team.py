"""
    team.py
    Module to manage teams.
    Display of the game during play time is also handled here.
"""

import tkinter as tk
from time import sleep

from words import Words, EndOfWords
import config as cfg

from lib.counter import DEFAULT_DURATION, Timer

class Team:
    def __word_pass__(self):
        self.words.pass_current_word()
        self.pick_word_to_guess()

    def __word_validate__(self):
        self.score_round += 1
        self.validated_counter.config(text=f'Mots validés ce tour : {self.score_round}')
        self.words.validate_current_word()
        try:
            self.pick_word_to_guess()
        except EndOfWords:
            pass

    def __init_gui__(self):
        self.pass_button = tk.Button(cfg.window,
                                     height=50,
                                     width=50,
                                     background='red',
                                     activebackground='red',
                                     text='Passer',
                                     command=lambda: self.__word_pass__())
        self.validate_button = tk.Button(cfg.window,
                                         height=50,
                                         width=50,
                                         background='green',
                                         activebackground='green',
                                         text='Valider',
                                         command=lambda: self.__word_validate__())
        self.to_guess = tk.Label(cfg.window, font=('calibri', 30, 'bold'))
        self.validated_counter = tk.Label(cfg.window,
                                          text=f'Mot validé ce tour : {self.score_round}',
                                          font=('calibri', 30, 'bold'))

    def __init__(self, name : str, playerA : str= 'Alice', playerB : str= 'Bob'):
        self.name : str = name
        self.playerA : str = playerA
        self.playerB : str = playerB
        # guesser : the one trying to guess the word at stake
        self.spy : str = playerA
        self.guesser : str = playerB
        # Initialization of the team's score and timer
        self.score = 0
        self.score_round = 0
        self.ctr : Timer = Timer(cfg.window)
        # GUI
        self.__init_gui__()

    def draw(self):
        self.ctr.draw()
        self.validated_counter.pack()
        self.to_guess.pack()
        self.pass_button.pack(side='left')
        self.validate_button.pack(side='right')
    
    def clear(self):
        self.ctr.clear()
        self.validated_counter.pack_forget()
        self.to_guess.pack_forget()
        self.pass_button.pack_forget()
        self.validate_button.pack_forget()

    def set_words(self, words : Words):
        self.words = words
    
    def get_score(self):
        return self.score

    def get_name(self):
        return self.name
    
    def get_spy(self):
        return self.spy

    def get_guesser(self):
        return self.guesser

    def pick_word_to_guess(self):
        word_to_guess : str = self.words.pick_word()
        self.to_guess.config(text=f'Le mot à deviner est : {word_to_guess}')

    def play_turn(self):
        """A team playing his allocated time for the current turn."""
        self.ctr.start()
        self.draw()

        self.pick_word_to_guess()
        while self.ctr.get_remaining_time() > 0 and self.words.nb_remaining_words() > 0:
            self.ctr.update()
            cfg.window.update()

        self.clear()

        label_round_end = ''
        saved_ctr = DEFAULT_DURATION
        if self.ctr.get_remaining_time() == 0:
            label_round_end = 'Time Out!'
            self.__word_pass__()
        elif (time_left := self.ctr.get_remaining_time()) > 0:
            label_round_end = f'Tout a été deviné et il restait {time_left:.1f}s.'
            if time_left > (threshold := 10):
                label_round_end += f'\nIl restait plus de {threshold}s, {self.name} va continuer à jouer !'
                self.spy, self.guesser = self.guesser, self.spy
                cfg.turn_picker ^= 1
                saved_ctr = time_left

        round_end = tk.Label(text=label_round_end, width=50)
        self.score += self.score_round
        scored = tk.Label(text=f'{self.name} a scoré {self.score_round} !')

        round_end.pack(anchor=tk.CENTER)
        scored.pack(anchor=tk.CENTER)

        cfg.window.update_idletasks()
        sleep(4)

        round_end.pack_forget()
        scored.pack_forget()

        self.ctr.reset(saved_ctr)
        self.spy, self.guesser = self.guesser, self.spy
        self.score_round = 0
        self.validated_counter.config(text=f'Mots validés ce tour : {self.score_round}')

