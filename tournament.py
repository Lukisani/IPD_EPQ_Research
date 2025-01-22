import pandas as pd
import matplotlib.pyplot as plt

def play_match(player1, player2, rounds):
    '''Plays a match between two players'''

    player1.reset()
    player2.reset()

    for _ in range(rounds):
        p1_move = player1.strategy(player2.history)
        p2_move = player2.strategy(player1.history)

        # Update histories
        player1.history.append(p1_move)
        player2.history.append(p2_move)

        # Update scores
        if p1_move == 'C' and p2_move == "C":
            player1.score += 3
            player2.score += 3
        elif p1_move == "C" and p2_move == "D":
            player1.score += 0
            player2.score += 5
        elif p1_move == "D" and p2_move == "C":
            player1.score += 5
            player2.score += 0
        else:
            player1.score += 1
            player2.score += 1

def run_basic_tournament(players, rounds=100, average=3):
    '''Runs basic tournament with round-robin format between every strategy included, not including noise'''
    scores = {player.name: 0 for player in players} # Dictionary to store the results of the tournament
    results = {}
    matchups_played = set() # Set to keep track of which matchups have already occurred

    for i, player1 in enumerate(players):
        for j,player2 in enumerate(players):
            matchup = tuple(sorted([player1.name, player2.name]))
            if matchup in matchups_played:
                continue  # Skip this matchup if it's already played

            # Record this matchup as played
            matchups_played.add(matchup)

            # Play the match
            play_match(player1, player2, rounds)

            # Store the result (can store both scores if needed)

            results[(player1.name, player2.name)] = (player1.score, player2.score)
            scores[player1.name] += player1.score
            if player1.name != player2.name: # Prevents same player from adding score to itself twice (when played against itself)
                # Automatically chooses first player if both the same
                scores[player2.name] += player2.score
    
    results = pd.DataFrame(results.items(), columns=['Match', 'Score'])
    scores = pd.DataFrame(scores.items(), columns=['Player', 'Score'])

    scores = scores.sort_values(by='Score', ascending=False).reset_index(drop=True)

    return results, scores

def duel(player1, player2, rounds=100, average=3):

    '''To view a full one-on-one match between two strategies for analysis'''

    play_match(player1, player2, rounds)

    scores = {
        player1.name : player1.score,
        player2.name : player2.score
    }

    results = {
        'Round' : list(range(1, rounds+1)),
        player1.name : player1.history,
        player2.name : player2.history
        }
    
    results = pd.DataFrame(results).T
    return scores, results