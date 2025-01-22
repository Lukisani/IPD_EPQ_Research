from strategies import*
from tournament import*

scores, results = duel(Random(), TitForTat(), rounds=20)
print(scores)
print(results)

import matplotlib.pyplot as plt
import seaborn as sns

def visualize_duel_results(scores, results):
    # Plotting scores over rounds
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='Round', y=scores.keys(), data=results)
    plt.title('Score Progression Over Rounds', fontsize=16)
    plt.xlabel('Round', fontsize=14)
    plt.ylabel('Score', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(title='Player', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

    # Heatmap of moves (C for Cooperate, D for Defect)
    plt.figure(figsize=(12, 6))
    sns.heatmap(results.drop(columns=['Round']), cmap='coolwarm', annot=True, fmt='s')
    plt.title('Move Distribution Over Rounds', fontsize=16)
    plt.xlabel('Round', fontsize=14)
    plt.ylabel('Player', fontsize=14)
    plt.tight_layout()
    plt.show()

# Example usage:
# Assuming `scores` and `results` are the outputs from the `duel` function
visualize_duel_results(scores, results)
