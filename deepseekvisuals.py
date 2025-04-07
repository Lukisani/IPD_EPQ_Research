import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_tournament_results(folder_path):
    """Main visualization function that creates three plots from saved tournament data"""
    # Load data from CSV files
    results_df, scores_df = load_tournament_data(folder_path)
    
    # Create visualization subplots
    fig, axs = plt.subplots(2, 2, figsize=(20, 18))
    
    # 1. Overall Performance Bar Chart
    plot_overall_scores(scores_df, axs[0, 0])
    
    # 2. Pairwise Performance Heatmap
    plot_pairwise_heatmap(results_df, axs[0, 1])
    
    # 3. Strategy Interaction Network
    plot_interaction_network(results_df, axs[1, 0])
    
    # 4. Score Distribution Radar Chart
    plot_radar_chart(results_df, axs[1, 1])
    
    plt.tight_layout()
    plt.show()

def load_tournament_data(folder_path):
    """Load results and scores from CSV files"""
    results_path = os.path.join(folder_path, [f for f in os.listdir(folder_path) if 'results' in f][0])
    scores_path = os.path.join(folder_path, [f for f in os.listdir(folder_path) if 'scores' in f][0])
    
    results_df = pd.read_csv(results_path)
    scores_df = pd.read_csv(scores_path)
    
    return results_df, scores_df

def plot_overall_scores(scores_df, ax):
    """Bar chart of total scores for each strategy"""
    scores_df = scores_df.sort_values('Score', ascending=False)
    sns.barplot(x='Score', y='Player', data=scores_df, ax=ax, palette='viridis')
    ax.set_title('Total Tournament Scores\n(Higher is Better)', fontsize=14)
    ax.set_xlabel('Average Score per Matchup', fontsize=12)
    ax.set_ylabel('Strategy', fontsize=12)
    ax.grid(True, alpha=0.3)

def plot_pairwise_heatmap(results_df, ax):
    """Heatmap showing average scores between strategy pairs"""
    # Create symmetric matrix of pairwise interactions
    matrix_df = pd.pivot_table(results_df, 
                             values='player1score', 
                             index='player1', 
                             columns='player2',
                             fill_value=0)
    
    # Make matrix symmetric by adding transposed values
    symmetric_matrix = (matrix_df + matrix_df.T) / 2
    
    sns.heatmap(symmetric_matrix, annot=True, fmt=".1f", cmap="YlGnBu", ax=ax)
    ax.set_title('Pairwise Performance Heatmap\n(Average Score per Interaction)', fontsize=14)
    ax.set_xlabel('Opponent Strategy', fontsize=12)
    ax.set_ylabel('Focal Strategy', fontsize=12)

def plot_interaction_network(results_df, ax):
    """Network graph showing strategy dominance relationships"""
    # Calculate net advantage between strategies
    network_data = []
    strategies = pd.unique(results_df[['player1', 'player2']].values.ravel())
    
    for strat in strategies:
        mask = results_df['player1'] == strat
        avg_score = results_df[mask]['player1score'].mean()
        network_data.append({'Strategy': strat, 'Score': avg_score})
    
    network_df = pd.DataFrame(network_data)
    
    # Create bubble chart visualization
    sns.scatterplot(x=range(len(network_df)), y='Score', size='Score',
                    hue='Strategy', data=network_df, ax=ax, sizes=(100, 500),
                    palette='tab20', legend=False)
    
    ax.set_xticks(range(len(network_df)))
    ax.set_xticklabels(network_df['Strategy'], rotation=45, ha='right')
    ax.set_title('Strategy Dominance Network\n(Larger Bubbles = Better Overall Performance)', fontsize=14)
    ax.set_xlabel('Strategies', fontsize=12)
    ax.set_ylabel('Average Score', fontsize=12)
    ax.grid(True, alpha=0.3)

def plot_radar_chart(results_df, ax):
    """Radar chart showing performance across different metrics"""
    # Calculate performance metrics
    metrics = {
        'Cooperation Rate': results_df.groupby('player1')['player1score'].mean(),
        'Max Score': results_df.groupby('player1')['player1score'].max(),
        'Min Score': results_df.groupby('player1')['player1score'].min(),
        'Score Consistency': 1/(results_df.groupby('player1')['player1score'].std() + 1e-6)
    }
    
    # Normalize metrics for radar chart
    metrics_df = pd.DataFrame(metrics)
    normalized_df = (metrics_df - metrics_df.min()) / (metrics_df.max() - metrics_df.min())
    
    # Plot radar chart
    angles = [n / float(len(normalized_df.columns)) * 2 * 3.14159 for n in range(len(normalized_df.columns))]
    angles += angles[:1]  # Close the circle
    
    for idx, row in normalized_df.iterrows():
        values = row.values.tolist()
        values += values[:1]
        ax.fill(angles, values, alpha=0.25)
        ax.plot(angles, values, label=idx)
    
    ax.set_theta_offset(3.14159 / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids([a * 180/3.14159 for a in angles[:-1]], metrics_df.columns)
    ax.set_title('Performance Radar Chart\n(Normalized Metrics Comparison)', fontsize=14)
    ax.legend(bbox_to_anchor=(1.3, 1))

# Usage example:
visualize_tournament_results('game_stats/basic_tournaments/basic_rnds=100_avg=10')