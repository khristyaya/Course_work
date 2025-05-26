import pandas as pd
import tkinter as tk
from tkinter import ttk

# Завантаження CSV
df_all = pd.read_csv('full_stats_with_position.csv')

# Очищаємо назви команд і сезону: видаляємо зайві лапки та пробіли
df_all['team'] = df_all['team'].str.replace('"', '').str.replace("'", "").str.strip()
df_all['season'] = df_all['season'].str.replace('"', '').str.replace("'", "").str.strip()


# Функція для обчислення статистики за команду та сезон
def get_team_statistics(team, season):
    print(f"Вибрані значення: команда = {team}, сезон = {season}")  # Для перевірки
    # Фільтрація даних за командою та сезоном
    df_team_season = df_all[(df_all['team'] == team) & (df_all['season'] == season)]

    if df_team_season.empty:
        result_label.config(text="Дані не знайдено для вибраної команди та сезону.")
        return

    # Обчислення статистики
    avg_goals = df_team_season['goal_scored'].mean()
    total_goals = df_team_season['goal_scored'].sum()
    total_conceded = df_team_season['goal_conceded'].sum()
    avg_shots = df_team_season['shot'].mean()
    total_yellow_cards = df_team_season['yellow'].sum()  # Загальна кількість жовтих карток
    total_red_cards = df_team_season['red'].sum()  # Загальна кількість червоних карток

    # Виведення результату
    result_text = (
        f"Сезон: {season}\n"
        f"Команда: {team}\n\n"
        f"Середня кількість голів: {avg_goals:.2f}\n"
        f"Загальна кількість забитих м'ячів: {total_goals}\n"
        f"Загальна кількість пропущених м'ячів: {total_conceded}\n"
        f"Середня кількість ударів по воротах: {avg_shots:.2f}\n"
        f"Загальна кількість жовтих карток: {total_yellow_cards}\n"
        f"Загальна кількість червоних карток: {total_red_cards}\n"
    )

    result_label.config(text=result_text)


# Створення основного вікна
root = tk.Tk()
root.title("Статистика команди")
root.geometry("500x500")  # Збільшене вікно

# Колір фону
root.config(bg="#F0F0F0")

# Фрейм для організації елементів
frame = tk.Frame(root, bg="#F0F0F0")
frame.pack(pady=20, padx=20, expand=True)

# Заголовок
title_label = tk.Label(frame, text="Футбольна статистика", font=("Arial", 16, "bold"), bg="#F0F0F0")
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Вибір команди
team_label = tk.Label(frame, text="Виберіть команду:", font=("Arial", 12), bg="#F0F0F0")
team_label.grid(row=1, column=0, pady=10, sticky="w")

team_combobox = ttk.Combobox(frame, values=[team.strip() for team in df_all['team'].unique()], width=25)
team_combobox.grid(row=1, column=1, pady=10)

# Вибір сезону
season_label = tk.Label(frame, text="Виберіть сезон:", font=("Arial", 12), bg="#F0F0F0")
season_label.grid(row=2, column=0, pady=10, sticky="w")

season_combobox = ttk.Combobox(frame, values=[season.strip() for season in df_all['season'].unique()], width=25)
season_combobox.grid(row=2, column=1, pady=10)

# Кнопка для отримання статистики
button = tk.Button(frame, text="Отримати статистику", font=("Arial", 12),
                   command=lambda: get_team_statistics(team_combobox.get(), season_combobox.get()), width=20,
                   bg="#4CAF50", fg="white", relief="flat")
button.grid(row=3, column=0, columnspan=2, pady=20)

# Текстове поле для результатів
result_label = tk.Label(frame, text="", justify="left", padx=10, pady=10, font=("Arial", 12), bg="#F0F0F0")
result_label.grid(row=4, column=0, columnspan=2, pady=10)

# Запуск інтерфейсу
root.mainloop()
