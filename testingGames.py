from strategies import*
from tournament import*

results = duel(TitForTat(), AlwaysDefect(), rounds=20)
results = pd.DataFrame(results)
results = results.T
print(results)