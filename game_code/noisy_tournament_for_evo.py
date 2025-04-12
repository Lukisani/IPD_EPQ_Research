import pandas as pd
import matplotlib.pyplot as plt
import random

def noisy_move(move, noise):
    num = random.random()
    if num <= noise:
        if move == 'C':
            move = 'D'
        else:
            move = 'C'
    return move

def play_noisy_match(player1, player2, rounds, noise, reward=3, temptation=5, sucker=0, punishment=1): # Procedure
    '''Plays a match between two players'''

    player1.reset()
    player2.reset()

    for _ in range(rounds):
        p1_move = noisy_move(player1.strategy(player2.history))
        p2_move = noisy_move(player2.strategy(player1.history))

        # Update histories
        player1.history.append(p1_move)
        player2.history.append(p2_move)

        # Update scores
        if p1_move == 'C' and p2_move == "C":
            player1.score += reward
            player2.score += reward
        elif p1_move == "C" and p2_move == "D":
            player1.score += sucker
            player2.score += temptation
        elif p1_move == "D" and p2_move == "C":
            player1.score += temptation
            player2.score += sucker
        else:
            player1.score += punishment
            player2.score += punishment

def run_noisy_tournament(players, reward, temptation, sucker, punishment, rounds=10, noise=0):
    '''Runs noisy tournament with round-robin format between every strategy included, including noise'''
    scores = {player.name: 0 for player in players}  # Dictionary to store the results of the tournament
    results = []  # List to store match results as dictionaries
    matchups_played = set()  # Set to keep track of which matchups have already occurred

    for i, player1 in enumerate(players):
        '''Need to edit so that score doesn't double up when played against itself'''
        for j, player2 in enumerate(players):
            matchup = tuple(sorted([player1.name, player2.name]))
            if matchup in matchups_played:
                continue  # Skip this matchup if it's already played

            # Record this matchup as played
            matchups_played.add(matchup)

            if player1.name == player2.name:
                continue # Skip if player is playing himself
            else:
                # Regular play between distinct strategies
                play_noisy_match(player1, player2, rounds, noise, reward, temptation, sucker, punishment)
                scores[player1.name] += player1.score
                scores[player2.name] += player2.score
                results.append({
                    "player1": player1.name,
                    "player2": player2.name,
                    "player1score": player1.score,
                    "player2score": player2.score
                })

    # Create DataFrame from match results
    results_df = pd.DataFrame(results)

    # Create DataFrame from scores
    scores_df = pd.DataFrame(scores.items(), columns=['Player', 'Score'])

    # Sort players by score
    scores_df = scores_df.sort_values(by='Score', ascending=False).reset_index(drop=True)

    return results_df, scores_df



def duel(player1, player2, rounds, noise, reward=3, temptation=5, sucker=0, punishment=1):

    '''To view a full one-on-one match between two strategies for analysis'''

    if player1.name == player2.name:
        # Self-play: Use clones to avoid shared state
        p1_clone = player1.clone()
        p2_clone = player2.clone()
        play_noisy_match(p1_clone, p2_clone, rounds, noise)
        scores = {
            f'{p1_clone.name}(1)' : p1_clone.score,
            f'{p2_clone.name}(2)' : p2_clone.score}
        results = {
            'Round' : list(range(1, rounds+1)),
            f'{p1_clone.name}(1)' : p1_clone.history,
            f'{p2_clone.name}(2)' : p2_clone.history}     
    else:
        # Regular play between distinct strategies
        play_noisy_match(player1, player2, rounds, noise)
        scores = {
            player1.name : player1.score,
            player2.name : player2.score
         }
        results = {
            'Round' : list(range(1, rounds+1)),
            player1.name : player1.history,
            player2.name : player2.history}

    scores = pd.DataFrame(scores.items(), columns=['Player', 'Score'])
    results = pd.DataFrame(results)
    return scores, results

# stuff = [noisy_move('C', 1) for i in range(10)]
# print(stuff)