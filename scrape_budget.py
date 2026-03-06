import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

INPUT = "films_with_urls.csv"
OUTPUT = "films_with_budget.csv"

HEADERS = {
    "User-Agent": "dddm-project/1.0"
}


def get_budget_cell_text(url: str):
    """
    Fetch a Wikipedia film page and return the raw text from the infobox
    row whose header is exactly 'Budget'.
    """
    if pd.isna(url) or not str(url).strip():
        return None

    r = requests.get(url, timeout=20, headers=HEADERS)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    infobox = soup.find("table", class_="infobox")

    if not infobox:
        return None

    for tr in infobox.find_all("tr"):
        th = tr.find("th")
        td = tr.find("td")

        if not th or not td:
            continue

        header = " ".join(th.get_text(" ", strip=True).split()).lower()

        if header == "budget":
            return " ".join(td.get_text(" ", strip=True).split())

    return None


def parse_budget(text: str):
    """
    Convert raw Wikipedia budget text into an integer USD value.

    Handles examples like:
    - $10 million
    - $8–10 million
    - $8-10 million
    - $150,000
    """
    if not text:
        return None

    # Remove citation markers like [1], [2]
    text = re.sub(r"\[[^\]]*\]", "", text)
    text = " ".join(text.split())
    lower = text.lower()

    # Match ranges like $8–10 million or $8-10 million
    m = re.search(r"\$([\d\.]+)\s*[–-]\s*([\d\.]+)\s*million", lower)
    if m:
        low = float(m.group(1))
        high = float(m.group(2))
        return int(((low + high) / 2) * 1_000_000)

    # Match single values like $10 million
    m = re.search(r"\$([\d\.]+)\s*million", lower)
    if m:
        return int(float(m.group(1)) * 1_000_000)

    # Match plain dollar amounts like $150,000
    m = re.search(r"\$([\d,]+)", text)
    if m:
        return int(m.group(1).replace(",", ""))

    return None


def main():
    df = pd.read_csv(INPUT)

    if "wiki_url" not in df.columns:
        raise RuntimeError(f"{INPUT} is missing required column: wiki_url")

    raw_budget_texts = []
    parsed_budgets = []

    for url in tqdm(df["wiki_url"], total=len(df), desc="Scraping budgets"):
        try:
            raw = get_budget_cell_text(url)
        except Exception:
            raw = None

        raw_budget_texts.append(raw)
        parsed_budgets.append(parse_budget(raw))

        time.sleep(0.15)

    df["budget_raw"] = raw_budget_texts
    df["budget"] = parsed_budgets

    df.to_csv(OUTPUT, index=False)

    print(f"Wrote {len(df)} rows -> {OUTPUT}")
    print("Budgets found:", df["budget"].notna().sum())

    sample = df.loc[df["budget"].notna(), ["title", "year", "budget_raw", "budget"]].head(10)
    if not sample.empty:
        print("\nSample parsed budgets:")
        print(sample.to_string(index=False))
    else:
        print("\nNo budgets found. Check wiki_url values and try a manual page test.")


if __name__ == "__main__":
    main()