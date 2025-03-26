import matplotlib.pyplot as plt
from game_code.tournaments import*
from strategies import*

def plot_moves(results):
    '''
    Plots the moves of each player over the rounds.
    '''
    plt.figure(figsize=(10, 6))
    for player in results.columns[1:]:  # Skip the 'Round' column
        moves = results[player].apply(lambda x: 1 if x == 'C' else 0)  # Convert 'C' to 1, 'D' to 0
        plt.plot(results['Round'], moves, label=player, marker='o', linestyle='-', markersize=5)
    
    plt.title('Moves Over Time')
    plt.xlabel('Round')
    plt.ylabel('Move (C=1, D=0)')
    plt.yticks([0, 1], ['D', 'C'])
    plt.legend()
    plt.grid(True)
    plt.show()

# scores, results = duel(TitForTat(), AlwaysDefect(), rounds=20)
# plot_moves(results)

def plot_cumulative_scores(results, player1_name, player2_name):
    '''
    Plots the cumulative scores of each player over the rounds.
    '''
    # Initialize cumulative scores
    cumulative_score_1 = 0
    cumulative_score_2 = 0
    cumulative_scores_1 = []
    cumulative_scores_2 = []

    for p1_move, p2_move in zip(results[player1_name], results[player2_name]):
        # Calculate scores for this round
        if p1_move == 'C' and p2_move == 'C':
            cumulative_score_1 += 3
            cumulative_score_2 += 3
        elif p1_move == 'C' and p2_move == 'D':
            cumulative_score_1 += 0
            cumulative_score_2 += 5
        elif p1_move == 'D' and p2_move == 'C':
            cumulative_score_1 += 5
            cumulative_score_2 += 0
        else:
            cumulative_score_1 += 1
            cumulative_score_2 += 1
        
        # Append to cumulative scores list
        cumulative_scores_1.append(cumulative_score_1)
        cumulative_scores_2.append(cumulative_score_2)
    
    # Add cumulative scores to results DataFrame
    results['Cumulative_Score_1'] = cumulative_scores_1
    results['Cumulative_Score_2'] = cumulative_scores_2
    
    # Plot cumulative scores
    plt.figure(figsize=(10, 6))
    plt.plot(results['Round'], results['Cumulative_Score_1'], label=f'{player1_name} Cumulative Score', marker='o', linestyle='-')
    plt.plot(results['Round'], results['Cumulative_Score_2'], label=f'{player2_name} Cumulative Score', marker='o', linestyle='-')
    plt.title('Cumulative Scores Over Time')
    plt.xlabel('Round')
    plt.ylabel('Cumulative Score')
    plt.legend()
    plt.grid(True)
    plt.show()

# scores, results = duel(TitForTat(), AlwaysDefect(), rounds=20)
# plot_cumulative_scores(results, TitForTat().name, AlwaysDefect().name)

import seaborn as sns

def plot_heatmap(results, player1_name, player2_name):
    '''
    Plots a heatmap of the moves of both players over the rounds.
    '''
    # Convert moves to numerical values
    move_map = {'C': 1, 'D': 0}
    player1_moves = results[player1_name].map(move_map)
    player2_moves = results[player2_name].map(move_map)
    
    # Create a DataFrame for the heatmap
    heatmap_data = pd.DataFrame({
        'Round': results['Round'],
        player1_name: player1_moves,
        player2_name: player2_moves
    }).set_index('Round')
    
    plt.figure(figsize=(10, 6))
    sns.heatmap(heatmap_data.T, cmap='RdYlGn', annot=True, fmt='d', cbar=False)
    plt.title('Moves Over Time (C=1, D=0)')
    plt.xlabel('Round')
    plt.ylabel('Player')
    plt.show()

# scores, results = duel(TitForTat(), AlwaysDefect(), rounds=20)
# plot_heatmap(results, 'Tit_for_tat', 'Always_defect')

def plot_final_scores(scores):
    '''
    Plots a bar chart of the final scores.
    '''
    plt.figure(figsize=(8, 5))
    plt.bar(scores['Player'], scores['Score'], color=['blue', 'orange'])
    plt.title('Final Scores')
    plt.xlabel('Player')
    plt.ylabel('Score')
    plt.show()

# scores, results = duel(TitForTat(), AlwaysDefect(), rounds=20)
# plot_final_scores(scores)

def combined_visualization(scores, results, player1_name, player2_name):
    '''
    Combines move plot, cumulative scores, and final scores into a single figure.
    '''
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Moves Over Time
    plt.subplot(2, 2, 1)
    for player in results.columns[1:]:
        moves = results[player].apply(lambda x: 1 if x == 'C' else 0)
        plt.plot(results['Round'], moves, label=player, marker='o', linestyle='-', markersize=5)
    plt.title('Moves Over Time')
    plt.xlabel('Round')
    plt.ylabel('Move (C=1, D=0)')
    plt.yticks([0, 1], ['D', 'C'])
    plt.legend()
    plt.grid(True)
    
    # Plot 2: Cumulative Scores
    plt.subplot(2, 2, 2)
    cumulative_score_1 = 0
    cumulative_score_2 = 0
    cumulative_scores_1 = []
    cumulative_scores_2 = []
    for p1_move, p2_move in zip(results[player1_name], results[player2_name]):
        if p1_move == 'C' and p2_move == 'C':
            cumulative_score_1 += 3
            cumulative_score_2 += 3
        elif p1_move == 'C' and p2_move == 'D':
            cumulative_score_1 += 0
            cumulative_score_2 += 5
        elif p1_move == 'D' and p2_move == 'C':
            cumulative_score_1 += 5
            cumulative_score_2 += 0
        else:
            cumulative_score_1 += 1
            cumulative_score_2 += 1
        cumulative_scores_1.append(cumulative_score_1)
        cumulative_scores_2.append(cumulative_score_2)
    results['Cumulative_Score_1'] = cumulative_scores_1
    results['Cumulative_Score_2'] = cumulative_scores_2
    plt.plot(results['Round'], results['Cumulative_Score_1'], label=f'{player1_name} Cumulative Score', marker='o', linestyle='-')
    plt.plot(results['Round'], results['Cumulative_Score_2'], label=f'{player2_name} Cumulative Score', marker='o', linestyle='-')
    plt.title('Cumulative Scores Over Time')
    plt.xlabel('Round')
    plt.ylabel('Cumulative Score')
    plt.legend()
    plt.grid(True)

    # Plot 3: Heatmap of Moves Over Time
    plt.subplot(2, 2, 3)
    move_map = {'C': 1, 'D': 0}
    player1_moves = results[player1_name].map(move_map)
    player2_moves = results[player2_name].map(move_map)
    heatmap_data = pd.DataFrame({
        'Round': results['Round'],
        player1_name: player1_moves,
        player2_name: player2_moves
    }).set_index('Round')
    sns.heatmap(heatmap_data.T, cmap='RdYlGn', annot=True, fmt='d', cbar=False)
    plt.title('Moves Over Time (C=1, D=0)')
    plt.xlabel('Round')
    plt.ylabel('Player')
    plt.grid(True)

    # Plot 4: Final Scores
    plt.subplot(2, 2, 4)
    plt.bar(scores['Player'], scores['Score'], color=['blue', 'orange'])
    plt.title('Final Scores')
    plt.xlabel('Player')
    plt.ylabel('Score')
    
    plt.tight_layout()
    plt.show()

scores, results = duel(TitForTat(), Random(), rounds=20)
combined_visualization(scores, results, TitForTat().name, Random().name)