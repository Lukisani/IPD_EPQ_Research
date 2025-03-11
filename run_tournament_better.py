import pandas as pd
import os, sys
import csv

from strategies import*
from tournament_better import*
from files import*

players = [TitForTat(), AlwaysCooperate(), AlwaysDefect(), TitForTwoTats(), Random(), Alternator(), NotNiceTitForTat(),
           Friedman(), Pavlov(), Prober(), Tester(), Joss(), SoftMajority(), AdaptiveTitForTat(), Punisher(),
           Extortioner(), Retaliator(), Spiteful()]
# results, scores = run_basic_tournament(players, rounds=100)
# print(results)
# print(scores)

# save_csv_file(results, './game_stats', 'match_results_even_better.csv')
# save_csv_file(scores, './game_stats', 'player_scores_even_better.csv')
# saves tournament results as csv files for later use

def average_basic_tournament(rounds=10, average=5):
    list_of_results = []
    list_of_scores = []

    for _ in range(average):
        results, scores = run_basic_tournament(players, rounds=rounds)
        list_of_results.append(results)
        list_of_scores.append(scores)

    # Sum all DataFrames in the list element-wise
    sum_results = pd.concat(list_of_results).groupby(level=0).sum(numeric_only=True)
    sum_scores = pd.concat(list_of_scores).groupby(level=0).sum(numeric_only=True)
    
    # Calculate the average by dividing by the number of tournaments
    average_results = sum_results / average
    average_scores = sum_scores / average
    
    # Add non-numeric columns back to the results DataFrame
    average_results = list_of_results[0][['player1', 'player2']].join(average_results)
    average_scores = list_of_scores[0][['Player']].join(average_scores)

    print(average_results)
    print(average_scores)

average_basic_tournament()