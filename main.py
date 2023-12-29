# Tirer des "cartes"/"mots"/"noms propres" dans un dictionnaire
# Les équipes jouent les unes après les autres
# 3 manches
# Faut pouvoir compter les points
# Pptés des mots : ils appartiennent à une équipe
# Faut un compteur

from team import *
from words import *
from random import sample

NB_WORDS_TO_GUESS = 6

# Construct the words to play with
with open('dictionnaire/test') as f:
    words = list(map(lambda x: x.strip('\n'), f.readlines()))

words_to_play = sample(words, k=NB_WORDS_TO_GUESS)
words = Words(words_to_play)

name_team_A = input('Nom équipe 1 : ')
# player_1_team_A = input('Nom joueur 1 : ')
# player_2_team_A = input('Nom joueur 2 : ')
#team_A = Team(name=name_team_A, playerA=player_1_team_A, playerB=player_2_team_A)
team_A = Team(name=name_team_A)
team_A.set_words(words)


name_team_B = input('Nom équipe 2 : ')
# player_1_team_B = input('Nom joueur 1 : ')
# player_2_team_B = input('Nom joueur 2 : ')
#team_B = Team(name=name_team_B, playerA=player_1_team_B, playerB=player_2_team_B)
team_B = Team(name=name_team_B)
team_B.set_words(words)

for round in range(1,4):
    print(f'Manche {round}')
    while words.nb_remaining_words() > 0:
        # A turn takes place
        team_A.play_turn()
        print("\n À l'autre équipe ! \n")
        team_B.play_turn()

    words.reset()
    print(f"Score de l'équipe {team_A.get_name()} : {team_A.get_score()}")
    print(f"Score de l'équipe {team_B.get_name()} : {team_A.get_score()}")
