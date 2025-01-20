import pandas as pd

from strategies import*
from tournament import*

players = [TitForTat(), AlwaysCooperate(), AlwaysDefect(), TitForTwoTats(), Random()]
results, scores = run_basic_tournament(players, rounds=10)
# print(results)

# import matplotlib.pyplot as plt

# def plot_results(results_df):
#     results_df.plot(kind='bar', x='Match', y='Score', title='Tournament Results')
#     plt.show()

print(scores)
