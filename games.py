import pandas as pd

from strategies import*
from tournament import*

players = [TitForTat(), AlwaysCooperate(), AlwaysDefect(), TitForTwoTats(), Random()]
results, scores = run_basic_tournament(players, rounds=10)
results_df = pd.DataFrame(results.items(), columns=['Match', 'Score'])
scores_df = pd.DataFrame(scores.items(), columns=['Player', 'Score'])
print(results_df)

# import matplotlib.pyplot as plt

# def plot_results(results_df):
#     results_df.plot(kind='bar', x='Match', y='Score', title='Tournament Results')
#     plt.show()

print(scores_df)
