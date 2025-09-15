"""
Process Forbes billionaire data.

This script:
1. Loads the latest JSON file from `data/external/forbes/` (fetched via API).
2. Converts the "ranking" section into a pandas DataFrame.
3. Saves the structured data as a timestamped CSV in `data/interim/forbes/billionaires_<date>.json`.
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime, timezone
from glob import glob

# find the latest fetched JSON file
file = glob("data/external/API_fetched/forbes_billionaires_*.json")

# ensure we found a file
if not file:
    raise FileNotFoundError("No forbes_billionaires_*.json file found in data/external/forbes")

# if multiple, take the first (should only be one)
file = file[0]

# load the JSON you saved earlier
with open(file, "r") as f:
    data = json.load(f)

# convert to DataFrame
df = pd.DataFrame(data["ranking"])

# Timestamped output filename
stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# save to interim as CSV
Path("data/interim/forbes").mkdir(parents=True, exist_ok=True)
df.to_csv(f"data/interim/billionaires_{stamp}.csv", index=False)

print("Saved structured CSV to data/interim/forbes/")
