import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Завантаження CSV
df_all = pd.read_csv('full_stats_with_position.csv')

# =============================================================================
# Big Four — Позиція у таблиці по сезонах
# =============================================================================

big_four = ["Arsenal", "Chelsea", "Man United", "Man City"]
df_big_four = df_all[df_all["team"].isin(big_four)]

# Кольори для кожної з команд
team_colors = {
    "Arsenal": "#FF0000",      # Червоний
    "Chelsea": "#0033A0",      # Синій
    "Man United": "#DA291C",  # Червоний Ман Юнайтед
    "Man City": "#6cabdd"     # Голубий
}

# Побудова графіка позицій по сезонах
def plot_position(df, title):
    g = sns.FacetGrid(df, col="season", row="team", hue="team", margin_titles=True,
                      height=3, aspect=2, palette=team_colors)
    g.map_dataframe(sns.lineplot, x="num_match", y="position")
    g.set_titles(row_template='{row_name}', col_template='{col_name}')
    g.set_axis_labels("Game Weeks (1-38)", "League Position (1-20)")
    g.set(ylim=(20, 0))  # Інверсія осі Y (1 — найкраще)
    plt.subplots_adjust(top=0.9)
    g.fig.suptitle(title)
    plt.show()

# Побудова графіку Big Four
plot_position(df_big_four, "League Position of Big Four since 2005")

# =============================================================================
# Барплот: Скільки разів команда фінішувала 4-ою
# =============================================================================

df_4th = df_all[(df_all["num_match"] == 38) & (df_all["position"] == 4)]
count_4th = df_4th["team"].value_counts().reset_index()
count_4th.columns = ["team", "num_seasons"]

plt.figure(figsize=(8, 5))
sns.barplot(data=count_4th, x="team", y="num_seasons", hue="team", palette="viridis", legend=False)
plt.xlabel("Teams")
plt.ylabel("Number of Seasons")
plt.title("Number of Times Finishing Fourth")

# Оновлення позначок осі X для цілих чисел
plt.xticks(range(len(count_4th["team"])), count_4th["team"])

plt.tight_layout()
plt.show()

# =============================================================================
# Manchester City — Сума очок за сезон (останні матчі)
# =============================================================================

df_city_points = df_all[(df_all["team"] == "Man City") & (df_all["num_match"] == 38)]
df_city_points = df_city_points.groupby("season", as_index=False).agg(points=("cu_points", "sum"))

# Сортування сезонів
df_city_points["season"] = pd.Categorical(df_city_points["season"], ordered=True,
                                          categories=sorted(df_city_points["season"].unique()))
df_city_points = df_city_points.sort_values("season")

# Побудова графіку
plt.figure(figsize=(10, 6))
plt.scatter(df_city_points["season"], df_city_points["points"], color='blue', s=100, label='Points')

for i, txt in enumerate(df_city_points["points"]):
    plt.annotate(txt, (df_city_points["season"].iloc[i], df_city_points["points"].iloc[i]),
                 textcoords="offset points", xytext=(0, 10), ha='center')

plt.plot(df_city_points["season"], df_city_points["points"], color='#10B5EF', marker='o', linestyle='-', markersize=8)
plt.title("Manchester City's Performance since 2019")
plt.xlabel("Season")
plt.ylabel("Total Points After 38 Matches")
plt.xticks(rotation=30, ha='right')
plt.grid(True)
plt.tight_layout()
plt.show()

# =============================================================================
# Arsenal vs Man City — Порівняння позицій та очок (2023-2024)
# =============================================================================

df_arsenal = df_all[(df_all["team"] == "Arsenal") & (df_all["season"] == "2023-2024")]
df_mancity = df_all[(df_all["team"] == "Man City") & (df_all["season"] == "2023-2024")]

# Функція порівняння: Позиція/Очки з можливістю інверсії осі Y
def plot_comparison(df1, df2, label1, label2, title, y_label, invert_y=False):
    plt.figure(figsize=(10, 6))
    plt.plot(df1["num_match"], df1["position"], label=label1, color='red', linestyle='-', marker='o')
    plt.plot(df2["num_match"], df2["position"], label=label2, color='#10B5EF', linestyle='-', marker='o')
    plt.title(title)
    plt.xlabel("Matches")
    plt.ylabel(y_label)
    if invert_y:
        plt.gca().invert_yaxis()
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Графік позицій
plot_comparison(df_arsenal, df_mancity, "Arsenal", "Man City",
                "Arsenal vs Man City (League Position)", "League Position", invert_y=True)

# Окрема функція для очок
def plot_points_comparison(df1, df2, label1, label2, title):
    plt.figure(figsize=(10, 6))
    plt.plot(df1["num_match"], df1["cu_points"], label=label1, color='red', linestyle='-', marker='o')
    plt.plot(df2["num_match"], df2["cu_points"], label=label2, color='#10B5EF', linestyle='-', marker='o')
    plt.title(title)
    plt.xlabel("Matches")
    plt.ylabel("Total Points")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Графік очок
plot_points_comparison(df_arsenal, df_mancity, "Arsenal", "Man City","Arsenal vs Man City (Total Points)")

# =============================================================================
# Big Four — Позиції у таблиці по сезонах (для кожного сезону окремо)
# =============================================================================

big_four = ["Arsenal", "Chelsea", "Man United", "Man City"]
df_big_four = df_all[df_all["team"].isin(big_four)]

# Кольори команд
team_colors = {
    "Arsenal": "#FF0000",
    "Chelsea": "#0033A0",
    "Man United": "#DA291C",
    "Man City": "#6cabdd"
}

# Отримати список сезонів
seasons = sorted(df_big_four["season"].unique())

# Побудова графіків — один графік на сезон
for season in seasons:
    plt.figure(figsize=(12, 6))
    for team in big_four:
        df_temp = df_big_four[(df_big_four["season"] == season) & (df_big_four["team"] == team)]
        plt.plot(df_temp["num_match"], df_temp["position"],
                 label=team,
                 color=team_colors[team],
                 linewidth=2,
                 marker='o',
                 markersize=4)
        # Додати маркер кінцевої позиції
        end_pos = df_temp[df_temp["num_match"] == df_temp["num_match"].max()]
        plt.text(end_pos["num_match"].values[0] + 0.5,
                 end_pos["position"].values[0],
                 f'{team}: {int(end_pos["position"].values[0])}',
                 color=team_colors[team],
                 fontsize=9,
                 va='center')

    plt.title(f'League Positions — Big Four ({season})', fontsize=16)
    plt.xlabel("Game Weeks (1-38)")
    plt.ylabel("League Position")
    plt.ylim(20, 0)  # Інверсія осі
    plt.xticks(range(1, 39, 1))
    plt.yticks(range(1, 21))
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(title="Teams")
    plt.tight_layout()
    plt.show()

# =============================================================================
# Середня позиція за всі тури кожного сезону
# =============================================================================

avg_positions_true = df_all.groupby(["season", "team"]).agg(avg_pos=("position", "mean")).reset_index()

# Pivot table для heatmap
pivot_avg_pos_true = avg_positions_true.pivot(index="team", columns="season", values="avg_pos")

plt.figure(figsize=(14, 8))
sns.heatmap(pivot_avg_pos_true, annot=True, fmt=".1f", cmap="YlGnBu", cbar_kws={"label": "Average League Position"})
plt.title("Average League Position by Season (All Matches)")
plt.xlabel("Season")
plt.ylabel("Team")
plt.tight_layout()
plt.show()

# =============================================================================
# Фільтрація даних для сезону 2023/24 — середня кількість ударів по воротах
# =============================================================================

df_2023_24 = df_all[df_all["season"] == "2023-2024"]

# Обчислення середньої кількості ударів по воротах для кожної команди
avg_shots_per_team = df_2023_24.groupby("team")["shot"].mean().reset_index()

# Сортування команд за середньою кількістю ударів
avg_shots_per_team_sorted = avg_shots_per_team.sort_values(by="shot", ascending=False)

# Побудова графіка
plt.figure(figsize=(12, 6))
sns.barplot(data=avg_shots_per_team_sorted, x="team", y="shot", palette="viridis")
plt.title("Average Shots per Team in 2023-2024 Season")
plt.xlabel("Team")
plt.ylabel("Average Shots")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
