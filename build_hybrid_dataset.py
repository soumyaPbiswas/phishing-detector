import pandas as pd
from hybrid_features import extract_features
import joblib
from tqdm import tqdm

df = pd.read_csv("data/phishing.csv", on_bad_lines="skip")
df.columns = df.columns.str.lower().str.strip()

# balanced sampling
sample_df = pd.concat([
    df[df["label"] == 1].sample(200, random_state=42),
    df[df["label"] == 0].sample(200, random_state=42)
]).reset_index(drop=True)

urls = sample_df["url"].astype(str)
labels = sample_df["label"]

rows = []

print("\nBuilding hybrid dataset (Fast Mode)...\n")

for url, label in tqdm(zip(urls, labels), total=len(urls)):
    feats = extract_features(url)  # no WHOIS, no heavy scraping
    feats["label"] = label
    rows.append(feats)

hybrid_df = pd.DataFrame(rows)
hybrid_df.to_csv("hybrid_dataset.csv", index=False)

joblib.dump(list(hybrid_df.columns[:-1]), "hybrid_features.pkl")

print("\nHybrid dataset created successfully.")
print(f"Rows: {len(hybrid_df)}, Features: {len(hybrid_df.columns)-1}")
