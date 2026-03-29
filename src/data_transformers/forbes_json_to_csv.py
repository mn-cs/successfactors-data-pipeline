"""
Process Forbes billionaire data.

This script:
1. Loads the latest JSON file from `data/external/forbes/` (fetched via API).
2. Converts the "ranking" section into a pandas DataFrame.
3. Saves the structured data as a timestamped CSV in `data/interim/forbes/billionaires_<date>.json`.
"""

from datetime import datetime, timezone
import json
from pathlib import Path

import pandas as pd


def forbes_json_to_csv(json_path: Path) -> Path:
    with open(json_path, "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data["ranking"])

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_dir = Path("data/interim/forbes")
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / f"billionaires_{stamp}.csv"
    df.to_csv(out_path, index=False)

    return out_path
