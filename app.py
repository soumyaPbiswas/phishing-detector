from flask import Flask, render_template, request
import joblib
from hybrid_features import extract_features
import pandas as pd

app = Flask(__name__)

model = joblib.load("hybrid_model.pkl")
feature_cols = joblib.load("hybrid_features.pkl")

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    url_value = ""

    if request.method == "POST":
        url_value = request.form.get("url","").strip()
        feats = extract_features(url_value)
        df = pd.DataFrame([[feats[col] for col in feature_cols]], columns=feature_cols)

        pred = model.predict(df)[0]
        prob = max(model.predict_proba(df)[0]) * 100

        if pred == 0:
            result = f"⚠️ Phishing ({prob:.2f}% confidence)"
        else:
            result = f"🟢 Safe ({prob:.2f}% confidence)"

    return render_template("index.html", msg=result, url_value=url_value)

if __name__ == "__main__":
    app.run(debug=True)
