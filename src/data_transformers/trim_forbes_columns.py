"""
Trim Forbes billionaire CSV.

This script:
1. Locates the single input CSV in `data/interim/forbes/` (created earlier from JSON).
2. Loads it into a pandas DataFrame.
3. Drops extra columns (`id`, `image`, `previous_worth`) if they exist.
4. Saves the cleaned data back into the same folder as `trimmed_<date>.csv`.
"""

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


def trim_forbes_columns(input_path: Path) -> Path:
    df_forbes = pd.read_csv(input_path)

    cols_to_drop = ["id", "image", "previous_worth"]
    df_forbes = df_forbes.drop(columns=[c for c in cols_to_drop if c in df_forbes.columns])

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_path = Path("data/interim") / f"trimmed_{stamp}.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    df_forbes.to_csv(out_path, index=False)
    return out_path
