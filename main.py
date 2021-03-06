import datetime
import time

import numpy as np
from marius.marius_ai import ai as marius
from johannes.johannes_ai import pokerAI as johannes
from mikkel.mikkel_ai import My_Experimenter_AI2 as mikkel
from mikkel.mikkel_ai2 import My_Keras_SL_AI as mikkel2

import game


def play_ais():
    win_counter = np.zeros(4)
    input_players = [marius("Marius"), johannes("Johannes"), mikkel("Mikkel")]
    for n in range(N_games):
        print(datetime.datetime.now(), " - Game nr:", n, "- Current win rates:", win_counter)
        g = game.Texas_holdem(input_players=input_players, logger=False)
        while len(g.players) > 1:
            g.play_one_step()
        p_id = g.players[0].id_value
        win_counter[p_id] += 1

    print(win_counter)
    print(input_players)
    print(time.time() - start_time)


start_time = time.time()
N_games = 500
N_threads = 4

s_time = time.time()
play_ais()
print(time.time() - s_time)
