import glob
from pathlib import Path
import pandas as pd
from datetime import datetime, timezone

def newest(pattern: str) -> str:
    paths = glob.glob(pattern)
    if not paths:
        raise FileNotFoundError(f"No files match: {pattern}")
    return max(paths, key=lambda p: Path(p).stat().st_mtime)

# --- Load files (pick newest matching each pattern) ---
trimmed_path = newest("data/interim/trimmed*.csv")                # has: name
dob_path      = newest("data/interim/date_of_birth_*.csv")        # has: clean_name, year, month, day
edu_path      = newest("data/interim/splited_edu_*.csv")          # has: clean_name, university_1..3, degree_1..3

df_trim = pd.read_csv(trimmed_path)
df_dob  = pd.read_csv(dob_path)
df_edu  = pd.read_csv(edu_path)

# --- Optional: normalize name fields (safer joins) ---
def norm(s):
    return (str(s).replace("\xa0", " ").strip() if pd.notna(s) else s)

df_trim["name"]       = df_trim["name"].map(norm)
df_dob["clean_name"]  = df_dob["clean_name"].map(norm)
df_edu["clean_name"]  = df_edu["clean_name"].map(norm)

# --- Ensure integer-like DoB columns are proper nullable ints ---
for col in ["year", "month", "day"]:
    if col in df_dob.columns:
        df_dob[col] = pd.to_numeric(df_dob[col], errors="coerce").astype("Int64")

# --- Select only needed columns from sources ---
dob_keep = ["clean_name", "year", "month", "day"]
edu_keep = ["clean_name",
            "university_1", "degree_1",
            "university_2", "degree_2",
            "university_3", "degree_3"]

df_dob = df_dob[dob_keep]
df_edu = df_edu[edu_keep]

# --- Merge: name (trimmed) ↔ clean_name (dob/edu) ---
out = df_trim.merge(df_dob, left_on="name", right_on="clean_name", how="left")
out = out.drop(columns=["clean_name"])

out = out.merge(df_edu, left_on="name", right_on="clean_name", how="left")
out = out.drop(columns=["clean_name"])

# --- Save ---
stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
Path("data/processed").mkdir(parents=True, exist_ok=True)
out_path = f"data/interim/merged_dataset_{stamp}.csv"
out.to_csv(out_path, index=False)

print(f"Merged rows: {len(out)}")
print(f"Saved: {out_path}")
