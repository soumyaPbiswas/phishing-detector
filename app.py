from flask import Flask, render_template, request
import joblib
from hybrid_features import extract_features
import pandas as pd
import tldextract

app = Flask(__name__)

model = joblib.load("hybrid_model.pkl")
feature_cols = joblib.load("hybrid_features.pkl")

SAFE_DOMAINS = {
    "trailhead.salesforce.com",
    "salesforce.com",
    "login.salesforce.com",
    "developer.salesforce.com"
}

PHISHING_THRESHOLD = 0.8

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    url_value = ""

    if request.method == "POST":
        url_value = request.form.get("url", "").strip()
        if url_value:
            ext = tldextract.extract(url_value)
            full_domain = ".".join(part for part in [ext.subdomain, ext.domain, ext.suffix] if part)

            feats = extract_features(url_value)
            df = pd.DataFrame([[feats[col] for col in feature_cols]], columns=feature_cols)

            proba = model.predict_proba(df)[0]
            phishing_prob = float(proba[0])
            safe_prob = float(proba[1])

            if full_domain in SAFE_DOMAINS:
                result = f"Safe ({safe_prob*100:.2f}% confidence, whitelisted domain)"
            elif phishing_prob >= PHISHING_THRESHOLD:
                result = f"Phishing ({phishing_prob*100:.2f}% confidence)"
            else:
                result = f"Safe ({safe_prob*100:.2f}% confidence, below phishing threshold)"

    return render_template("index.html", msg=result, url_value=url_value)

if __name__ == "__main__":
    app.run(debug=True)
