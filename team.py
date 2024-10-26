"""
    team.py
    Module to manage teams.
    Display of the game during play time is also handled here.
"""

import tkinter as tk
from time import sleep

from words import Words, EndOfWords

from lib.counter import Timer
from lib.mutex import Mutex

class Team:
    def __word_pass__(self):
        self.words.pass_current_word()
        self.pick_word_to_guess()

    def __word_validate__(self):
        self.score += 1
        self.validated_counter.config(text=f'Mots validés ce tour : {self.score}')
        self.words.validate_current_word()
        try:
            self.pick_word_to_guess()
        except EndOfWords:
            pass

    def __init_gui__(self, window):
        self.window = window

        self.pass_button = tk.Button(self.window,
                                     height=50,
                                     width=50,
                                     background='red',
                                     activebackground='red',
                                     text='Passer',
                                     command=lambda: self.__word_pass__())
        self.validate_button = tk.Button(self.window,
                                         height=50,
                                         width=50,
                                         background='green',
                                         activebackground='green',
                                         text='Valider',
                                         command=lambda: self.__word_validate__())
        self.to_guess = tk.Label(self.window, font=('calibri', 30, 'bold'))
        self.validated_counter = tk.Label(self.window,
                                          text=f'Mot validé ce tour : {self.score}',
                                          font=('calibri', 30, 'bold'))

    def __init__(self, name : str, window, playerA : str= 'Alice', playerB : str= 'Bob'):
        self.name : str = name
        self.playerA : str = playerA
        self.playerB : str = playerB
        # guesser : the one trying to guess the word at stake
        self.spy : str = playerA
        self.guesser : str = playerB
        # Initialization of the team's score and timer
        self.score = 0
        self.ctr : Timer = Timer(window)
        # GUI
        self.__init_gui__(window)

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

    def pick_word_to_guess(self):
        word_to_guess : str = self.words.pick_word()
        self.to_guess.config(text=f'Le mot à deviner est : {word_to_guess}')
    
    def print_guesser(self):
        label = tk.Label(self.window,
                         text=f"{self.name}, c'est à {self.spy} de faire deviner à {self.guesser}, {self.spy} t'es prêt ?!")
        mutex : Mutex = Mutex()
        mutex.take()
        b = tk.Button(self.window ,text="Prêt ?", command=mutex.put, height=7, width=20)
        label.pack()
        b.pack()
        while mutex.get_value() == 0:
            self.window.update()
        label.pack_forget()
        b.pack_forget()

    def play_turn(self):
        """A team playing his allocated time for the current turn."""
        self.print_guesser()
        self.ctr.start()
        self.draw()

        previous_score = self.score

        self.pick_word_to_guess()
        while self.ctr.get_remaining_time() > 0 and self.words.nb_remaining_words() > 0:
            self.ctr.update()
            self.window.update()

        self.clear()

        label_round_end = ''
        if self.ctr.get_remaining_time() == 0:
            label_round_end = 'Time Out!'
            self.__word_pass__()
        elif self.ctr.get_remaining_time() > 0:
            label_round_end = f'Tout a été deviné et il restait {self.ctr.get_remaining_time():.1f}s.'

        round_end = tk.Label(text=label_round_end)
        scored = tk.Label(text=f'{self.name} a scoré {self.score - previous_score} !')

        round_end.pack(anchor=tk.CENTER)
        scored.pack(anchor=tk.CENTER)

        self.window.update_idletasks()
        sleep(4)

        round_end.pack_forget()
        scored.pack_forget()

        self.ctr.reset()
        self.spy, self.guesser = self.guesser, self.spy
