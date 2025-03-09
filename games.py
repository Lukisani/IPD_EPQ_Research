import pandas as pd
import os, sys
import csv

from strategies import*
from tournament import*
from files import*

players = [TitForTat(), AlwaysCooperate(), AlwaysDefect(), TitForTwoTats(), Random(), Alternator(), NotNiceTitForTat(),
           Friedman(), Pavlov(), Prober(), Tester(), Joss(), SoftMajority(), AdaptiveTitForTat(), Punisher(),
           Extortioner(), Retaliator(), Spiteful()]
results, scores = run_basic_tournament(players, rounds=10)
print(results)

# import matplotlib.pyplot as plt

# def plot_results(results_df):
#     results_df.plot(kind='bar', x='Match', y='Score', title='Tournament Results')
#     plt.show()

print(scores)


# import matplotlib.pyplot as plt
# import seaborn as sns

# def visualize_tournament_data(results, scores):
#     # Visualize the scores
#     plt.figure(figsize=(10, 6))
#     sns.barplot(x='Score', y='Player', data=scores.sort_values(by='Score', ascending=False), palette='viridis')
#     plt.title('Player Scores in the Tournament', fontsize=16)
#     plt.xlabel('Score', fontsize=14)
#     plt.ylabel('Player', fontsize=14)
#     plt.xticks(fontsize=12)
#     plt.yticks(fontsize=12)
#     plt.tight_layout()
#     plt.show()

#     # Visualize the results (match-level scores)
#     if not results.empty:  # Only plot if results are available
#         results_expanded = results.copy()
#         results_expanded[['Player 1', 'Player 2']] = results_expanded['Match'].apply(pd.Series)
#         results_expanded[['Player 1 Score', 'Player 2 Score']] = results_expanded['Score'].apply(pd.Series)
#         results_melted = pd.melt(
#             results_expanded,
#             id_vars=['Player 1', 'Player 2'],
#             value_vars=['Player 1 Score', 'Player 2 Score'],
#             var_name='Player',
#             value_name='Score'
#         )

#         plt.figure(figsize=(12, 8))
#         sns.boxplot(x='Player', y='Score', data=results_melted, palette='coolwarm')
#         plt.title('Score Distribution Across Matches', fontsize=16)
#         plt.xlabel('Player', fontsize=14)
#         plt.ylabel('Score', fontsize=14)
#         plt.xticks(fontsize=12)
#         plt.yticks(fontsize=12)
#         plt.tight_layout()
#         plt.show()

# # Example usage:
# # Assuming `results` and `scores` are the DataFrames returned by the tournament function
# visualize_tournament_data(results, scores)

import matplotlib.pyplot as plt
import seaborn as sns

def visualize_tournament_data_with_attributes(results, scores, strategies):
    # Creating a dataframe for classifier attributes
    data = []
    for player in strategies:
        for attr, value in player.classifier.items():
            data.append({
                'Player': player.name,
                'Attribute': attr,
                'Value': value
            })
    df_classifier = pd.DataFrame(data)
    
    # Plotting scores
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Score', y='Player', data=scores.sort_values(by='Score', ascending=False), palette='viridis')
    plt.title('Player Scores in the Tournament', fontsize=16)
    plt.xlabel('Score', fontsize=14)
    plt.ylabel('Player', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.savefig('./figures/tournament_standings.pdf')
    plt.show()

    # Plotting attribute-based color coding
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Attribute', y='Value', hue='Player', data=df_classifier, palette='coolwarm', s=100)
    plt.title('Classifier Attributes of Strategies', fontsize=16)
    plt.xlabel('Attribute', fontsize=14)
    plt.ylabel('Value', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('./figures/classifier.pdf')
    plt.show()

    # Visualizing the results
    if not results.empty:
        results_expanded = results.copy()
        results_expanded[['Player 1', 'Player 2']] = results_expanded['Match'].apply(pd.Series)
        results_expanded[['Player 1 Score', 'Player 2 Score']] = results_expanded['Score'].apply(pd.Series)
        results_melted = pd.melt(
            results_expanded,
            id_vars=['Player 1', 'Player 2'],
            value_vars=['Player 1 Score', 'Player 2 Score'],
            var_name='Player',
            value_name='Score'
        )

        plt.figure(figsize=(12, 8))
        sns.boxplot(x='Player', y='Score', data=results_melted, palette='coolwarm')
        plt.title('Score Distribution Across Matches', fontsize=16)
        plt.xlabel('Player', fontsize=14)
        plt.ylabel('Score', fontsize=14)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.tight_layout()
        plt.show()

# Example usage:
# Assuming `results` and `scores` are the DataFrames returned by the tournament function, and `strategies` is a list of strategy instances
visualize_tournament_data_with_attributes(results, scores, players)
