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

import re
import pandas as pd
import numpy as np
import glob
from datetime import datetime, timezone

def parse_education(edu: str):
    """
    Parse education string into up to 3 (university, degree) pairs.
    Always match 'text before ( ... )' as university, inside as degree.
    """
    if pd.isna(edu) or not str(edu).strip():
        return [(None, None)] * 3
    s = str(edu).replace("\xa0", " ")
    pairs = []
    # regex: capture (university name)(degree inside)
    # non-greedy before, then parentheses
    pattern = re.compile(r"\s*([^()]+?)\s*\(([^()]*)\)")
    for m in pattern.finditer(s):
        uni = m.group(1).strip(" ,;")
        deg = m.group(2).strip()
        pairs.append((uni, deg))
        if len(pairs) == 3:
            break
    # If nothing matched (no parentheses at all) → treat as one university, no degree
    if not pairs:
        pairs.append((s.strip(), None))
    # Pad to 3
    while len(pairs) < 3:
        pairs.append((None, None))
    return pairs

# Load data
splited_path = glob.glob("data/external/web_scraped/wiki_university_degree_*.csv")[0]
df = pd.read_csv(splited_path)

# Parse education column
parsed = df["education"].apply(parse_education)

# Create new columns
for i in range(3):
    df[f"university_{i+1}"] = parsed.apply(lambda lst: lst[i][0])
    df[f"degree_{i+1}"] = parsed.apply(lambda lst: lst[i][1])

# Save with timestamp in the same folder
stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
out_file = f"data/interim/splited_edu_{stamp}.csv"
df.to_csv(out_file, index=False)