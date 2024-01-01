from random import sample
import tkinter as tk

from team import *
from words import *
from mutex import *

NB_WORDS_TO_GUESS = 32

window = tk.Tk()

# Construct the words to play with
with open('dictionary/wordlist_fr') as f:
    words = list(set(map(lambda x: x.strip('\n'), f.readlines())))

words_to_play = sample(words, k=NB_WORDS_TO_GUESS)
words = Words(words_to_play)

def fill_team_infos(window):
    l_name = tk.Label(window, text="Nom d'équipe : ", height=5, width=50)
    l_player1 = tk.Label(window, text="Nom joueur 1 : ", height=5, width=50)
    l_player2 = tk.Label(window, text="Nom joueur 2 : ", height=5, width=50)
    e_name = tk.Entry(window)
    e_player1 = tk.Entry(window)
    e_player2 = tk.Entry(window)

    mutex : Mutex = Mutex()
    mutex.take()
    b = tk.Button(window ,text="Submit", command=lambda: mutex.put())
    l_name.pack()
    e_name.pack()
    l_player1.pack()
    e_player1.pack()
    l_player2.pack()
    e_player2.pack()
    b.pack()

    while mutex.get_value() == 0:
        window.update_idletasks()
        window.update()

    l_name.pack_forget()
    l_player1.pack_forget()
    l_player2.pack_forget()
    e_name.pack_forget()
    e_player1.pack_forget()
    e_player2.pack_forget()
    b.pack_forget()

    return Team(name=e_name.get(), window=window, playerA=e_player1.get(), playerB=e_player2.get())

team_A = fill_team_infos(window)
team_A.set_words(words)

team_B = fill_team_infos(window)
team_B.set_words(words)

def change_team(window):
    label = tk.Label(window, text="À l'autre équipe !", anchor=tk.CENTER, height=5, width=50)
    b = tk.Button(window ,text="Prêt ?", command=lambda: mutex.put())
    mutex : Mutex = Mutex()
    mutex.take()
    label.pack()
    b.pack()
    while mutex.get_value() == 0:
        window.update_idletasks()
        window.update()
    label.pack_forget()
    b.pack_forget()

def print_scores(window, team_1, team_2, round):
    score_team_1 = tk.Label(window,
                            text=f"Score de l'équipe {team_1.get_name()} : {team_1.get_score()}",
                            anchor=tk.CENTER,
                            font=('calibri', 20, 'bold'),)
    score_team_2 = tk.Label(window,
                            text=f"Score de l'équipe {team_2.get_name()} : {team_2.get_score()}",
                            anchor=tk.CENTER,
                            font=('calibri', 20, 'bold'))
    
    b = tk.Button(window ,text='Manche suivante' if round < 3 else 'Fin', command=lambda: mutex.put())
    mutex : Mutex = Mutex()
    mutex.take()
    score_team_1.pack()
    score_team_2.pack()
    b.pack()
    while mutex.get_value() == 0:
        window.update_idletasks()
        window.update()
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

    label = tk.Label(window, text=f'Manche {round} : {todo}', anchor=tk.CENTER, height=5, width=50)
    b = tk.Button(window ,text='Prêt ?', command=lambda: mutex.put(), height=7, width=20)
    mutex : Mutex = Mutex()
    mutex.take()
    label.pack()
    b.pack()
    while mutex.get_value() == 0:
        window.update_idletasks()
        window.update()
    label.pack_forget()
    b.pack_forget()


i = 0
teams = [team_A, team_B]

for round in range(1,4):
    print_round(window, round)
    teams[i%2].play_turn()
    i += 1
    while words.nb_remaining_words() > 0:
        change_team(window)
        teams[i%2].play_turn()
        i += 1

    words.reset()
    print_scores(window, team_A, team_B, round)
