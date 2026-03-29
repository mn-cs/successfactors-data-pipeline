from glob import glob
import os
from pathlib import Path

from dotenv import load_dotenv

from src.api_fetchers.forbes_billionaires_api_fetch import fetch_forbes_json, save_external
from src.data_transformers.clean_date_of_birth import clean_date_of_birth
from src.data_transformers.forbes_json_to_csv import forbes_json_to_csv
from src.data_transformers.merge_interims import merge_interims
from src.data_transformers.split_university_degree import split_university_degree
from src.data_transformers.trim_forbes_columns import trim_forbes_columns
from src.scrapers.date_of_birth import scrape_date_of_birth
from src.scrapers.university_degree import scrape_university_degree

load_dotenv()


def latest_match(pattern: str) -> Path | None:
    matches = glob(pattern)
    if not matches:
        return None
    return Path(max(matches))


def get_scrape_limit() -> int | None:
    raw_limit = os.getenv("SCRAPE_LIMIT", "10").strip()
    if raw_limit.lower() in {"all", "full", "none", ""}:
        return None

    try:
        limit = int(raw_limit)
    except ValueError as exc:
        raise ValueError("SCRAPE_LIMIT must be a positive integer or 'all'.") from exc

    if limit <= 0:
        raise ValueError("SCRAPE_LIMIT must be a positive integer or 'all'.")

    return limit


def main() -> None:
    """
    Run the full data preparation pipeline.

    Steps:
    1. Fetch raw Forbes billionaire data from the API.
    2. Save raw JSON to the external data directory.
    3. Convert raw Forbes JSON to interim CSV.
    4. Trim unnecessary Forbes columns.
    5. Clean scraped date-of-birth data.
    6. Split scraped education data into university/degree columns.
    7. Merge interim datasets into one final processed dataset.
    """
    raw_data = fetch_forbes_json(page=1)
    raw_json_path = save_external(raw_data)

    forbes_csv_path = forbes_json_to_csv(raw_json_path)
    trimmed_csv_path = trim_forbes_columns(forbes_csv_path)
    scrape_limit = get_scrape_limit()

    dob_scrape_path = latest_match("data/external/web_scraped/wiki_date_of_birth_*.csv")
    if dob_scrape_path is None:
        dob_scrape_path = scrape_date_of_birth(limit=scrape_limit)

    edu_scrape_path = latest_match("data/external/web_scraped/wiki_university_degree_*.csv")
    if edu_scrape_path is None:
        edu_scrape_path = scrape_university_degree(limit=scrape_limit)

    dob_csv_path = clean_date_of_birth(dob_scrape_path)
    edu_csv_path = split_university_degree(edu_scrape_path)

    merged_csv_path = merge_interims(
        trimmed_path=trimmed_csv_path,
        dob_path=dob_csv_path,
        edu_path=edu_csv_path,
    )

    print(f"Pipeline complete. Final dataset saved to: {merged_csv_path}")


if __name__ == "__main__":
    main()
