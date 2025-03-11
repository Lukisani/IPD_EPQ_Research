import pandas as pd
import os, sys
import csv

from strategies import*
from delete_later.tournament import*
from files import*

players = [TitForTat(), AlwaysCooperate(), AlwaysDefect(), TitForTwoTats(), Random(), Alternator(), NotNiceTitForTat(),
           Friedman(), Pavlov(), Prober(), Tester(), Joss(), SoftMajority(), AdaptiveTitForTat(), Punisher(),
           Extortioner(), Retaliator(), Spiteful()]
results, scores = run_basic_tournament(players, rounds=10)
print(results)
print(scores)

save_csv_file(results, './game_stats', 'match_results_original.csv')
save_csv_file(scores, './game_stats', 'player_scores_original.csv')
# saves tournament results as csv files for later use