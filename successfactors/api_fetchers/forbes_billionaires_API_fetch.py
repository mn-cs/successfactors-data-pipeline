"""
Fetch Forbes billionaire data from API.

This script:
1. Reads your RAPIDAPI_KEY from `.env`.
2. Calls the Forbes Billionaires API (via RapidAPI) to fetch JSON data.
3. Saves the raw API response into `data/external/forbes/` as `fetched_data_<date>.json`.

Usage:
- Make sure you have a `.env` file with RAPIDAPI_KEY set.
- Run the script directly to download and save the latest data.
"""

import os
import json
from pathlib import Path
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone


load_dotenv()
API_KEY = os.getenv("RAPIDAPI_KEY")
if not API_KEY:
    raise RuntimeError("RAPIDAPI_KEY missing. Put it in your .env file.")

# Timestamped output filename
stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# Function to fetch data from the Forbes Billionaires API
def fetch_forbes_json(page: int = 1) -> dict:
    url = "https://forbes-billionaires-api.p.rapidapi.com/list.php"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "forbes-billionaires-api.p.rapidapi.com",
    }
    resp = requests.get(url, headers=headers, params={"page": page}, timeout=30)
    resp.raise_for_status()
    return resp.json()

# Function to save the raw JSON response
def save_external(data: dict, fname: str = f"forbes_billionaires_{stamp}.json"):
    ext = Path("data/external/API_fetched"); ext.mkdir(parents=True, exist_ok=True)
    with open(ext / fname, "w") as f:
        json.dump(data, f)
    print(f"Saved raw API response → {ext/fname}")

if __name__ == "__main__":
    data = fetch_forbes_json(page=1)
    save_external(data)
