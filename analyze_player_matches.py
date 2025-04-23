# pick off csv files of tournament to make separate csv file for each player

import pandas as pd
import os, sys
import ast
from files import*

direc = ObjectView(get_direc())

def get_player_stats(folder_directory, filename):
    # try:
    results = pd.read_csv(f'{folder_directory}/{filename}') # Extracts csv file
    print(results)
    
    new_folder_name = 'player_stats'
    new_folder_path = os.path.join(folder_directory, new_folder_name)
    create_folder(new_folder_path)

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
        save_csv_file(player_results, f'{folder_directory}/{new_folder_name}', f"{player}.csv")
    # except FileNotFoundError:
    #     print('Error, file not found')
    # except:
    #     print('Error')

folder_directory = './game_stats/basic_tournaments/basic_rnds=100_avg=10'
filename = 'basic_results_rnds=100_avg=10.csv'

get_player_stats(folder_directory, filename)
