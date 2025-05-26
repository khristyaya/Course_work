import pandas as pd
import warnings

# Suppress the SettingWithCopyWarning
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)

# Set options to display all columns
pd.set_option('display.max_columns', None)

# Завантаження даних з чотирьох сезонів
data_season_1 = pd.read_csv('data_19-20.csv')
data_season_2 = pd.read_csv('data_20-21.csv')
data_season_3 = pd.read_csv('data_21-22.csv')
data_season_4 = pd.read_csv('data_22-23.csv')
data_season_5 = pd.read_csv('data_23-24.csv')

# Додавання колонки сезону
data_season_1['Season'] = '2019/2020'
data_season_2['Season'] = '2020/2021'
data_season_3['Season'] = '2021/2022'
data_season_4['Season'] = '2022/2023'
data_season_5['Season'] = '2023/2024'

# Об'єднання даних у один датафрейм
data = pd.concat([data_season_1, data_season_2, data_season_3, data_season_4, data_season_5], ignore_index=True)

# Вибір потрібних колонок
selected_columns = [
    'Season', 'Date', 'HomeTeam', 'AwayTeam',
    'FTHG', 'FTAG', 'FTR',
    'HTHG', 'HTAG',
    'HS', 'AS', 'HST', 'AST',
    'HC', 'AC',
    'HF', 'AF',
    'HY', 'AY', 'HR', 'AR'
]

# Фільтрація датафрейму
data_selected = data[selected_columns]

# Перевірка наявність пропущених значень
print(data_selected.isnull().sum())

# Перетворення стовпця Date в тип datetime
data_selected.loc[:, 'Date'] = pd.to_datetime(data_selected['Date'], dayfirst=True)

# Додавання нових колонок
data_selected.loc[:, 'GoalDifference'] = data_selected['FTHG'] - data_selected['FTAG']
data_selected.loc[:, 'HTGoalDifference'] = data_selected['HTHG'] - data_selected['HTAG']

# Перетворення результатів на числові значення
data_selected.loc[:, 'HomeWin'] = data_selected['FTR'].apply(lambda x: 1 if x == 'H' else 0)
data_selected.loc[:, 'AwayWin'] = data_selected['FTR'].apply(lambda x: 1 if x == 'A' else 0)
data_selected.loc[:, 'Draw'] = data_selected['FTR'].apply(lambda x: 1 if x == 'D' else 0)

# Заповнення пропусків середнім значенням для кожної колонки
numerical_columns = [
    'FTHG', 'FTAG', 'HTHG', 'HTAG',
    'HS', 'AS', 'HST', 'AST',
    'HC', 'AC', 'HF', 'AF',
    'HY', 'AY', 'HR', 'AR',
    'GoalDifference', 'HTGoalDifference', 'HomeWin', 'AwayWin', 'Draw'
]

# Заповнення пропусків середнім значенням для числових колонок
data_selected.loc[:, numerical_columns] = data_selected[numerical_columns].fillna(data_selected[numerical_columns].mean())

# Перевірка результату
print(data_selected.head())

# Збереження очищених даних у новий CSV файл (за потреби)
data_selected.to_csv('cleaned_data.csv', index=False)
