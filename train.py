import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_csv("Honeywell_Synthetic_Historical_Dataset_10000.csv")
print(df["OffSpec"].value_counts())

print("\nDataset Loaded Successfully")
print(df.head())

drop_columns = [
    "Timestamp",
    "Grade",
    "Recommended Action"
]

df = df.drop(columns=drop_columns)

X = df[
    [
        "Stock Flow (L/min)",
        "Filler Flow (kg/min)",
        "Steam Pressure (bar)",
        "Machine Speed (m/min)",
        "Moisture (%)",
        "Ash (%)",
        "Caliper (mm)"
    ]
]

y = df["OffSpec"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    random_state=42
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report\n")
print(classification_report(y_test, y_pred))

importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nFeature Importance\n")
print(importance)

if not os.path.exists("model"):
    os.makedirs("model")

joblib.dump(model, "model/paper_model.pkl")

print("\nModel Saved Successfully")