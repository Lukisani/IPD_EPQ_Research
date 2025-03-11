from delete_later.tournament import*
from strategies import*

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

def visualize_duel(results):
    results = results.T  # Transpose back to original structure (rounds as rows)

    plt.figure(figsize=(10, 5))
    
    # Convert actions to numeric values (e.g., Cooperate = 1, Defect = 0)
    player1 = results.columns[1]  # First player
    player2 = results.columns[2]  # Second player

    moves_p1 = [1 if move == 'C' else 0 for move in results[player1]]
    moves_p2 = [1 if move == 'C' else 0 for move in results[player2]]

    plt.plot(results["Round"], moves_p1, marker='o', label=player1, linestyle='-')
    plt.plot(results["Round"], moves_p2, marker='x', label=player2, linestyle='--')

    plt.yticks([0, 1], ['Defect', 'Cooperate'])
    plt.xlabel('Round')
    plt.ylabel('Action')
    plt.title(f'{player1} vs {player2} - Move History')
    plt.legend()
    plt.show()

scores, results = duel(TitForTat(), Random())

def visualize_duel(results):
    results = results.T  # Transpose back to original structure (rounds as rows)

    plt.figure(figsize=(10, 5))
    
    # Convert actions to numeric values (e.g., Cooperate = 1, Defect = 0)
    player1 = results.columns[1]  # First player
    player2 = results.columns[2]  # Second player

    moves_p1 = [1 if move == 'C' else 0 for move in results[player1]]
    moves_p2 = [1 if move == 'C' else 0 for move in results[player2]]

    plt.plot(results["Round"], moves_p1, marker='o', label=player1, linestyle='-')
    plt.plot(results["Round"], moves_p2, marker='x', label=player2, linestyle='--')

    plt.yticks([0, 1], ['Defect', 'Cooperate'])
    plt.xlabel('Round')
    plt.ylabel('Action')
    plt.title(f'{player1} vs {player2} - Move History')
    plt.legend()
    plt.show()


def visualize_scores(results):
    results = results.T
    player1 = results.columns[1]
    player2 = results.columns[2]

    # Simulate scores assuming Cooperate = 3 points, Defect = 0, etc.
    # You might need to replace this with actual scoring from play_match()
    scores_p1 = np.cumsum([3 if move == 'C' else 0 for move in results[player1]])
    scores_p2 = np.cumsum([3 if move == 'C' else 0 for move in results[player2]])

    plt.figure(figsize=(10, 5))
    plt.plot(results["Round"], scores_p1, marker='o', label=f"{player1} Cumulative Score")
    plt.plot(results["Round"], scores_p2, marker='x', label=f"{player2} Cumulative Score")

    plt.xlabel("Round")
    plt.ylabel("Cumulative Score")
    plt.title(f"{player1} vs {player2} - Score Progression")
    plt.legend()
    plt.show()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def visualize_duel_table(results):
    results = results.T  # Transpose so strategies are rows and rounds are columns
    player1, player2 = results.columns[1], results.columns[2]

    # Convert 'C' to 1 (cooperate) and 'D' to 0 (defect)
    mapping = {'C': 1, 'D': 0}
    player1_moves = results[player1].replace(mapping).values.astype(int)
    player2_moves = results[player2].replace(mapping).values.astype(int)

    num_rounds = len(player1_moves)

    # Create figure
    fig, ax = plt.subplots(figsize=(num_rounds / 5, 2))
    ax.set_xlim(0, num_rounds)
    ax.set_ylim(-0.5, 1.5)  # Two rows only

    # Plot cooperation/defection as squares
    for i in range(num_rounds):
        ax.add_patch(plt.Rectangle((i, 1), 1, 1, color='lightgreen' if player1_moves[i] else 'lightcoral'))
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, color='lightgreen' if player2_moves[i] else 'lightcoral'))

    # Formatting
    ax.set_yticks([0.5, 1.5])
    ax.set_yticklabels([player2, player1], fontsize=12)

    # Label every 10 rounds
    xticks = np.arange(0, num_rounds, 10)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticks + 1, fontsize=10)  # Rounds are 1-based

    ax.set_xlabel("Rounds", fontsize=12)
    ax.set_title(f"{player1} vs {player2} - Cooperation/Defection", fontsize=14)

    # Hide frame and ticks for a clean look
    ax.set_frame_on(False)
    ax.tick_params(axis='y', left=False)  # Hide y-axis ticks
    ax.tick_params(axis='x', bottom=False)  # Hide x-axis ticks

    plt.show()

visualize_duel_table(results)