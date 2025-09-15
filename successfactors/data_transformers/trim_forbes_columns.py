"""
Trim Forbes billionaire CSV.

This script:
1. Locates the single input CSV in `data/interim/forbes/` (created earlier from JSON).
2. Loads it into a pandas DataFrame.
3. Drops extra columns (`id`, `image`, `previous_worth`) if they exist.
4. Saves the cleaned data back into the same folder as `trimmed_<date>.csv`.
"""

import pandas as pd
from datetime import datetime, timezone
from glob import glob

def main():

    # 1. Locate input file
    file = glob("data/interim/forbes/billionaires_*.csv")

    # ensure we found a file
    if not file:
        raise FileNotFoundError("No input CSV found in data/interim/forbes")

    file = file[0]  # should only be one

    # 2. Load CSV
    df_forbes = pd.read_csv(file)

    # 3. Drop unwanted columns if they exist
    cols_to_drop = ["id", "image", "previous_worth"]
    df_forbes = df_forbes.drop(columns=[c for c in cols_to_drop if c in df_forbes.columns])

    # 4. Save with timestamp in the same folder
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_file = f"data/interim/trimmed_{stamp}.csv"
    df_forbes.to_csv(out_file, index=False)

    print(f"Processed Forbes data saved → {out_file}")

if __name__ == "__main__":
    main()