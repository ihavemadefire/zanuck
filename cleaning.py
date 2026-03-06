import pandas as pd

INPUT = "films_enriched_fixed_genre.csv"
OUTPUT = "films_cleaned.csv"

noise_genres = {
    "Adult",
    "Biography",
    "Music",
    "Short",
    "Talk-Show",
    "Talk Show",
    "Western"
}

df = pd.read_csv(INPUT)

def clean_genres(genre_string):

    if pd.isna(genre_string):
        return genre_string

    genres = [g.strip() for g in genre_string.split(",")]

    # remove noise genres
    genres = [g for g in genres if g not in noise_genres]

    return ", ".join(genres)

df["genre"] = df["genre"].apply(clean_genres)

df.to_csv(OUTPUT, index=False)

print("Saved cleaned dataset:", OUTPUT)