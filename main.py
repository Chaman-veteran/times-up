# Tirer des "cartes"/"mots"/"noms propres" dans un dictionnaire
# Les équipes jouent les unes après les autres
# 3 manches
# Faut pouvoir compter les points
# Pptés des mots : ils appartiennent à une équipe
# Faut un compteur

from team import *
from random import sample

NB_WORDS_TO_GUESS = 3

with open('dictionnaire/test') as f:
    words = list(map(lambda x: x.strip('\n'), f.readlines()))

words_to_play = sample(words, k=NB_WORDS_TO_GUESS)

name_team_A = input('Nom équipe 1 : ')
player_1_team_A = input('Nom joueur 1 : ')
player_2_team_A = input('Nom joueur 2 : ')
team_A = Team(name=name_team_A, playerA=player_1_team_A, playerB=player_2_team_A)
# TODO: donner la référence vers l'objet Words à l'équipe


name_team_B = input('Nom équipe 2 : ')
player_1_team_B = input('Nom joueur 1 : ')
player_2_team_B = input('Nom joueur 2 : ')
team_B = Team(name=name_team_B, playerA=player_1_team_B, playerB=player_2_team_B)
# TODO: donner la référence vers l'objet Words à l'équipe

for round in range(1,4):
    print(f'Manche {round}')
    # TODO: utiliser les méthodes des équipes pour jouer
    # penser à reset les mots utilisés entre rounds
    # gérer les finds de manches (faire des tours)

