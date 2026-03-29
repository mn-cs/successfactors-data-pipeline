"""
This module loads scraped education data and splits each entry into
separate university and degree fields.

- The parse_education() function extracts up to 3 (university, degree) pairs
  by taking the full university name before parentheses and the degree inside parentheses.
- Handles rows with multiple universities, single universities without degrees,
  or missing values, always returning 3 pairs (padding with None if needed).
- Expands these pairs into new columns: university_1..3 and degree_1..3.
- Saves the transformed DataFrame to data/interim/ as a timestamped CSV file.
"""

from datetime import datetime, timezone
from glob import glob
from pathlib import Path
import re

import pandas as pd


def parse_education(edu: str):
    if pd.isna(edu) or not str(edu).strip():
        return [(None, None)] * 3

    s = str(edu).replace("\xa0", " ")
    pairs = []

    pattern = re.compile(r"\s*([^()]+?)\s*\(([^()]*)\)")
    for m in pattern.finditer(s):
        uni = m.group(1).strip(" ,;")
        deg = m.group(2).strip()
        pairs.append((uni, deg))
        if len(pairs) == 3:
            break

    if not pairs:
        pairs.append((s.strip(), None))

    while len(pairs) < 3:
        pairs.append((None, None))

    return pairs


def split_university_degree(input_path: Path | None = None) -> Path:
    if input_path is None:
        files = glob("data/external/web_scraped/wiki_university_degree_*.csv")
        if not files:
            raise FileNotFoundError(
                "No scraped education file found. Run src/scrapers/university_degree.py first."
            )
        input_path = Path(max(files))

    df = pd.read_csv(input_path)

    parsed = df["education"].apply(parse_education)

    for i in range(3):
        df[f"university_{i + 1}"] = parsed.apply(lambda lst: lst[i][0])
        df[f"degree_{i + 1}"] = parsed.apply(lambda lst: lst[i][1])

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_path = Path("data/interim") / f"splited_edu_{stamp}.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(out_path, index=False)
    return out_path
