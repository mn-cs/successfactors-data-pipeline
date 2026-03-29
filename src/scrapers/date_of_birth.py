from datetime import datetime, timezone
from glob import glob
from pathlib import Path
import random
import re
import time

from bs4 import BeautifulSoup
from loguru import logger
import pandas as pd
import requests


# ---------- tiny helpers ----------
def clean_slug(s: str) -> str:
    s = s.strip().replace(" ", "_")
    # drop *_&_family / -and-family / _and_family
    s = re.sub(r"(_|-)?(%26|&|and)?(_|-)?family$", "", s, flags=re.I)
    s = re.sub(r"_+", "_", s).strip("_")
    return s


def wikipedia_search_best_title(query: str) -> str | None:
    """Use Wikipedia opensearch to find the best page title for a query."""
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "opensearch",
        "search": query,
        "limit": 1,
        "namespace": 0,
        "format": "json",
    }
    r = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    r.raise_for_status()
    data = r.json()
    if len(data) >= 2 and data[1]:
        return data[1][0]  # first title string
    return None


def scrape_birthdate(slug: str):
    """Return {'wiki_name', clean_name, 'year','month','day'}, using search fallback on 404."""

    def try_fetch(slug_try: str):
        url = f"https://en.wikipedia.org/wiki/{slug_try}"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        infobox = soup.select_one("table.infobox")
        if not infobox:
            return {
                "wiki_name": slug_try,
                "clean_name": slug,
                "year": None,
                "month": None,
                "day": None,
            }
        # Born row
        td = None
        for th in infobox.select("th"):
            if th.get_text(strip=True) == "Born":
                td = th.find_next_sibling("td")
                break
        if not td:
            return {
                "wiki_name": slug_try,
                "clean_name": slug,
                "year": None,
                "month": None,
                "day": None,
            }
        bday = td.select_one(".bday")
        if bday and re.fullmatch(r"\d{4}-\d{2}-\d{2}", bday.text.strip()):
            y, m, d = map(int, bday.text.strip().split("-"))
            return {"wiki_name": slug_try, "clean_name": slug, "year": y, "month": m, "day": d}
        return {
            "wiki_name": slug_try,
            "clean_name": slug,
            "year": None,
            "month": None,
            "day": None,
        }

    # 1) try cleaned slug directly
    cleaned = clean_slug(slug)
    try:
        return try_fetch(cleaned)
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code == 404:
            # 2) fall back: search by natural name (underscores -> spaces)
            title = wikipedia_search_best_title(cleaned.replace("_", " "))
            if title:
                # retry using the found title as slug
                found_slug = title.replace(" ", "_")
                try:
                    return try_fetch(found_slug)
                except Exception:
                    pass
        # any other HTTP error -> just return None fields
        return {"wiki_name": cleaned, "clean_name": slug, "year": None, "month": None, "day": None}
    except Exception:
        return {"wiki_name": cleaned, "clean_name": slug, "year": None, "month": None, "day": None}


def clean_name(name: str) -> str:
    """Remove family indicators and other common patterns"""
    patterns = [
        r"\s*&\s*family\s*$",
        r"\s*family\s*$",
        r"\s*&\s*co\.?\s*$",
        r"\s*&\s*sons?\s*$",
        r"\s*&\s*daughters?\s*$",
    ]

    cleaned = name
    for pattern in patterns:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE).strip()

    return cleaned


def scrape_date_of_birth(limit: int | None = None) -> Path:
    files = glob("data/interim/forbes/billionaires_*.csv")
    if not files:
        raise FileNotFoundError(
            "No Forbes interim CSV found. Run src/dataset.py or create data/interim/forbes first."
        )

    latest_file = max(files)
    df = pd.read_csv(latest_file)
    names = df["name"].head(limit) if limit is not None else df["name"]
    total = len(names)

    records = []
    for index, slug in enumerate(names, start=1):
        logger.info(
            "Scraping birth date {current}/{total}: {name}", current=index, total=total, name=slug
        )
        records.append(scrape_birthdate(slug))
        time.sleep(0.4 + random.random() * 0.6)  # be polite

    out = pd.DataFrame(records)
    for col in ["year", "month", "day"]:
        out[col] = pd.to_numeric(out[col], errors="coerce").astype("Int64")

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_dir = Path("data/external/web_scraped")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"wiki_date_of_birth_{stamp}.csv"
    out.to_csv(out_path, index=False)
    return out_path


if __name__ == "__main__":
    path = scrape_date_of_birth()
    print(f"Saved birthdate scrape -> {path}")
