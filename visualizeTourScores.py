import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_final_scores(folder_path):
    """
    Creates a bar plot showing the final scores of all strategies from saved tournament data
    
    Args:
        folder_path: Path to the tournament folder containing the CSV files
    """
    # Load the scores data
    scores_file = [f for f in os.listdir(folder_path) if 'scores' in f][0]
    scores_path = os.path.join(folder_path, scores_file)
    scores_df = pd.read_csv(scores_path)
    
    # Sort by score for better visualization
    scores_df = scores_df.sort_values('Score', ascending=False)
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    ax = sns.barplot(x='Score', y='Player', data=scores_df, palette='viridis')
    
    # Customize the plot
    ax.set_title('Final Tournament Scores', fontsize=16, pad=20)
    ax.set_xlabel('Total Score', fontsize=12)
    ax.set_ylabel('Strategy', fontsize=12)
    
    # Add value labels on each bar
    for p in ax.patches:
        width = p.get_width()
        ax.text(width + max(scores_df['Score'])*0.01, 
                p.get_y() + p.get_height()/2., 
                f'{int(width)}', 
                ha='left', va='center', fontsize=10)
    
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Example usage:
plot_final_scores('game_stats/basic_tournaments/basic_rnds=100_avg=10')