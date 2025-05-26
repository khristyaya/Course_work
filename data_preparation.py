import pandas as pd
import numpy as np

# Завантаження даних з CSV-файлів
data_season_1 = pd.read_csv('data_19-20.csv')
data_season_2 = pd.read_csv('data_20-21.csv')
data_season_3 = pd.read_csv('data_21-22.csv')
data_season_4 = pd.read_csv('data_22-23.csv')
data_season_5 = pd.read_csv('data_23-24.csv')

# Вибір необхідних колонок
col_needed = [
    "HomeTeam", "AwayTeam", "Date",
    "FTHG", "FTAG", "FTR",
    "HTHG", "HTAG", "HTR",
    "HS", "AS", "HST", "AST",
    "HF", "AF", "HC", "AC",
    "HY", "AY", "HR", "AR"
]

# Вибір потрібних колонок для кожного сезону
df_2020 = pd.DataFrame(data_season_1[col_needed])
df_2021 = pd.DataFrame(data_season_2[col_needed])
df_2022 = pd.DataFrame(data_season_3[col_needed])
df_2023 = pd.DataFrame(data_season_4[col_needed])
df_2024 = pd.DataFrame(data_season_5[col_needed])

# Додавання колонки "Season" для кожного сезону
df_2020["Season"] = "2019-2020"
df_2021["Season"] = "2020-2021"
df_2022["Season"] = "2021-2022"
df_2023["Season"] = "2022-2023"
df_2024["Season"] = "2023-2024"

seasons = ["2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024"]

# Об'єднання усіх сезонів
df_raw = pd.concat([df_2020, df_2021, df_2022, df_2023, df_2024])

# Перетворення дати на формат datetime
df_raw.loc[:, 'Date'] = pd.to_datetime(df_raw['Date'], dayfirst=True)


def extract_stats(df_raw, n_season=None):
    print(f"Extracting Stats for Season {n_season} ...")

    df_season = df_raw[df_raw["Season"] == n_season]
    all_teams = sorted(df_season["HomeTeam"].unique())

    df_output = pd.DataFrame()

    for temp_team in all_teams:
        # Home Matches
        df_home = df_season[df_season["HomeTeam"] == temp_team].copy()
        df_home_stats = pd.DataFrame({
            "season": n_season,
            "date": df_home["Date"],
            "team": df_home["HomeTeam"],
            "venue": "home",
            "opponent": df_home["AwayTeam"],
            "goal_scored": df_home["FTHG"],
            "goal_conceded": df_home["FTAG"],
            "goal_diff": df_home["FTHG"] - df_home["FTAG"],
            "shot": df_home["HS"],
            "on_target": df_home["HST"],
            "on_target_rate": df_home["HST"] / df_home["HS"],
            "hit_rate": df_home["FTHG"] / df_home["HS"],
            "shot_opp": df_home["AS"],
            "on_target_opp": df_home["AST"],
            "on_target_rate_opp": df_home["AST"] / df_home["AS"],
            "hit_rate_opp": df_home["FTAG"] / df_home["AS"],
            "foul_commited": df_home["HF"],
            "foul_received": df_home["AF"],
            "foul_ratio": df_home["HF"] / df_home["AF"],
            "yellow": df_home["HY"],
            "yellow_opp": df_home["AY"],
            "red": df_home["HR"],
            "red_opp": df_home["AR"],
            "corner_awarded": df_home["HC"],
            "corner_conceded": df_home["AC"]
        })

        # Away Matches
        df_away = df_season[df_season["AwayTeam"] == temp_team].copy()
        df_away_stats = pd.DataFrame({
            "season": n_season,
            "date": df_away["Date"],
            "team": df_away["AwayTeam"],
            "venue": "away",
            "opponent": df_away["HomeTeam"],
            "goal_scored": df_away["FTAG"],
            "goal_conceded": df_away["FTHG"],
            "goal_diff": df_away["FTAG"] - df_away["FTHG"],
            "shot": df_away["AS"],
            "on_target": df_away["AST"],
            "on_target_rate": df_away["AST"] / df_away["AS"],
            "hit_rate": df_away["FTAG"] / df_away["AS"],
            "shot_opp": df_away["HS"],
            "on_target_opp": df_away["HST"],
            "on_target_rate_opp": df_away["HST"] / df_away["HS"],
            "hit_rate_opp": df_away["FTHG"] / df_away["HS"],
            "foul_commited": df_away["AF"],
            "foul_received": df_away["HF"],
            "foul_ratio": df_away["AF"] / df_away["HF"],
            "yellow": df_away["AY"],
            "yellow_opp": df_away["HY"],
            "red": df_away["AR"],
            "red_opp": df_away["HR"],
            "corner_awarded": df_away["AC"],
            "corner_conceded": df_away["HC"]
        })

        # Об’єднати домашні та виїзні матчі
        df_team = pd.concat([df_home_stats, df_away_stats], ignore_index=True)
        df_team.sort_values(by="date", inplace=True)
        df_team.reset_index(drop=True, inplace=True)

        df_team.insert(3, "num_match", range(1, len(df_team) + 1))

        # Кумулятивна різниця голів
        df_team["cu_goal_diff"] = df_team["goal_diff"].cumsum()

        # Очки
        df_team["points"] = np.select(
            [df_team["goal_diff"] > 0, df_team["goal_diff"] == 0],
            [3, 1], default=0
        )
        df_team["cu_points"] = df_team["points"].cumsum()

        # Результат
        df_team["result"] = np.select(
            [df_team["points"] == 3, df_team["points"] == 1],
            ["Win", "Draw"], default="Loss"
        )

        # Очки + різниця голів для позиції
        df_team["points_w_goaldiff"] = (df_team["cu_points"] +
                                        df_team["cu_goal_diff"] / 1000 +
                                        df_team["on_target"] / 1_000_000)

        # Додати до фінального DataFrame
        df_output = pd.concat([df_output, df_team], ignore_index=True)

    return df_output

# Витягнути статистику по сезонах
df_stats_all = pd.DataFrame()
for season in seasons:
    stats = extract_stats(df_raw, n_season=season)
    df_stats_all = pd.concat([df_stats_all, stats], ignore_index=True)

# =============================================================================
# Extract League Positions for Each Match
# =============================================================================

def extract_pos(df_season):
    season_label = df_season.iloc[0]["season"]
    print(f"Extracting League Position for Season {season_label} ...")

    all_teams = sorted(df_season["team"].unique())
    league_table = []

    for match_day in range(1, 39):
        day_df = df_season[df_season["num_match"] == match_day]
        points_table = day_df[["team", "cu_points", "cu_goal_diff"]].copy()

        # Сортировка по очкам і різниці голів
        points_table["rank_score"] = points_table["cu_points"] + points_table["cu_goal_diff"] / 1000
        points_table.sort_values(by="rank_score", ascending=False, inplace=True)
        points_table.reset_index(drop=True, inplace=True)
        points_table["position"] = range(1, 21)
        points_table["match_day"] = match_day
        points_table["season"] = season_label

        league_table.append(points_table)

    return pd.concat(league_table, ignore_index=True)

# Отримати позицію для кожного сезону
df_positions_all = pd.DataFrame()
for season in seasons:
    df_season_stats = df_stats_all[df_stats_all["season"] == season]
    df_positions = extract_pos(df_season_stats)
    df_positions_all = pd.concat([df_positions_all, df_positions], ignore_index=True)

# З'єднання позиції з основною таблицею
df_stats_all = df_stats_all.merge(
    df_positions_all[["team", "match_day", "season", "position"]],
    left_on=["team", "num_match", "season"],
    right_on=["team", "match_day", "season"],
    how="left"
)

# Видалити колонку match_day
df_stats_all.drop(columns=["match_day"], inplace=True)

# Перевірка результату
print(df_stats_all[["team", "num_match", "season", "position"]].head())

# Зберегти оновлений файл з позицією
df_stats_all.to_csv("full_stats_with_position.csv", index=False)
print("Файл 'full_stats_with_position.csv' збережено.")

