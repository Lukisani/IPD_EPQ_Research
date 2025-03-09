import pandas as pd

def create_player_csv_from_match_results(input_file):
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Initialize a dictionary to store results for each player
    player_results = {player: {'player1score': 0, 'player2score': 0} for player in pd.unique(df[['player1', 'player2']].values.ravel())}

    # Loop through the matches in the DataFrame
    for _, row in df.iterrows():
        player1 = row['player1']
        player2 = row['player2']
        player1score = row['player1score']
        player2score = row['player2score']

        # Append the score to each player's record
        player_results[player1]['player1score'] += player1score
        player_results[player2]['player2score'] += player2score

    # Create DataFrame for each player's results
    results_data = []
    for player, scores in player_results.items():
        results_data.append({'Player': player, 'Total Player1 Score': scores['player1score'], 'Total Player2 Score': scores['player2score']})

    results_df = pd.DataFrame(results_data)

    return results_df

# Example usage
input_file = 'match_results.csv'  # Path to the input CSV file
player_scores_df = create_player_csv_from_match_results(input_file)
print(player_scores_df)
