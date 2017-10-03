import itertools
import random
import warnings
import threading
import os
import boto3
import json

from collections import namedtuple

from isolation import Board
from sample_players import (RandomPlayer, open_move_score,
                            improved_score, center_score)
from game_agent import *

TIME_LIMIT = 200  # number of milliseconds before timeout

Agent = namedtuple("Agent", ["constructor", "name"])
a1 = Agent(lambda: ImprovedAlphaBetaPlayer(score_fn=improved_score), "normal agent")
a2 = Agent(lambda: ImprovedAlphaBetaPlayer(score_fn=improved_score), "imporved agent")

p1 = a1.constructor()
p2 = a2.constructor()

game = Board(p1, p2)
for _ in range(2):
    move = random.choice(game.get_legal_moves())
    game.apply_move(move)

winner, moves, termination = game.play(time_limit=TIME_LIMIT)

print(winner,len(moves),termination,p1.depths_reached,p2.depths_reached)

winvalue = 1 if p1 == winner else -1
p1_avg_depth = sum(p1.depths_reached)/len(p1.depths_reached)
p2_avg_depth = sum(p2.depths_reached)/len(p2.depths_reached)
print(winvalue,len(moves),termination,p1_avg_depth,p2_avg_depth)

