from datetime import datetime
from glob import glob
from pathlib import Path
import re
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup
from loguru import logger
import pandas as pd
import requests


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


def get_alma_or_education(name: str):
    url = f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}"
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        resp.raise_for_status()
    except requests.RequestException:
        return None
    soup = BeautifulSoup(resp.text, "html.parser")

    # Try multiple infobox class variations
    table_classes = ["infobox biography vcard", "infobox card", "infobox vcard", "infobox"]

    table = None
    for class_name in table_classes:
        table = soup.find("table", class_=class_name)
        if table:
            break

    if not table:
        return None

    # Look for both "Alma mater" and "Education"
    label = None
    for search_term in ["alma", "education"]:
        label = table.find(
            "th", class_="infobox-label", string=lambda text: text and search_term in text.lower()
        )
        if label:
            break

    data = label.find_next_sibling("td") if label else None
    if not data:
        return None

    # Get all text and format with label
    education_text = data.get_text(" ", strip=True)
    return education_text


def scrape_university_degree(limit: int | None = None) -> Path:
    files = glob("data/interim/forbes/billionaires_*.csv")
    if not files:
        raise FileNotFoundError(
            "No Forbes interim CSV found. Run src/dataset.py or create data/interim/forbes first."
        )

    latest_file = max(files)
    df = pd.read_csv(latest_file)
    names = df["name"].head(limit) if limit is not None else df["name"]
    total = len(names)

    results = []
    for index, name in enumerate(names, start=1):
        logger.info(
            "Scraping education {current}/{total}: {name}", current=index, total=total, name=name
        )
        clean_name_str = clean_name(name)
        edu = get_alma_or_education(clean_name_str)
        results.append(
            {
                "forbes_name": name,
                "clean_name": clean_name_str,
                "education": edu,
            }
        )

    stamp = datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d")
    out_dir = Path("data/external/web_scraped")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"wiki_university_degree_{stamp}.csv"
    pd.DataFrame(results).to_csv(out_path, index=False)
    return out_path


if __name__ == "__main__":
    path = scrape_university_degree()
    print(f"Saved education scrape -> {path}")
