import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

MUBI_URL = "https://en.wikipedia.org/wiki/List_of_Mubi_films"
BASE = "https://en.wikipedia.org"

def _clean_ws(s: str) -> str:
    return " ".join(s.split())

def _is_year(text: str) -> bool:
    return bool(re.fullmatch(r"(19|20)\d{2}", text.strip()))

def _find_heading(soup: BeautifulSoup, heading_text: str):
    target = heading_text.strip().casefold()
    for h in soup.find_all(["h2", "h3"]):
        txt = _clean_ws(h.get_text(" ", strip=True)).casefold()
        if txt == target:
            return h
    return None

def scrape_mubi_released_by_year(url: str = MUBI_URL, year_start: int = 2016) -> pd.DataFrame:
    html = requests.get(url, timeout=30, headers={"User-Agent": "dddm-project/1.0"}).text
    soup = BeautifulSoup(html, "html.parser")

    released_h = _find_heading(soup, "Released films")
    if not released_h:
        raise RuntimeError("Could not find 'Released films' heading")

    rows = []

    # Iterate forward through headings after "Released films"
    # Stop when we hit the next major section (h2), e.g. "Upcoming"
    for tag in released_h.find_all_next(["h2", "h3"]):
        if tag.name == "h2":
            # reached next major section
            break

        if tag.name == "h3":
            year_text = _clean_ws(tag.get_text(" ", strip=True))
            if not _is_year(year_text):
                continue

            year = int(year_text)
            if year < year_start:
                continue

            table = tag.find_next("table", class_="wikitable")
            if not table:
                continue

            # Parse the table rows
            for tr in table.select("tr"):
                tds = tr.find_all("td")
                if len(tds) < 2:
                    continue  # header row or malformed

                theatrical_release = _clean_ws(tds[0].get_text(" ", strip=True))

                # Film title is a wiki link in one of the later columns
                a = tr.select_one("i a[href^='/wiki/']") or tr.select_one("a[href^='/wiki/']")
                if not a:
                    continue

                title = _clean_ws(a.get_text(strip=True))
                wiki_url = BASE + a["href"]

                rows.append({
                    "company": "Mubi",
                    "year": year,
                    "theatrical_release": theatrical_release,
                    "title": title,
                    "wiki_url": wiki_url,
                })

    df = pd.DataFrame(rows)

    # De-dupe just in case
    if not df.empty:
        df = df.drop_duplicates(subset=["title", "year"], keep="first").reset_index(drop=True)

    return df

if __name__ == "__main__":
    df = scrape_mubi_released_by_year()

    out = "mubi_released_2016_plus.csv"
    df.to_csv(out, index=False)

    print(f"Wrote {len(df)} rows -> {out}")
    print(df.head(10))