import pandas as pd
import numpy as np
import joblib
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

# Завантаження моделі та LabelEncoder
model = joblib.load('model_final.pkl')
le_home = joblib.load('le_home.pkl')
le_away = joblib.load('le_away.pkl')
le_htr = joblib.load('le_htr.pkl')
le_ftr = joblib.load('le_ftr.pkl')

# Завантаження CSV
files = ["data_19-20.csv", "data_20-21.csv", "data_21-22.csv", "data_22-23.csv", "data_23-24.csv"]
dfs = [pd.read_csv(file) for file in files]
df_all = pd.concat(dfs)
df_all['Date'] = pd.to_datetime(df_all['Date'], dayfirst=True, errors='coerce')

# Список команд
available_teams = df_all['HomeTeam'].unique()

# Функція показу логотипу
def show_logo(team_name, label):
    path = f"logos/{team_name}.png"
    if os.path.exists(path):
        image = Image.open(path).resize((100, 100))
        logo = ImageTk.PhotoImage(image)
        label.image = logo
        label.config(image=logo)
    else:
        label.config(image='', text="(Без логотипу)", font=("Arial", 10))

# Прогноз
def predict_result():
    home_team_name = home_team_combobox.get()
    away_team_name = away_team_combobox.get()

    if home_team_name not in available_teams or away_team_name not in available_teams:
        result_label.config(text="⚠️ Неправильна назва команди.")
        return

    match = df_all[
        (df_all['HomeTeam'] == home_team_name) & (df_all['AwayTeam'] == away_team_name)
    ].sort_values(by='Date', ascending=False).head(1)

    if match.empty:
        result_label.config(text="Матч між цими командами не знайдено.")
        return

    row = match.iloc[0]
    home_encoded = le_home.transform([row['HomeTeam']])[0]
    away_encoded = le_away.transform([row['AwayTeam']])[0]
    htr_encoded = le_htr.transform([row['HTR']])[0]

    features = [
        row["FTHG"], row["FTAG"], row["HTHG"], row["HTAG"], htr_encoded,
        row["HS"], row["AS"], row["HST"], row["AST"],
        row["HF"], row["AF"], row["HC"], row["AC"],
        row["HY"], row["AY"], row["HR"], row["AR"],
        home_encoded, away_encoded
    ]

    feature_names = ["FTHG", "FTAG", "HTHG", "HTAG", "HTR",
                     "HS", "AS", "HST", "AST", "HF", "AF",
                     "HC", "AC", "HY", "AY", "HR", "AR",
                     "HomeTeam", "AwayTeam"]

    features_df = pd.DataFrame([features], columns=feature_names)

    prediction = model.predict(features_df)[0]
    predicted_label = le_ftr.inverse_transform([prediction])[0]

    if predicted_label == 'H':
        result = f"Перемога: {home_team_name}"
    elif predicted_label == 'A':
        result = f"Перемога: {away_team_name}"
    else:
        result = "Нічия"

    result_label.config(text=f"Прогноз: {result}")

# --- Інтерфейс ---
root = tk.Tk()
root.title("Прогноз футбольного матчу")
root.geometry("650x400")

title_label = tk.Label(root, text="Прогноз результату матчу", font=("Arial", 16, "bold"))
title_label.pack(pady=20)

frame = tk.Frame(root)
frame.pack()

# Лівий та правий блоки
left_frame = tk.Frame(frame)
left_frame.grid(row=0, column=0, padx=30)

right_frame = tk.Frame(frame)
right_frame.grid(row=0, column=1, padx=30)

# Надписи
tk.Label(left_frame, text="Домашня команда", font=("Arial", 12)).pack()
home_logo_label = tk.Label(left_frame)
home_logo_label.pack(pady=5)
home_team_combobox = ttk.Combobox(left_frame, values=sorted(available_teams), width=25)
home_team_combobox.pack()
home_team_combobox.bind("<<ComboboxSelected>>", lambda e: show_logo(home_team_combobox.get(), home_logo_label))

tk.Label(right_frame, text="Гостьова команда", font=("Arial", 12)).pack()
away_logo_label = tk.Label(right_frame)
away_logo_label.pack(pady=5)
away_team_combobox = ttk.Combobox(right_frame, values=sorted(available_teams), width=25)
away_team_combobox.pack()
away_team_combobox.bind("<<ComboboxSelected>>", lambda e: show_logo(away_team_combobox.get(), away_logo_label))

# Кнопка прогнозу
predict_button = tk.Button(root, text="Отримати прогноз", font=("Arial", 12), command=predict_result, bg="#4CAF50", fg="white", width=25)
predict_button.pack(pady=20)

# Результат
result_label = tk.Label(root, text="", font=("Arial", 14), pady=10)
result_label.pack()

root.mainloop()
