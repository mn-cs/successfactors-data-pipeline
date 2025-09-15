import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime
from zoneinfo import ZoneInfo 
from glob import glob

# Load CSV
files = glob("data/interim/forbes/billionaires_*.csv")

# pick the latest one (sorted by filename)
latest_file = max(files)

# load into DataFrame
df = pd.read_csv(latest_file)

def clean_name(name: str) -> str:
    """Remove family indicators and other common patterns"""
    patterns = [
        r'\s*&\s*family\s*$',
        r'\s*family\s*$', 
        r'\s*&\s*co\.?\s*$',
        r'\s*&\s*sons?\s*$',
        r'\s*&\s*daughters?\s*$'
    ]
    
    cleaned = name
    for pattern in patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE).strip()
    
    return cleaned

def get_alma_or_education(name: str):
    url = f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(resp.text, "html.parser")
    
    # Try multiple infobox class variations
    table_classes = [
        "infobox biography vcard",
        "infobox card", 
        "infobox vcard",
        "infobox"
    ]
    
    table = None
    for class_name in table_classes:
        table = soup.find("table", class_=class_name)
        if table:
            break
    
    if not table:
        return None
    
    # Look for both "Alma mater" and "Education"
    label = None
    label_text = None
    for search_term in ["alma", "education"]:
        label = table.find("th", class_="infobox-label", string=lambda text: text and search_term in text.lower())
        if label:
            label_text = label.get_text(strip=True)
            break
    
    data = label.find_next_sibling("td") if label else None
    if not data:
        return None
        
    # Get all text and format with label
    education_text = data.get_text(" ", strip=True)
    return education_text

count = 0
results = []

for name in df["name"]:
    count += 1
    print(count, name)
    clean_name_str = clean_name(name)
    edu = get_alma_or_education(clean_name_str)
    results.append({
        "forbes_name": name,
        "clean_name": clean_name_str,
        "education": edu
    })

stamp = datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d")
out_df = pd.DataFrame(results)
out_df.to_csv(f"data/external/web_scraped/wiki_university_degree_{stamp}.csv", index=False)
print(out_df.head(10))