import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

NEON_URL = "https://en.wikipedia.org/wiki/List_of_Neon_films"
BASE = "https://en.wikipedia.org"

def _clean_ws(s: str) -> str:
    return " ".join(s.split())

def _find_heading_by_text(soup: BeautifulSoup, text: str):
    """
    Find a Wikipedia section heading by its displayed text (e.g., '2010s').
    Works even if there is no id='2010s' present in the HTML response.
    """
    target = text.strip().casefold()

    # Most common: <span class="mw-headline">2010s</span>
    for span in soup.select("span.mw-headline"):
        if span.get_text(strip=True).casefold() == target:
            # Return the heading tag (h2/h3/h4...) if possible
            return span.find_parent(re.compile(r"^h[1-6]$")) or span

    # Fallback: heading might be plain text in <h3> etc.
    for h in soup.find_all(re.compile(r"^h[1-6]$")):
        if h.get_text(" ", strip=True).casefold() == target:
            return h

    return None

def _extract_year_from_release_date(release_date: str):
    m = re.search(r"\b(19|20)\d{2}\b", release_date)
    return int(m.group(0)) if m else None

def scrape_neon_released_2010s_2020s(url: str = NEON_URL) -> pd.DataFrame:
    """
    Scrape Neon 'Released films' tables for the 2010s and 2020s.
    Returns: company, decade, release_date, year, title, wiki_url
    """
    html = requests.get(url, timeout=30, headers={"User-Agent": "dddm-project/1.0"}).text
    soup = BeautifulSoup(html, "html.parser")

    rows = []
    for decade in ["2010s", "2020s"]:
        heading = _find_heading_by_text(soup, decade)
        if not heading:
            raise RuntimeError(f"Could not find heading text '{decade}' on Neon page")

        table = heading.find_next("table", class_="wikitable")
        if not table:
            raise RuntimeError(f"Found heading '{decade}' but no following wikitable")

        for tr in table.select("tr"):
            tds = tr.find_all("td")
            if len(tds) < 2:
                continue

            release_date = _clean_ws(tds[0].get_text(" ", strip=True))
            year = _extract_year_from_release_date(release_date)

            # Film title usually appears as an italicized wiki link
            a = tr.select_one("i a[href^='/wiki/']") or tr.select_one("a[href^='/wiki/']")
            if not a:
                continue

            title = _clean_ws(a.get_text(strip=True))
            wiki_url = BASE + a["href"]

            rows.append({
                "company": "Neon",
                "decade": decade,
                "release_date": release_date,
                "year": year,
                "title": title,
                "wiki_url": wiki_url,
            })

    df = pd.DataFrame(rows)

    # De-dupe conservatively (title+year is usually enough here)
    df = df.drop_duplicates(subset=["title", "year"], keep="first").reset_index(drop=True)
    return df

if __name__ == "__main__":
    df = scrape_neon_released_2010s_2020s()
    out = "neon_released_2010s_2020s.csv"
    df.to_csv(out, index=False)
    print(f"Wrote {len(df)} rows -> {out}")
    print(df.head(10))