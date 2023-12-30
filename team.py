import tkinter as tk
from time import sleep

from words import *
from counter import *
from mutex import *

class Team:
    def __word_pass__(self):
        self.words.pass_current_word()
        self.pick_word_to_guess()

    def __word_validate__(self):
        self.words.validate_current_word()
        self.score += 1
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
                                     text='Pass',
                                     command=lambda: self.__word_pass__(),
                                     font=('calibri', 10, 'bold'))
        self.validate_button = tk.Button(self.window,
                                         height=50,
                                         width=50,
                                         background='green',
                                         text='Validate',
                                         command=lambda: self.__word_validate__(),
                                         font=('calibri', 10, 'bold'))
        self.to_guess = tk.Label(self.window, font=('calibri', 30, 'bold'))

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
        self.to_guess.pack()
        self.pass_button.pack(side='left')
        self.validate_button.pack(side='right')
    
    def clear(self):
        self.ctr.clear()
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
        to_guess : str = self.words.pick_word()
        self.to_guess.config(text=f'Le mot à deviner est : {to_guess}')
    
    def print_guesser(self):
        label = tk.Label(self.window,
                         font=('calibri', 20, 'bold'),
                         text=f"{self.name}, c'est à {self.guesser} de deviner, {self.spy}, t'es prêt ?!")
        b = tk.Button(self.window ,text="Prêt ?", command=lambda: mutex.put(), height=7, width=20)
        mutex : Mutex = Mutex()
        mutex.take()
        label.pack()
        b.pack()
        while mutex.get_value() == 0:
            self.window.update_idletasks()
            self.window.update()
        label.pack_forget()
        b.pack_forget()

    def play_turn(self):
        """A team playing his allocated time for the current turn."""
        self.print_guesser()
        self.ctr.start(duration=5)
        self.draw()

        previous_score = self.score

        self.pick_word_to_guess()
        while self.ctr.get_remaining_time() > 0 and self.words.nb_remaining_words() > 0:
            self.ctr.update()
            self.window.update_idletasks()
            self.window.update()

        self.clear()

        if self.ctr.get_remaining_time() == 0:
            to = tk.Label(text='Time Out!',
                          anchor=tk.CENTER,
                          font=('calibri', 20, 'bold'))
            to.pack()
            self.window.update_idletasks()
            self.window.update()
            sleep(3)
            to.pack_forget()
        elif self.ctr.get_remaining_time() > 0:
            ez = tk.Label(text=f'EZ, tout a été deviné et il restait {self.ctr.get_remaining_time()}s.',
                          anchor=tk.CENTER,
                         font=('calibri', 20, 'bold'))
            ez.pack()
            self.window.update_idletasks()
            self.window.update()
            sleep(3)
            ez.pack_forget()

        scored = tk.Label(text=f'{self.name} a scoré {self.score - previous_score} !',
                          anchor=tk.CENTER,
                         font=('calibri', 20, 'bold'))
        scored.pack()
        self.window.update_idletasks()
        self.window.update()
        sleep(3)
        scored.pack_forget()

        self.ctr.reset()
        self.spy, self.guesser = self.guesser, self.spy
