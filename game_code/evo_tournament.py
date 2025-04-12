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
    """Evolution with proper instance tracking"""
    population = [deepcopy(p) for p in initial_players]
    population_history = []
    score_history = []

    for gen in range(generations):
        # Reset and run tournament
        for p in population:
            p.reset()
        
        _, scores_df = run_noisy_tournament(population, reward, temptation,
                                          sucker, punishment, rounds, noise)
        
        # Create instance->score mapping
        instance_scores = dict(zip(scores_df['Instance_ID'], scores_df['Score']))
        
        # Sort population by individual performance
        population.sort(key=lambda x: instance_scores.get(id(x), 0), reverse=True)
        
        # Track population by type (using regular dict instead of defaultdict)
        type_counts = {}
        type_scores = {}
        for player in population:
            if player.name not in type_counts:
                type_counts[player.name] = 0
                type_scores[player.name] = []
            type_counts[player.name] += 1
            type_scores[player.name].append(instance_scores.get(id(player), 0))
        
        population_history.append(type_counts)
        score_history.append({k: sum(v)/len(v) for k, v in type_scores.items()})
        
        # Evolutionary step
        new_population = population[:-num_alter] + [deepcopy(p) for p in population[:num_alter]]
        population = new_population

    return population_history, score_history

# Initialize population
players = [
    *[TitForTat() for _ in range(5)],
    *[AlwaysDefect() for _ in range(5)],
    *[AlwaysCooperate() for _ in range(5)]
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
    plt.subplot(1, 3, 1)
    df_pop = pd.DataFrame(population_history).fillna(0)
    df_pop.plot.area(stacked=True, ax=plt.gca())
    plt.title("Population Composition")
    plt.xlabel("Generation")
    plt.ylabel("Number of Players")
    
    # Average scores plot
    plt.subplot(1, 3, 2)
    df_scores = pd.DataFrame(score_history)
    df_scores.plot(ax=plt.gca())
    plt.title("Average Scores")
    plt.xlabel("Generation")
    plt.ylabel("Average Score")

    # Population line graph plot
    plt.subplot(1, 3, 3)
    for strategy in df_pop.columns:
        plt.plot(df_pop.index, df_pop[strategy], label=strategy, marker='o')
    plt.title("Population Trends (Lines)")
    plt.xlabel("Generation")
    plt.ylabel("Number of Players")
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

# Generate visualization
plot_evolution(pop_history, score_history)