import pandas as pd

df = pd.read_csv("data/phishing.csv", on_bad_lines="skip")
df.columns = df.columns.str.lower().str.strip()

non_numeric = [col for col in df.columns if not pd.api.types.is_numeric_dtype(df[col])]

print("Non-numeric columns:")
print(non_numeric)
