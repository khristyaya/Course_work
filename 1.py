import matplotlib.pyplot as plt
import numpy as np

metrics = [
    'Володіння м\'ячем', 'Удари', 'Удари в площину', 'xG', 'Передачі',
    'Точність передач', 'Фоли', 'Офсайди', 'Кутові'
]

team1_values = [34, 9, 4, 0.75, 346, 79, 8, 4, 1]
team2_values = [66, 10, 1, 1.14, 726, 89, 9, 0, 3]

fig, ax = plt.subplots(figsize=(14, 7))
y_pos = np.arange(len(metrics))

team1_scaled = []
team2_scaled = []
for t1, t2 in zip(team1_values, team2_values):
    local_max = max(t1, t2, 1e-5)  # уникаємо ділення на 0
    team1_scaled.append(t1 / local_max * 100)
    team2_scaled.append(t2 / local_max * 100)

bars1 = ax.barh(y_pos, team1_scaled, color='orange', edgecolor='black', height=0.4, align='center')
bars2 = ax.barh(y_pos, [-v for v in team2_scaled], color='blue', edgecolor='black', height=0.4, align='center')

for i in range(len(metrics)):
    ax.text(team1_scaled[i] + 2, y_pos[i], f'{team1_values[i]}', va='center', ha='left', fontsize=10, color='black', fontweight='bold')
    ax.text(-team2_scaled[i] - 2, y_pos[i], f'{team2_values[i]}', va='center', ha='right', fontsize=10, color='black', fontweight='bold')

    ax.text(0, y_pos[i] + 0.25, metrics[i], va='bottom', ha='center', fontsize=11, fontweight='bold')


ax.set_yticks([])
ax.set_xticks([])
ax.set_xlim(-110, 110)
ax.set_frame_on(False)


ax.legend(loc='upper right', fontsize=11)
team1_cards = "1/0"
team2_cards = "1/0"
plt.title('Порівняння команд', fontsize=16, fontweight='bold', pad=15)
plt.figtext(0.25, 0.01, f'Жовті/червоні картки Команда 1: {team1_cards}', fontsize=10)
plt.figtext(0.75, 0.01, f'Жовті/червоні картки Команда 2: {team2_cards}', fontsize=10, ha='right')

plt.tight_layout(pad=2)
plt.show()
