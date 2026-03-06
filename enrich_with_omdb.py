import os
import time
import requests
import pandas as pd
from tqdm import tqdm

API_KEY = os.getenv("OMDB_API_KEY")

INPUT = "seed_films.csv"
OUTPUT = "films_enriched.csv"

BASE_URL = "http://www.omdbapi.com/"

def fetch_movie(title, year):

    params = {
        "t": title,
        "y": year,
        "apikey": API_KEY
    }

    r = requests.get(BASE_URL, params=params)
    data = r.json()

    if data.get("Response") == "False":
        return None

    return data


def parse_boxoffice(val):
    if not val or val == "N/A":
        return None

    val = val.replace("$","").replace(",","")
    try:
        return int(val)
    except:
        return None


def main():

    df = pd.read_csv(INPUT)

    rows = []

    for _, row in tqdm(df.iterrows(), total=len(df)):

        title = row["title"]
        year = int(row["year"])

        data = fetch_movie(title, year)

        if data is None:
            continue

        rows.append({
            "company": row["company"],
            "title": title,
            "year": year,
            "genre": data.get("Genre"),
            "imdb_rating": data.get("imdbRating"),
            "metascore": data.get("Metascore"),
            "box_office": parse_boxoffice(data.get("BoxOffice")),
            "runtime": data.get("Runtime"),
            "awards": data.get("Awards")
        })

        time.sleep(0.25)

    out = pd.DataFrame(rows)

    out.to_csv(OUTPUT, index=False)

    print("Wrote", len(out), "rows")


if __name__ == "__main__":
    main()