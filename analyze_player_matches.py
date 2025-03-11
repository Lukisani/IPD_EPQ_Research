# pick off csv files of tournament to make separate csv file for each player

import pandas as pd
import ast
from files import*

results = pd.read_csv("./game_stats/match_results_better.csv")
print(results)

# Get the list of unique players
players = pd.unique(results[['player1', 'player2']].values.ravel())
    
# Loop over each player
for player in players:
    # Filter the matches where the player is either player1 or player2
    player_matches = results[(results['player1'] == player) | (results['player2'] == player)]
    
    # Prepare a list to store the match details for this player
    player_results = []
    
    # Loop through the filtered matches
    for _, row in player_matches.iterrows():
        if row['player1'] == player:
            player_results.append({
                'player': player,
                'opponent': row['player2'],
                'player score': row['player1score'],
                'opponent score': row['player2score']
            })
        else:
            player_results.append({
                'player': player,
                'opponent': row['player1'],
                'player score': row['player2score'],
                'opponent score': row['player1score']
            })
    
    # Create DataFrame for the current player
    player_results = pd.DataFrame(player_results)
    
    # Save the player's results to a CSV file
    save_csv_file(player_results, './game_stats/player_stats', f"{player}.csv")


