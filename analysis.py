import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)

df = pd.read_csv('full_stats_with_position.csv')

print("Описова статистика:")
print(df.describe())

numeric_columns = df.select_dtypes(include=['float64', 'int64'])

df['TotalGoals'] = df['goal_scored'] + df['goal_conceded']

season_goals = df.groupby('season')['TotalGoals'].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 8))
plt.pie(season_goals, labels=season_goals.index, autopct=lambda p: f'{int(p * sum(season_goals) / 100)}', startangle=90)
plt.title("Загальна кількість голів за сезон")
plt.axis('equal')
plt.show()

avg_goals_per_season = df.groupby('season')['TotalGoals'].mean()

plt.figure(figsize=(10, 6))
plt.plot(avg_goals_per_season.index, avg_goals_per_season.values, label='Середня кількість голів', color='b', marker='o')
plt.axhline(avg_goals_per_season.mean(), color='r', linestyle='--', label=f'Середнє значення: {avg_goals_per_season.mean():.2f}')
plt.title("Середня кількість голів за сезон")
plt.xlabel("Сезони")
plt.ylabel("Середня кількість голів")
plt.legend()
plt.show()

df['Result'] = df.apply(
    lambda row: 'Win' if row['goal_scored'] > row['goal_conceded'] else ('Lose' if row['goal_scored'] < row['goal_conceded'] else 'Draw'), axis=1)

seasons = df['season'].unique()

result_colors = {'Win': 'green', 'Lose': 'red', 'Draw': 'grey'}

for season in seasons:
    season_data = df[df['season'] == season]
    results = season_data.groupby(['team', 'Result']).size().unstack(fill_value=0)

    results.plot(kind='bar', stacked=True, figsize=(12, 6), color=[result_colors[result] for result in results.columns])
    plt.title(f"Кількість перемог, поразок та нічиїх для команд у сезоні {season}")
    plt.xlabel("Команди")
    plt.ylabel("Кількість матчів")
    plt.xticks(rotation=45)
    plt.legend(title="Результат", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()
