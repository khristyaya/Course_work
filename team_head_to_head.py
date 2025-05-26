import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Завантаження даних з CSV
df = pd.read_csv("full_stats_with_position.csv")

# Перевірка перших кількох рядків
print(df.head())

# Функція для отримання статистики команд
def get_team_stats(df, season, team1, team2):
    # Фільтруємо за сезоном
    season_data = df[df['season'] == season]

    # Отримуємо статистику для вибраних команд
    team1_data = season_data[season_data['team'] == team1]
    team2_data = season_data[season_data['team'] == team2]

    # Для кожної команди підрахуємо необхідні статистики
    team1_stats = {
        'Удари': team1_data['shot'].sum(),
        'Удари в площину': team1_data['on_target'].sum(),
        'Фоли': team1_data['foul_commited'].sum(),
        'Кутові': team1_data['corner_awarded'].sum(),
        'Жовті картки': team1_data['yellow'].sum(),
        'Червоні картки': team1_data['red'].sum(),
        'Позиція в лізі': team1_data['position'].max()
    }

    team2_stats = {
        'Удари': team2_data['shot'].sum(),
        'Удари в площину': team2_data['on_target'].sum(),
        'Фоли': team2_data['foul_commited'].sum(),
        'Кутові': team2_data['corner_awarded'].sum(),
        'Жовті картки': team2_data['yellow'].sum(),
        'Червоні картки': team2_data['red'].sum(),
        'Позиція в лізі': team2_data['position'].max()
    }

    return team1_stats, team2_stats

# Функція для побудови графіка
def plot_comparison(team1_stats, team2_stats, team1, team2):
    metrics = list(team1_stats.keys())
    team1_values = list(team1_stats.values())
    team2_values = list(team2_stats.values())

    fig, ax = plt.subplots(figsize=(14, 7))
    y_pos = np.arange(len(metrics))

    # Масштабування окремо для кожного показника
    team1_scaled = []
    team2_scaled = []
    for t1, t2 in zip(team1_values, team2_values):
        local_max = max(t1, t2, 1e-5)  # уникаємо ділення на 0
        team1_scaled.append(t1 / local_max * 100)
        team2_scaled.append(t2 / local_max * 100)

    # Бар-графіки з новими кольорами
    bars1 = ax.barh(y_pos, team1_scaled, color='red', edgecolor='black', height=0.4, align='center', label=team1)
    bars2 = ax.barh(y_pos, [-v for v in team2_scaled], color='purple', edgecolor='black', height=0.4, align='center',
                    label=team2)

    # Значення + назви над барами
    for i in range(len(metrics)):
        # Значення на кінцях
        ax.text(team1_scaled[i] + 2, y_pos[i], f'{team1_values[i]}', va='center', ha='left', fontsize=10, color='black',
                fontweight='bold')
        ax.text(-team2_scaled[i] - 2, y_pos[i], f'{team2_values[i]}', va='center', ha='right', fontsize=10,
                color='black', fontweight='bold')
        # Назва показника над центром
        ax.text(0, y_pos[i] + 0.25, metrics[i], va='bottom', ha='center', fontsize=11, fontweight='bold')

    # Оформлення
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_xlim(-110, 110)
    ax.set_frame_on(False)

    # Легенда + картки (переміщена до верхнього лівого кута)
    ax.legend(loc='upper left', fontsize=11)
    team1_cards = f"{team1_stats['Жовті картки']}/{team1_stats['Червоні картки']}"  # Картки для команди 1
    team2_cards = f"{team2_stats['Жовті картки']}/{team2_stats['Червоні картки']}"  # Картки для команди 2
    plt.title(f'Порівняння команд {team1} та {team2}', fontsize=16, fontweight='bold', pad=15)

    plt.tight_layout(pad=2)
    plt.show()

# Наприклад, вибираємо сезон 2021/22 та команди "Arsenal" і "Liverpool"
team1 = "Arsenal"
team2 = "Liverpool"
season = "2021-2022"

# Отримуємо статистику для команд
team1_stats, team2_stats = get_team_stats(df, season, team1, team2)

# Виводимо графік
plot_comparison(team1_stats, team2_stats, team1, team2)
