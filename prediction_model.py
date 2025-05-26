import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE
import matplotlib.pyplot as plt
import joblib
from sklearn.preprocessing import LabelEncoder

E0_2019 = pd.read_csv("data_19-20.csv")
E0_2020 = pd.read_csv("data_20-21.csv")
E0_2021 = pd.read_csv("data_21-22.csv")
E0_2022 = pd.read_csv("data_22-23.csv")
E0_2023 = pd.read_csv("data_23-24.csv")

numerical_columns = [
    "FTHG", "FTAG",
    "HTHG", "HTAG", "HTR",
    "HS", "AS", "HST", "AST",
    "HF", "AF", "HC", "AC",
    "HY", "AY", "HR", "AR"
]

df_raw = pd.concat([
    E0_2019[numerical_columns + ["HomeTeam", "AwayTeam", "FTR"]].assign(Season="2019-2020"),
    E0_2020[numerical_columns + ["HomeTeam", "AwayTeam", "FTR"]].assign(Season="2020-2021"),
    E0_2021[numerical_columns + ["HomeTeam", "AwayTeam", "FTR"]].assign(Season="2021-2022"),
    E0_2022[numerical_columns + ["HomeTeam", "AwayTeam", "FTR"]].assign(Season="2022-2023"),
    E0_2023[numerical_columns + ["HomeTeam", "AwayTeam", "FTR"]].assign(Season="2023-2024")
])

print(df_raw.isnull().sum())

le_home = LabelEncoder()
le_away = LabelEncoder()
le_ftr = LabelEncoder()
le_htr = LabelEncoder()

df_raw['HomeTeam'] = le_home.fit_transform(df_raw['HomeTeam'])
df_raw['AwayTeam'] = le_away.fit_transform(df_raw['AwayTeam'])
df_raw['FTR'] = le_ftr.fit_transform(df_raw['FTR'])
df_raw['HTR'] = le_htr.fit_transform(df_raw['HTR'])

print(df_raw.dtypes)

print(df_raw['FTR'].unique())
print(df_raw['HTR'].unique())

X = df_raw[numerical_columns + ["HomeTeam", "AwayTeam"]]
y = df_raw['FTR'].astype('category')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=1234)

rf_model = RandomForestClassifier(n_estimators=5000, max_features=2, random_state=1234)
rf_model.fit(X_train, y_train)

importances = rf_model.feature_importances_
indices = np.argsort(importances)

plt.figure(figsize=(10, 6))
plt.title("Feature Importance")
plt.barh(range(len(indices)), importances[indices], align="center")
plt.yticks(range(len(indices)), np.array(numerical_columns + ["HomeTeam", "AwayTeam"])[indices])
plt.xlabel("Relative Importance")
plt.show()

selector = RFE(rf_model, n_features_to_select=10, step=1)
selector = selector.fit(X_train, y_train)

joblib.dump(selector, 'model_rfe.pkl')

rf_model_final = RandomForestClassifier(n_estimators=5000, max_features=2, random_state=1234)
rf_model_final.fit(X_train, y_train)

train_accuracy = rf_model_final.score(X_train, y_train)
test_accuracy = rf_model_final.score(X_test, y_test)

print(f"Train Accuracy: {train_accuracy:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")

joblib.dump(rf_model_final, 'model_final.pkl')

y_train_pred = rf_model_final.predict(X_train)
y_test_pred = rf_model_final.predict(X_test)

joblib.dump({'y_train': y_train_pred, 'y_test': y_test_pred}, 'predictions.pkl')

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

print("Confusion Matrix (Test Data):")
print(confusion_matrix(y_test, y_test_pred))
print("\nClassification Report (Test Data):")
print(classification_report(y_test, y_test_pred))

joblib.dump(le_home, 'le_home.pkl')
joblib.dump(le_away, 'le_away.pkl')
joblib.dump(le_ftr, 'le_ftr.pkl')
joblib.dump(le_htr, 'le_htr.pkl')
