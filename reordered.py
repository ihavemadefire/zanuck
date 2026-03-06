import pandas as pd

INPUT = "films_enriched.csv"
OUTPUT = "films_enriched_fixed_genre.csv"

df = pd.read_csv(INPUT)

def move_horror_first(genre_string):

    if pd.isna(genre_string):
        return genre_string

    genres = [g.strip() for g in genre_string.split(",")]

    if "Horror" in genres:
        genres.remove("Horror")
        genres.insert(0, "Horror")

    return ", ".join(genres)

df["genre"] = df["genre"].apply(move_horror_first)

df.to_csv(OUTPUT, index=False)

print("Saved corrected genre file:", OUTPUT)