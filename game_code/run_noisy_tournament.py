import pandas as pd
import os, sys
import csv

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(PARENT_DIR)
sys.path.append(PARENT_DIR)

from strategies import*
from noisy_tournament import*
from files import*

direc = ObjectView(get_direc())



players = [TitForTat(), AlwaysCooperate(), AlwaysDefect(), TitForTwoTats(), Random(), Alternator(), NotNiceTitForTat(),
           Friedman(), Pavlov(), Prober(), Tester(), Joss(), SoftMajority(), AdaptiveTitForTat(), Punisher(),
           Extortioner(), Retaliator(), Spiteful()]

# results, scores = run_noisy_tournament(players, rounds=100)
# print(results)
# print(scores)

# save_csv_file(results, './game_stats', 'match_results_even_better.csv')
# save_csv_file(scores, './game_stats', 'player_scores_even_better.csv')
# saves tournament results as csv files for later use

def average_noisy_tournament(rounds=100, average=10, noise=0, reward=3, temptation=5, sucker=0, punishment=1):
    print('rounds=', rounds)
    print()
    print()
    list_of_results = []
    list_of_scores = []

    for _ in range(average):
        results, scores = run_noisy_tournament(players, rounds=rounds,
        noise=noise, reward=reward, temptation=temptation, sucker=sucker, punishment=punishment)

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

    # print(average_results)
    # print(average_scores)

    new_folder_name = 'noisy_rnds={}_avg={}'.format(rounds, average)
    new_folder_path = os.path.join(direc.noisy_tournaments, new_folder_name)
    create_folder(new_folder_path)

    save_csv_file(average_results, new_folder_path, f'noisy_results_rnds={rounds}_avg={average}')
    save_csv_file(average_scores, new_folder_path, f'noisy_scores_rnds={rounds}_avg={average}')

    #kwargs for metadata file
    meta = {
        'Type' : 'noisy_tournament',
        'Rounds' : rounds,
        'Average' : average,
        'Noise' : noise,
        'Reward' : reward,
        'Temptation' : temptation,
        'Sucker' : sucker,
        'Punishment' : punishment
    }

    create_meta_file(new_folder_path, 'metadata.txt', **meta)

average_noisy_tournament()

# scores, results = duel(TitForTat(),TitForTat(), rounds=20, noise=.1)
# print(scores)
# print(results)