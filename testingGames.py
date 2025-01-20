from strategies import*
from tournament import*

scores, results = duel(Random(), TitForTwoTats(), rounds=20)
print(scores)
print(results)