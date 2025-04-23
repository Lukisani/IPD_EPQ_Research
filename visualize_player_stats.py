import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

playerName = 'Adaptive_Tit_For_Tat'
filename = playerName + '.csv'
directory = './delete_later/basic_rnds=100_avg=10/player_stats'

# Load data - ensure correct column names
df = pd.read_csv(f"{directory}/{filename}")

# Rename columns if needed (remove spaces)
df = df.rename(columns={
    'player score': 'player_score',
    'opponent score': 'opponent_score'
})

# Create plot
plt.figure(figsize=(14, 8))
sns.set_style("whitegrid")

# Use a professional color palette
palette = {
    'player_score': '#3498db',  # Nice blue
    'opponent_score': '#e74c3c'  # Complementary red
}

# Create melted dataframe for seaborn
melted_df = pd.melt(df, 
                   id_vars=["opponent"], 
                   value_vars=["player_score", "opponent_score"])

# Plot
ax = sns.barplot(
    data=melted_df,
    x="opponent",
    y="value",
    hue="variable",
    palette=palette,
    saturation=0.85  # Makes colors slightly less intense
)

# Formatting
plt.title(f'{playerName} vs Opponents: Score Comparison', pad=20, fontsize=16)
plt.xlabel('Opponent Strategy', fontsize=12)
plt.ylabel('Total Score', fontsize=12)
plt.xticks(rotation=45, ha='right')

# Improve legend
legend = plt.legend(
    title='Strategy',
    labels=[playerName, 'Opponent'],
    frameon=True,
    framealpha=1,
    edgecolor='black'
)
legend.get_frame().set_facecolor('white')

# Add value labels
for p in ax.patches:
    ax.annotate(
        f"{int(p.get_height())}",
        (p.get_x() + p.get_width() / 2., p.get_height()),
        ha='center',
        va='center',
        xytext=(0, 5),
        textcoords='offset points',
        fontsize=9
    )

plt.tight_layout()

plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load and prepare data
df = pd.read_csv(f"{directory}/{filename}")
df = df.rename(columns={'player score': 'score'})  # Focus on player's scores only

# Create plot
plt.figure(figsize=(12, 6))
sns.set_style("whitegrid")

# Bar plot with custom colors
ax = sns.barplot(
    data=df,
    x='opponent',
    y='score',
    palette=['#4c72b0' if x != playerName else '#55a868' for x in df['opponent']]
)

# Highlight self-play matchup
for i, label in enumerate(ax.get_xticklabels()):
    if label.get_text() == playerName:
        ax.patches[i].set_facecolor('#55a868')

# Formatting
plt.title(f'{playerName} Performance Against Opponents', pad=20, fontsize=14)
plt.xlabel('Opponent Strategy', fontsize=12)
plt.ylabel('Accumulated Score', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.ylim(0, df['score'].max() * 1.1)  # Add 10% headroom

# Annotate values on bars
for p in ax.patches:
    ax.annotate(f"{int(p.get_height())}", 
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', 
                xytext=(0, 5), 
                textcoords='offset points')

plt.tight_layout()
plt.show()