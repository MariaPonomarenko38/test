import sys
import pandas as pd

df = pd.read_csv(sys.argv[1]) if sys.argv[1].endswith(".csv") else pd.read_excel(sys.argv[1])
print(f"Loaded: {df.shape[0]} rows × {df.shape[1]} cols | {df.isnull().sum().sum()} nulls | {df.duplicated().sum()} dupes")

df.columns = df.columns.str.strip().str.lower().str.replace(r"\s+", "_", regex=True)
df = df.drop_duplicates()
df[df.select_dtypes("object").columns] = df.select_dtypes("object").apply(lambda c: c.str.strip())
df[df.select_dtypes("number").columns] = df.select_dtypes("number").apply(lambda c: c.fillna(c.median()))
df[df.select_dtypes("object").columns] = df.select_dtypes("object").fillna("unknown")

out = sys.argv[1].rsplit(".", 1)[0] + "_cleaned.csv"
df.to_csv(out, index=False)
print(f"Saved: {df.shape[0]} rows × {df.shape[1]} cols → {out}")