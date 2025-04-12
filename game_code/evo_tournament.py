import pandas as pd
import os, sys
import csv

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(PARENT_DIR)
sys.path.append(PARENT_DIR)

from strategies import*
from noisy_tournament_for_evo import*
from files import*

direc = ObjectView(get_direc())




players = [TitForTat(), AlwaysCooperate(), AlwaysDefect(), TitForTwoTats(), Random(), Alternator(), NotNiceTitForTat(),
           Friedman(), Pavlov(), Prober(), Tester(), Joss(), SoftMajority(), AdaptiveTitForTat(), Punisher(),
           Extortioner(), Retaliator(), Spiteful()]





def evolution_tournament(initial_players, generations, num_alter=3, rounds=10, noise=0, 
                        reward=3, temptation=5, sucker=0, punishment=1):
    """
    Simulates an evolutionary tournament over multiple generations.
    
    Parameters:
        initial_players (list): List of Player instances representing starting population
        generations (int): Number of generations to simulate
        rounds, noise, reward, temptation, sucker, punishment: Tournament parameters
        
    Returns:
        tuple: (population_history, score_history) tracking evolution of strategies
    """
    # Initialize population with clones to avoid modifying original players
    population = [p.clone() for p in initial_players]
    
    # Track population composition and average scores per generation
    population_history = []
    score_history = []

    for gen in range(generations):
        # Reset all players before the tournament
        for player in population:
            player.reset()
        
        # Run tournament (we only need the scores_df here)
        _, scores_df = run_noisy_tournament(population, reward, temptation, 
                                          sucker, punishment, rounds, noise)
        print(scores_df)
        
        # Create a score mapping for all players
        score_mapping = {player: player.score for player in population}
        
        # Calculate strategy statistics
        strategy_stats = {}
        for player in population:
            if player.name not in strategy_stats:
                strategy_stats[player.name] = {
                    'count': 0,
                    'total_score': 0
                }
            strategy_stats[player.name]['count'] += 1
            strategy_stats[player.name]['total_score'] += player.score
        
        # print(strategy_stats)
        
        # Record population composition
        composition = {name: stats['count'] for name, stats in strategy_stats.items()}
        population_history.append(composition)
        
        # Record average scores
        avg_scores = {name: stats['total_score']/stats['count'] 
                     for name, stats in strategy_stats.items()}
        score_history.append(avg_scores)
        
        # Evolutionary selection - sort by individual scores
        population.sort(key=lambda x: x.score, reverse=True)

        # names = []
        # for i in population:
        #     names.append(i.name)
        # print('old pop:',names)
        
        # Remove bottom 3 and duplicate top 3
        new_population = population[:num_alter*-1]  # Keep all but last num_alter (default 3)
        top_performers = population[:num_alter]  # Get top num_alter (default 3)
        
        # Add clones of top performers
        new_population.extend([p.clone() for p in top_performers])
        
        # Update population for next generation
        population = new_population
        
        # names = []
        # for i in population:
        #     names.append(i.name)
        # print('new pop:', names)

        # names = []
        # for i in population:
        #     names.append(i.name)
        # print(names)

    return population_history, score_history

# Initialize population
players = [
    TitForTat(), TitForTat(), TitForTat(), TitForTat(), TitForTat(),
    AlwaysDefect(), AlwaysDefect(), AlwaysDefect(), AlwaysDefect(), AlwaysDefect(),
    AlwaysCooperate(), AlwaysCooperate(), AlwaysCooperate(), AlwaysCooperate(), AlwaysCooperate()
]

# Run evolutionary tournament
pop_history, score_history = evolution_tournament(
    initial_players=players,
    generations=10,
    num_alter=3,
    rounds=10,
    noise=0.0,
    reward=3,
    temptation=5,
    sucker=0,
    punishment=1
)

# print(pop_history)
# print(score_history)

# Analyze results
final_population = pop_history[-1]
print("Final population composition:")
for strategy, count in final_population.items():
    print(f"{strategy}: {count}")

def plot_evolution(population_history, score_history):
    """Visualizes population composition and scores over generations"""
    plt.figure(figsize=(12, 6))
    
    # Population composition plot
    plt.subplot(1, 2, 1)
    df_pop = pd.DataFrame(population_history).fillna(0)
    df_pop.plot.area(stacked=True, ax=plt.gca())
    plt.title("Population Composition")
    plt.xlabel("Generation")
    plt.ylabel("Number of Players")
    
    # Average scores plot
    plt.subplot(1, 2, 2)
    df_scores = pd.DataFrame(score_history)
    df_scores.plot(ax=plt.gca())
    plt.title("Average Scores")
    plt.xlabel("Generation")
    plt.ylabel("Average Score")
    
    plt.tight_layout()
    plt.show()

# Generate visualization
plot_evolution(pop_history, score_history)