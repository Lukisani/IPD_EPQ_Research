import pandas as pd
import os, sys
import csv

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(PARENT_DIR)
sys.path.append(PARENT_DIR)

from strategies import*
from tournaments import*
from files import*

direc = ObjectView(get_direc())



players = [TitForTat(), AlwaysCooperate(), AlwaysDefect(), TitForTwoTats(), Random(), Alternator(), NotNiceTitForTat(),
           Friedman(), Pavlov(), Prober(), Tester(), Joss(), SoftMajority(), AdaptiveTitForTat(), Punisher(),
           Extortioner(), Retaliator(), Spiteful()]

# results, scores = run_basic_tournament(players, rounds=100)
# print(results)
# print(scores)

# save_csv_file(results, './game_stats', 'match_results_even_better.csv')
# save_csv_file(scores, './game_stats', 'player_scores_even_better.csv')
# saves tournament results as csv files for later use

def average_basic_tournament(rounds=100, average=10, reward=3, temptation=5, sucker=0, punishment=1):
    list_of_results = []
    list_of_scores = []

    for _ in range(average):
        results, scores = run_basic_tournament(players, rounds=rounds,
        reward=reward, temptation=temptation, sucker=sucker, punishment=punishment)

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

    # Saves results all under one folder
    new_folder_name = 'basic_rnds={}_avg={}'.format(rounds, average)
    new_folder_path = os.path.join(direc.basic_tournaments, new_folder_name)
    create_folder(new_folder_path)

    save_csv_file(average_results, new_folder_path, f'basic_results_rnds={rounds}_avg={average}')
    save_csv_file(average_scores, new_folder_path, f'basic_scores_rnds={rounds}_avg={average}')

    #kwargs for metadata file
    meta = {
        'Type' : 'basic_tournament',
        'Rounds' : rounds,
        'Average' : average,
        'Reward' : reward,
        'Temptation' : temptation,
        'Sucker' : sucker,
        'Punishment' : punishment
    }

    create_meta_file(new_folder_path, 'metadata.txt', **meta)



average_basic_tournament()

# scores, results = duel(TitForTat(), TitForTat(), rounds=100, reward=3, temptation=5, sucker=0, punishment=1)
# print(scores)
# print(results)