"""
Module to drop the 'wiki_name' column from the scraped date of birth file
and save the result into data/interim/ with a timestamped filename.
"""

from datetime import datetime, timezone
from glob import glob
from pathlib import Path

import pandas as pd


def clean_date_of_birth(input_path: Path | None = None) -> Path:
    if input_path is None:
        files = glob("data/external/web_scraped/wiki_date_of_birth_*.csv")
        if not files:
            raise FileNotFoundError(
                "No scraped date-of-birth file found. Run src/scrapers/date_of_birth.py first."
            )
        input_path = Path(max(files))

    df = pd.read_csv(input_path)

    df = df.drop(columns=["wiki_name"], errors="ignore")

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_path = Path("data/interim") / f"date_of_birth_{stamp}.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(out_path, index=False)
    return out_path
