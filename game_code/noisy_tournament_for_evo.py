import pandas as pd
import matplotlib.pyplot as plt
import random
from copy import deepcopy

def noisy_move(move, noise):
    num = random.random()
    if num <= noise:
        if move == 'C':
            move = 'D'
        else:
            move = 'C'
    return move

def play_noisy_match(player1, player2, rounds, noise, reward=3, temptation=5, sucker=0, punishment=1): # Procedure
    '''Plays a match between two players'''

    player1.reset()
    player2.reset()

    for _ in range(rounds):
        p1_move = noisy_move(player1.strategy(player2.history), noise)
        p2_move = noisy_move(player2.strategy(player1.history), noise)


        # Update histories
        player1.history.append(p1_move)
        player2.history.append(p2_move)

        # Update scores
        if p1_move == 'C' and p2_move == "C":
            player1.score += reward
            player2.score += reward
        elif p1_move == "C" and p2_move == "D":
            player1.score += sucker
            player2.score += temptation
        elif p1_move == "D" and p2_move == "C":
            player1.score += temptation
            player2.score += sucker
        else:
            player1.score += punishment
            player2.score += punishment

def run_noisy_tournament(players, reward, temptation, sucker, punishment, rounds=10, noise=0):
    '''Runs noisy tournament with round-robin format between every strategy included, including noise'''
    scores = {player: 0 for player in players}  # Individual total scores
    match_counts = {player: 0 for player in players}  # Matches per player
    results = []  # For storing match details
    seen_pairs = set()  # Track played matchups using frozenset of ids

    for i, player1 in enumerate(players):
        for j, player2 in enumerate(players):
            # Skip self-play and duplicate matchups
            if player1 is player2:
                continue
                
            pair = frozenset({id(player1), id(player2)})
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)

            # Clone players to isolate match state
            p1_clone = deepcopy(player1)
            p2_clone = deepcopy(player2)
            
            # Play match with noise
            play_noisy_match(p1_clone, p2_clone, rounds, noise, 
                            reward, temptation, sucker, punishment)
            
            # Record scores
            scores[player1] += p1_clone.score
            scores[player2] += p2_clone.score
            match_counts[player1] += 1
            match_counts[player2] += 1
            
            # Store match results
            results.append({
                "player1": player1.name,
                "player2": player2.name,
                "player1_score": p1_clone.score,
                "player2_score": p2_clone.score,
                "rounds": rounds
            })

    # Calculate average scores per match
    avg_scores = {
        player: total_score / match_counts[player] 
        for player, total_score in scores.items()
    }
    
    # Convert results to DataFrame
    results_df = pd.DataFrame(results)
    
    return results_df, avg_scores



def duel(player1, player2, rounds, noise, reward=3, temptation=5, sucker=0, punishment=1):

    '''To view a full one-on-one match between two strategies for analysis'''

    if player1.name == player2.name:
        # Self-play: Use clones to avoid shared state
        p1_clone = player1.clone()
        p2_clone = player2.clone()
        play_noisy_match(p1_clone, p2_clone, rounds, noise)
        scores = {
            f'{p1_clone.name}(1)' : p1_clone.score,
            f'{p2_clone.name}(2)' : p2_clone.score}
        results = {
            'Round' : list(range(1, rounds+1)),
            f'{p1_clone.name}(1)' : p1_clone.history,
            f'{p2_clone.name}(2)' : p2_clone.history}     
    else:
        # Regular play between distinct strategies
        play_noisy_match(player1, player2, rounds, noise)
        scores = {
            player1.name : player1.score,
            player2.name : player2.score
         }
        results = {
            'Round' : list(range(1, rounds+1)),
            player1.name : player1.history,
            player2.name : player2.history}

    scores = pd.DataFrame(scores.items(), columns=['Player', 'Score'])
    results = pd.DataFrame(results)
    return scores, results

# stuff = [noisy_move('C', 1) for i in range(10)]
# print(stuff)

import pandas as pd
import os, sys
import csv

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(PARENT_DIR)
sys.path.append(PARENT_DIR)

from strategies import*
from noisy_tournament_for_evo import*
from files import*

direc = ObjectView(get_direc())

players = [TitForTat(), AlwaysDefect(), AlwaysCooperate(), TitForTat(), AlwaysDefect(), AlwaysCooperate(), TitForTat(), AlwaysDefect(), AlwaysCooperate()]
results, avg_scores = run_noisy_tournament(players, reward=3, temptation=5, sucker=0, punishment=1, rounds=10, noise=0.0)

print("Match Results:")
print(results.head())

print("\nAverage Scores:")
for player, score in avg_scores.items():
    print(f"{player.name}: {score:.1f}")