import games

import matplotlib.pyplot as plt
import seaborn as sns

def visualize_tournament_data(results, scores):
    # Visualize the scores
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Score', y='Player', data=scores.sort_values(by='Score', ascending=False), palette='viridis')
    plt.title('Player Scores in the Tournament', fontsize=16)
    plt.xlabel('Score', fontsize=14)
    plt.ylabel('Player', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.show()

    # Visualize the results (match-level scores)
    if not results.empty:  # Only plot if results are available
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
# Assuming `results` and `scores` are the DataFrames returned by the tournament function
visualize_tournament_data(results, scores) # ignore for now
