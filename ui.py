import tkinter as tk
import tkinter.font as tkFont

from lib.mutex import Mutex

from team import Team
import config as cfg

tkFont.nametofont("TkDefaultFont").configure(family='calibri', size=16, weight='bold')

def refreshUntilMutex(mutex):
    while mutex.get_value() == 0:
        cfg.window.update()

def print_scores(team_1, team_2, round):
    score_team_1 = tk.Label(cfg.window,
                            text=f"Score de l'équipe {team_1.get_name()} : {team_1.get_score()}")
    score_team_2 = tk.Label(cfg.window,
                            text=f"Score de l'équipe {team_2.get_name()} : {team_2.get_score()}")
    
    mutex : Mutex = Mutex()
    mutex.take()
    b = tk.Button(cfg.window, text='Manche suivante' if round < 3 else 'Fin', command=mutex.put)
    score_team_1.pack(anchor=tk.CENTER)
    score_team_2.pack(anchor=tk.CENTER)
    b.pack()
    refreshUntilMutex(mutex)
    score_team_1.pack_forget()
    score_team_2.pack_forget()
    b.pack_forget()

def print_round(round):
    if round == 1:
        todo = "il faut deviner à l'aide de phrases."
    elif round == 2:
        todo = "il faut deviner à l'aide d'un mot."
    else:
        todo = "il faut deviner à l'aide de mimes."

    label = tk.Label(cfg.window, text=f'Manche {round} : {todo}', height=5, width=50)
    mutex : Mutex = Mutex()
    mutex.take()
    b = tk.Button(cfg.window, text='Prêt ?', command=mutex.put, height=7, width=20)
    label.pack(anchor=tk.CENTER)
    b.pack()
    refreshUntilMutex(mutex)
    label.pack_forget()
    b.pack_forget()

def print_guesser(team : Team):
    label = tk.Label(cfg.window,
                     text=f"{team.get_guesser()}, c'est à {team.get_spy()} " \
                        + f"de faire deviner à {team.get_guesser()}, {team.get_spy()} t'es prêt ?!")
    mutex : Mutex = Mutex()
    mutex.take()
    b = tk.Button(cfg.window ,text="Prêt ?", command=mutex.put, height=7, width=20)
    label.pack()
    b.pack()
    refreshUntilMutex(mutex)
    label.pack_forget()
    b.pack_forget()

def change_team():
    label = tk.Label(cfg.window, text="À l'autre équipe !", height=5, width=50)
    mutex : Mutex = Mutex()
    mutex.take()
    b = tk.Button(cfg.window, text="Prêt ?", command=mutex.put)
    label.pack(anchor=tk.CENTER)
    b.pack()
    refreshUntilMutex(mutex)
    label.pack_forget()
    b.pack_forget()
