"""
    main.py
    Dictates the structure of the game.
"""

import tkinter as tk

from lib.mutex import Mutex

import config as cfg
from team import Team
from ui import print_round, print_guesser, change_team, print_scores, refreshUntilMutex
from words import Words

playable_words = Words('dictionary/wordlist_fr')

def fill_team_infos():
    l_name = tk.Label(cfg.window, text="Nom d'équipe : ", height=5, width=50)
    l_player1 = tk.Label(cfg.window, text="Nom joueur 1 : ", height=5, width=50)
    l_player2 = tk.Label(cfg.window, text="Nom joueur 2 : ", height=5, width=50)
    e_name = tk.Entry(cfg.window)
    e_player1 = tk.Entry(cfg.window)
    e_player2 = tk.Entry(cfg.window)

    mutex : Mutex = Mutex()
    mutex.take()
    b = tk.Button(cfg.window, text="Valider", command=mutex.put)
    for (label, entry) in ((l_name, e_name), (l_player1, e_player1), (l_player2, e_player2)):
        label.pack()
        entry.pack()
    b.pack()

    refreshUntilMutex(mutex)

    for (label, entry) in ((l_name, e_name), (l_player1, e_player1), (l_player2, e_player2)):
        label.pack_forget()
        entry.pack_forget()
    b.pack_forget()

    return Team(name=e_name.get(), playerA=e_player1.get(), playerB=e_player2.get())

team_A : Team = fill_team_infos()
team_A.set_words(playable_words)

team_B : Team = fill_team_infos()
team_B.set_words(playable_words)

teams = [team_A, team_B]

for round in range(1,4):
    print_round(round)
    print_guesser(teams[cfg.turn_picker])
    teams[cfg.turn_picker].play_turn()
    cfg.turn_picker ^= 1
    while playable_words.nb_remaining_words() > 0:
        change_team()
        print_guesser(teams[cfg.turn_picker])
        teams[cfg.turn_picker].play_turn()
        cfg.turn_picker ^= 1

    playable_words.reset()
    print_scores(team_A, team_B, round)
