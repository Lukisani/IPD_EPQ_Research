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

def run_basic_tournament(players, rounds=100):
    '''Runs basic tournament with round-robin format between every strategy included, not including noise'''
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
                # Self-play: Use clones to avoid shared state
                p1_clone = player1.clone()
                p2_clone = player2.clone()
                play_match(p1_clone, p2_clone, rounds)
                scores[player1.name] += p1_clone.score + p2_clone.score
                results.append({
                    "player1": player1.name,
                    "player2": player2.name,
                    "player1score": p1_clone.score,
                    "player2score": p2_clone.score
                })
            else:
                # Regular play between distinct strategies
                play_match(player1, player2, rounds)
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

def duel(player1, player2, rounds=100):

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