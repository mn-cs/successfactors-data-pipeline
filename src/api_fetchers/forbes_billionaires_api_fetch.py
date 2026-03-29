"""
Fetch Forbes billionaire data from the RapidAPI endpoint
and save the raw JSON response to the external data directory.
"""

from datetime import datetime, timezone
import json
import os
from pathlib import Path

from dotenv import load_dotenv
import requests

from src.config import EXTERNAL_DATA_DIR


def get_api_key() -> str:
    load_dotenv()
    api_key = os.getenv("RAPIDAPI_KEY")
    if not api_key:
        raise RuntimeError("RAPIDAPI_KEY missing. Put it in your .env file.")
    return api_key


def fetch_forbes_json(page: int = 1) -> dict:
    api_key = get_api_key()

    url = "https://forbes-billionaires-api.p.rapidapi.com/list.php"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "forbes-billionaires-api.p.rapidapi.com",
    }

    resp = requests.get(url, headers=headers, params={"page": page}, timeout=30)
    resp.raise_for_status()
    return resp.json()


def save_external(data: dict) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_dir = EXTERNAL_DATA_DIR / "api_fetched"
    out_dir.mkdir(parents=True, exist_ok=True)

    file_path = out_dir / f"forbes_billionaires_{stamp}.json"

    with open(file_path, "w") as f:
        json.dump(data, f)

    return file_path


if __name__ == "__main__":
    data = fetch_forbes_json(page=1)
    path = save_external(data)
    print(f"Saved raw API response → {path}")
