import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_selection import RFE
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
import pickle


df_2020 = pd.read_csv('data_19-20.csv')
df_2021 = pd.read_csv('data_20-21.csv')
df_2022 = pd.read_csv('data_21-22.csv')
df_2023 = pd.read_csv('data_22-23.csv')
df_2024 = pd.read_csv('data_23-24.csv')

# Потрібні числові колонки
numerical_columns = [
    "FTHG", "FTAG",
    "HTHG", "HTAG", "HTR",
    "HS", "AS", "HST", "AST",
    "HF", "AF", "HC", "AC",
    "HY", "AY", "HR", "AR"
]


df_2020["Season"] = "2019-2020"
df_2021["Season"] = "2020-2021"
df_2022["Season"] = "2021-2022"
df_2023["Season"] = "2022-2023"
df_2024["Season"] = "2023-2024"


columns_to_keep = numerical_columns + ["Season", "HomeTeam", "AwayTeam", "FTR", "Date"]

df_raw = pd.concat([
    df_2020[columns_to_keep],
    df_2021[columns_to_keep],
    df_2022[columns_to_keep],
    df_2023[columns_to_keep],
    df_2024[columns_to_keep]
])


df_raw["Date"] = pd.to_datetime(df_raw["Date"], errors='coerce')
df_raw["Year"] = df_raw["Date"].dt.year
df_raw["Month"] = df_raw["Date"].dt.month


df_raw = df_raw.drop(columns=["Date"])


df_raw["Season"] = df_raw["Season"].astype("category")


label_encoder_home = LabelEncoder()
df_raw["HomeTeam"] = label_encoder_home.fit_transform(df_raw["HomeTeam"].astype(str))

label_encoder_away = LabelEncoder()
df_raw["AwayTeam"] = label_encoder_away.fit_transform(df_raw["AwayTeam"].astype(str))


with open('label_encoder_home.pkl', 'wb') as f:
    pickle.dump(label_encoder_home, f)

with open('label_encoder_away.pkl', 'wb') as f:
    pickle.dump(label_encoder_away, f)


col_predictors = numerical_columns + ["Season", "Month", "Year", "HomeTeam", "AwayTeam"]
X = df_raw[col_predictors]
y = df_raw["FTR"].astype("category")


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=1234)


rf_model = RandomForestClassifier(n_estimators=5000, random_state=1234, n_jobs=-1)
rf_model.fit(X_train, y_train)


importances = rf_model.feature_importances_
indices = np.argsort(importances)[::-1]


plt.figure(figsize=(10, 6))
plt.title("Feature Importances")
plt.barh(range(len(indices)), importances[indices], align="center")
plt.yticks(range(len(indices)), [col_predictors[i] for i in indices])
plt.xlabel("Relative Importance")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()


selector = RFE(rf_model, n_features_to_select=10, step=1)
selector = selector.fit(X_train, y_train)

selected_features = [col_predictors[i] for i in range(len(col_predictors)) if selector.support_[i]]
print("Selected Features (RFE):", selected_features)


param_grid = {
    "n_estimators": [100, 500, 1000],
    "max_depth": [10, 20, None]
}
grid_search = GridSearchCV(RandomForestClassifier(random_state=1234, n_jobs=-1), param_grid, cv=5)
grid_search.fit(X_train, y_train)

print("Best Parameters:", grid_search.best_params_)


y_train_pred = grid_search.predict(X_train)
y_test_pred = grid_search.predict(X_test)

print("Training Accuracy:", accuracy_score(y_train, y_train_pred))
print("Test Accuracy:", accuracy_score(y_test, y_test_pred))

print("Classification Report (Test):")
print(classification_report(y_test, y_test_pred))


with open('model_final.pkl', 'wb') as f:
    pickle.dump(grid_search, f)


predictions = pd.DataFrame({"Actual": y_test, "Predicted": y_test_pred})
predictions.to_csv("predictions.csv", index=False)
