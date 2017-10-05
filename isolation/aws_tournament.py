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

NUM_MATCHES = 2  # number of matches against each opponent
TIME_LIMIT = 200  # number of milliseconds before timeout
INSTANCES = 250  # number of game agents that will be initiated

Agent = namedtuple("Agent", ["constructor", "name"])
a1 = Agent(lambda: AlphaBetaPlayer(score_fn=improved_score), "imporved agent")
a2 = Agent(lambda: AlphaBetaPlayer(score_fn=custom_score_3), "reachability")

def play_matches():
    g1p1 = a1.constructor()
    g1p2 = a2.constructor()
    g2p1 = a1.constructor()
    g2p2 = a2.constructor()

    stats = []
    for _ in range(NUM_MATCHES):
        games = [Board(g1p1, g1p2), Board(g2p2, g2p1)]
        for _ in range(2):
            move = random.choice(games[0].get_legal_moves())
            for game in games:
                game.apply_move(move)
        stats.append(play_out_with_stats(games[0],g1p1,g1p2))
        stats.append(play_out_with_stats(games[1],g2p1,g2p2))
    return stats

def play_out_with_stats(game,p1,p2):
    winner, moves, termination = game.play(time_limit=TIME_LIMIT)
    winvalue = 1 if p1 == winner else -1
    p1_avg_depth = sum(p1.depths_reached)/len(p1.depths_reached)
    p2_avg_depth = sum(p2.depths_reached)/len(p2.depths_reached)
    return (winvalue,len(moves),termination,p1_avg_depth,p2_avg_depth)

def handler(event,context):
    stats = play_matches()
    return stats

local_results = []
def fork_local():
    print('Local fork initialized')
    stats = handler({},{})
    local_results.extend(stats)
    print('Local fork finalized')

def swarm_local():
    print('Kicking off local swarm with',INSTANCES,'instances')
    threads = [ threading.Thread(target=fork_local, args=(), kwargs={}) for x in range(INSTANCES) ]
    for thread in threads: thread.start()
    for thread in threads: thread.join()
    report(local_results)

def report(stats):
    #print(stats)
    print(a1.name,'vs',a2.name)
    games = len(stats)
    win_rate = sum( 1 for x in stats if x[0] >= 0)/len(stats) * 100
    game_length = sum( x[1] for x in stats)/len(stats)
    forfeits = sum( 1 for x in stats if x[2] == 'forfeit')
    timeouts = sum( 1 for x in stats if x[2] == 'timeout')
    p1_depth = sum( x[3] for x in stats)/len(stats)
    p2_depth = sum( x[4] for x in stats)/len(stats)

    print('Games:',games)
    print(a1.name,'Wins:',win_rate)
    print(a2.name,'Wins:',100-win_rate)
    print('Avg Game Length:',game_length)
    if forfeits: print('!!!Forfeits:',forfeits)
    if timeouts: print('!!!Timeouts:',timeouts)
    print(a1.name,'Avg. Depth',p1_depth)
    print(a2.name,'Avg. Depth',p2_depth)

def fork_aws():
    client = boto3.client('lambda')
    res = client.invoke(FunctionName="IsolationBot",InvocationType="RequestResponse",Payload="")
    if res['StatusCode'] != 200:
        print('AWS Lambda Error',res.FunctionError)
        return []
    body = res['Payload'].read()
    jbody = json.loads(body)
    if 'errorMessage' in jbody:
        print('execution error',jbody['errorMessage'])
        return []
    local_results.extend(jbody)

def swarm_aws():
    client = boto3.client('lambda')
    print('Updating Lambda function...')
    os.system("./scripts/upload.sh")
    print('Running agents')
    threads = [ threading.Thread(target=fork_aws, args=(), kwargs={}) for x in range(INSTANCES) ]
    for thread in threads: thread.start()
    for thread in threads: thread.join()
    report(local_results)

def main():
    swarm_aws()
    return

if __name__ == "__main__":
    main()
