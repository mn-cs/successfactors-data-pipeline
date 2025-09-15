"""
Module to drop the 'wiki_name' column from the scraped date of birth file
and save the result into data/interim/ with a timestamped filename.
"""

import glob
import pandas as pd
from datetime import datetime, timezone

# Load the latest scraped date of birth file
splited_path = glob.glob("data/external/web_scraped/wiki_date_of_birth_*.csv")[0]
df = pd.read_csv(splited_path)

# Drop wiki_name
df = df.drop(columns=["wiki_name"], errors="ignore")

# Save to interim with timestamp
stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
out_file = f"data/interim/date_of_birth_{stamp}.csv"
df.to_csv(out_file, index=False)

print(f"Saved cleaned file to: {out_file}")
