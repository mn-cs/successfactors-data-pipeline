"""
Merge the interim datasets into a single dataset for modeling.
This module defines a function `merge_interims` that takes the
paths to three interim datasets (trimmed, date of birth, and
education) and merges them into a single dataset. The merged
dataset is saved as a CSV file in the `data/processed` directory
with a timestamp in the filename.

The function performs the following steps:

1. Reads the three interim datasets into pandas DataFrames.

2. Normalizes the name columns in each DataFrame by replacing
   non-breaking spaces with regular spaces and stripping
   leading/trailing whitespace.

3. Converts the year, month, and day columns in the date of
   birth DataFrame to numeric types, coercing errors to NaN
   and using the Int64 data type to allow for missing values.

4. Selects the relevant columns from the date of birth and
   education DataFrames for merging.

5. Merges the trimmed DataFrame with the date of birth DataFrame
   on the name columns, and then merges the resulting DataFrame
   with the education DataFrame on the name columns.

6. Saves the final merged DataFrame to a CSV file in the `data/processed`
   directory with a filename that includes the current date in UTC.
"""

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


def merge_interims(trimmed_path: Path, dob_path: Path, edu_path: Path) -> Path:
    df_trim = pd.read_csv(trimmed_path)
    df_dob = pd.read_csv(dob_path)
    df_edu = pd.read_csv(edu_path)

    def norm(s):
        return str(s).replace("\xa0", " ").strip() if pd.notna(s) else s

    df_trim["name"] = df_trim["name"].map(norm)
    df_dob["clean_name"] = df_dob["clean_name"].map(norm)
    df_edu["clean_name"] = df_edu["clean_name"].map(norm)

    for col in ["year", "month", "day"]:
        if col in df_dob.columns:
            df_dob[col] = pd.to_numeric(df_dob[col], errors="coerce").astype("Int64")

    dob_keep = ["clean_name", "year", "month", "day"]
    edu_keep = [
        "clean_name",
        "university_1",
        "degree_1",
        "university_2",
        "degree_2",
        "university_3",
        "degree_3",
    ]

    df_dob = df_dob[dob_keep]
    df_edu = df_edu[edu_keep]

    out = df_trim.merge(df_dob, left_on="name", right_on="clean_name", how="left")
    out = out.drop(columns=["clean_name"])

    out = out.merge(df_edu, left_on="name", right_on="clean_name", how="left")
    out = out.drop(columns=["clean_name"])

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_path = Path("data/processed") / f"merged_dataset_{stamp}.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    out.to_csv(out_path, index=False)
    return out_path
