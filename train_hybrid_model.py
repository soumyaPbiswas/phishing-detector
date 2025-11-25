import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

df = pd.read_csv("hybrid_dataset.csv")

feature_cols = joblib.load("hybrid_features.pkl")

X = df[feature_cols]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=500,
    max_depth=None,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("\nTRAINING COMPLETE\n")
print(classification_report(y_test, y_pred))

joblib.dump(model, "hybrid_model.pkl")

print("\nModel saved: hybrid_model.pkl")
