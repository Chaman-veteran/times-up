"""
    main.py
    Dictates the structure of the game.
"""

import tkinter as tk
import tkinter.font as tkFont

import config as cfg
from team import Team
from words import Words
from lib.mutex import Mutex

window = tk.Tk()
tkFont.nametofont("TkDefaultFont").configure(family='calibri', size=16, weight='bold')

words = Words('dictionary/wordlist_fr')

def refreshUntilMutex(mutex):
    while mutex.get_value() == 0:
        window.update()

def fill_team_infos(window):
    l_name = tk.Label(window, text="Nom d'équipe : ", height=5, width=50)
    l_player1 = tk.Label(window, text="Nom joueur 1 : ", height=5, width=50)
    l_player2 = tk.Label(window, text="Nom joueur 2 : ", height=5, width=50)
    e_name = tk.Entry(window)
    e_player1 = tk.Entry(window)
    e_player2 = tk.Entry(window)

    mutex : Mutex = Mutex()
    mutex.take()
    b = tk.Button(window, text="Valider", command=mutex.put)
    for (label, entry) in ((l_name, e_name), (l_player1, e_player1), (l_player2, e_player2)):
        label.pack()
        entry.pack()
    b.pack()

    refreshUntilMutex(mutex)

    for (label, entry) in ((l_name, e_name), (l_player1, e_player1), (l_player2, e_player2)):
        label.pack_forget()
        entry.pack_forget()
    b.pack_forget()

    return Team(name=e_name.get(), window=window, playerA=e_player1.get(), playerB=e_player2.get())

team_A = fill_team_infos(window)
team_A.set_words(words)

team_B = fill_team_infos(window)
team_B.set_words(words)

def change_team(window):
    label = tk.Label(window, text="À l'autre équipe !", height=5, width=50)
    mutex : Mutex = Mutex()
    mutex.take()
    b = tk.Button(window, text="Prêt ?", command=mutex.put)
    label.pack(anchor=tk.CENTER)
    b.pack()
    refreshUntilMutex(mutex)
    label.pack_forget()
    b.pack_forget()

def print_scores(window, team_1, team_2, round):
    score_team_1 = tk.Label(window,
                            text=f"Score de l'équipe {team_1.get_name()} : {team_1.get_score()}")
    score_team_2 = tk.Label(window,
                            text=f"Score de l'équipe {team_2.get_name()} : {team_2.get_score()}")
    
    mutex : Mutex = Mutex()
    mutex.take()
    b = tk.Button(window, text='Manche suivante' if round < 3 else 'Fin', command=mutex.put)
    score_team_1.pack(anchor=tk.CENTER)
    score_team_2.pack(anchor=tk.CENTER)
    b.pack()
    refreshUntilMutex(mutex)
    score_team_1.pack_forget()
    score_team_2.pack_forget()
    b.pack_forget()

def print_round(window, round):
    if round == 1:
        todo = "il faut deviner à l'aide de phrases."
    elif round == 2:
        todo = "il faut deviner à l'aide d'un mot."
    else:
        todo = "il faut deviner à l'aide de mimes."

    label = tk.Label(window, text=f'Manche {round} : {todo}', height=5, width=50)
    mutex : Mutex = Mutex()
    mutex.take()
    b = tk.Button(window, text='Prêt ?', command=mutex.put, height=7, width=20)
    label.pack(anchor=tk.CENTER)
    b.pack()
    refreshUntilMutex(mutex)
    label.pack_forget()
    b.pack_forget()

teams = [team_A, team_B]

for round in range(1,4):
    print_round(window, round)
    teams[cfg.turn_picker].play_turn()
    cfg.turn_picker ^= 1
    while words.nb_remaining_words() > 0:
        change_team(window)
        teams[cfg.turn_picker].play_turn()
        cfg.turn_picker ^= 1

    words.reset()
    print_scores(window, team_A, team_B, round)
