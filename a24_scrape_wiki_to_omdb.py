import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

A24_URL = "https://en.wikipedia.org/wiki/List_of_A24_films"
BASE = "https://en.wikipedia.org"

def _clean_ws(s: str) -> str:
    return " ".join(s.split())

def _find_heading_by_text(soup: BeautifulSoup, text: str):
    """
    Find a Wikipedia section heading element by its displayed text (e.g., '2010s').
    Works even if there is no id='2010s' in the HTML you got.
    """
    target = text.strip().casefold()

    # Wikipedia headings often look like:
    # <h3><span class="mw-headline" ...>2010s</span></h3>
    for span in soup.select("span.mw-headline"):
        if span.get_text(strip=True).casefold() == target:
            return span.find_parent(re.compile(r"^h[1-6]$")) or span

    # Fallback: sometimes headings are plain h3/h4 text without mw-headline span
    for h in soup.find_all(re.compile(r"^h[1-6]$")):
        if h.get_text(" ", strip=True).casefold() == target:
            return h

    return None

def scrape_a24_released_2010s_2020s(url: str = A24_URL) -> pd.DataFrame:
    html = requests.get(url, timeout=30, headers={"User-Agent": "dddm-project/1.0"}).text
    soup = BeautifulSoup(html, "html.parser")

    rows = []

    for decade in ["2010s", "2020s"]:
        heading = _find_heading_by_text(soup, decade)
        if not heading:
            raise RuntimeError(
                f"Could not find heading text '{decade}'. "
                "Run debug_headings() below to see what headings exist."
            )

        table = heading.find_next("table", class_="wikitable")
        if not table:
            raise RuntimeError(f"Found heading '{decade}' but no following wikitable.")

        for tr in table.select("tr"):
            tds = tr.find_all("td")
            if len(tds) < 2:
                continue  # header row

            release_date = _clean_ws(tds[0].get_text(" ", strip=True))

            # Title is usually italic link; fallback to any wiki link in the row
            a = tr.select_one("i a[href^='/wiki/']") or tr.select_one("a[href^='/wiki/']")
            if not a:
                continue

            title = _clean_ws(a.get_text(strip=True))
            wiki_url = BASE + a["href"]

            rows.append({
                "company": "A24",
                "decade": decade,
                "release_date": release_date,
                "title": title,
                "wiki_url": wiki_url,
            })

    return pd.DataFrame(rows)

# Optional debugging helper
def debug_headings(url: str = A24_URL):
    html = requests.get(url, timeout=30, headers={"User-Agent": "dddm-project/1.0"}).text
    soup = BeautifulSoup(html, "html.parser")
    headlines = [s.get_text(strip=True) for s in soup.select("span.mw-headline")]
    print("mw-headline count:", len(headlines))
    print("first 50 mw-headlines:", headlines[:50])

if __name__ == "__main__":
    # If it fails, run debug_headings() once to inspect what your HTML contains.
    df = scrape_a24_released_2010s_2020s()
    print(df.head(10))
    df.to_csv("a24_released_2010s_2020s.csv", index=False)
    print("Wrote:", len(df)) 