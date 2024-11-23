import tkinter as tk
import tkinter.font as tkFont

from lib.mutex import Mutex

from team import Team
import config as cfg

tkFont.nametofont("TkDefaultFont").configure(family='calibri', size=16, weight='bold')

def refreshUntilMutex(mutex):
    """
        Updates the window as long as the given mutex is taken.
        :param mutex: The mutex for which we must wait for release
    """
    while mutex.get_value() == 0:
        cfg.window.update()

def init_window():
    cfg.window.title("Times Up")
    cfg.window.geometry('1200x700')

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

def print_round(round, next_team_to_play : Team):
    if round == 1:
        todo = "il faut deviner à l'aide de phrases."
    elif round == 2:
        todo = "il faut deviner à l'aide d'un mot."
    else:
        todo = "il faut deviner à l'aide de mimes."

    label = tk.Label(cfg.window, text=f'Manche {round} : {todo}', height=5, width=50)
    label.pack(anchor=tk.CENTER)
    print_guesser(next_team_to_play)
    label.pack_forget()

def print_guesser(team : Team):
    label = tk.Label(cfg.window,
                     text=f"{team.get_name()}, c'est à {team.get_spy()} " \
                        + f"de faire deviner à {team.get_guesser()}")
    mutex : Mutex = Mutex()
    mutex.take()
    b = tk.Button(cfg.window, text="Prêt ?", command=mutex.put, height=7, width=20)
    label.pack()
    b.pack()
    refreshUntilMutex(mutex)
    label.pack_forget()
    b.pack_forget()
