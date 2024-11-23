"""
    main.py
    Dictates the structure of the game.
"""

import config as cfg
from team import Team
from ui import print_round, print_guesser, print_scores, fill_team_infos, init_window
from words import Words

playable_words = Words('dictionary/wordlist_fr')
init_window()

team_A : Team = fill_team_infos()
team_A.set_words(playable_words)

team_B : Team = fill_team_infos()
team_B.set_words(playable_words)

teams = [team_A, team_B]

for round in range(1,4):
    print_round(round, next_team_to_play = teams[cfg.turn_picker])
    teams[cfg.turn_picker].play_turn()
    cfg.turn_picker ^= 1
    while playable_words.nb_remaining_words() > 0:
        print_guesser(teams[cfg.turn_picker])
        teams[cfg.turn_picker].play_turn()
        cfg.turn_picker ^= 1

    playable_words.reset()
    print_scores(team_A, team_B, round)
