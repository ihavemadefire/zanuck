import pandas as pd

FILMS_CSV = "films_cleaned.csv"
A24_CSV = "a24_released_2010s_2020s.csv"
NEON_CSV = "neon_released_2010s_2020s.csv"
MUBI_CSV = "mubi_released_2016_plus.csv"
OUT_CSV = "films_with_urls.csv"


def normalize_title(series):
    return (
        series.astype(str)
        .str.lower()
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )


films = pd.read_csv(FILMS_CSV)
a24 = pd.read_csv(A24_CSV)
neon = pd.read_csv(NEON_CSV)
mubi = pd.read_csv(MUBI_CSV)

# Normalize source schemas
a24_urls = pd.DataFrame({
    "company": "A24",
    "title": a24["title"],
    "year": a24["release_date"].astype(str).str.extract(r"((?:19|20)\d{2})")[0],
    "wiki_url": a24["wiki_url"],
})

neon_urls = pd.DataFrame({
    "company": "Neon",
    "title": neon["title"],
    "year": neon["year"],
    "wiki_url": neon["wiki_url"],
})

mubi_urls = pd.DataFrame({
    "company": "Mubi",
    "title": mubi["title"],
    "year": mubi["year"],
    "wiki_url": mubi["wiki_url"],
})

urls = pd.concat([a24_urls, neon_urls, mubi_urls], ignore_index=True)

# Normalize keys
films["company_key"] = films["company"].astype(str).str.strip().str.lower()
films["title_key"] = normalize_title(films["title"])
films["year_key"] = pd.to_numeric(films["year"], errors="coerce").astype("Int64")

urls["company_key"] = urls["company"].astype(str).str.strip().str.lower()
urls["title_key"] = normalize_title(urls["title"])
urls["year_key"] = pd.to_numeric(urls["year"], errors="coerce").astype("Int64")

# Keep only one row per unique source key
urls = urls.drop_duplicates(subset=["company_key", "title_key", "year_key"])

merged = films.merge(
    urls[["company_key", "title_key", "year_key", "wiki_url"]],
    on=["company_key", "title_key", "year_key"],
    how="left",
    validate="many_to_one",
)

merged = merged.drop(columns=["company_key", "title_key", "year_key"])

merged.to_csv(OUT_CSV, index=False)

print(f"Wrote {len(merged)} rows -> {OUT_CSV}")
print("Missing wiki_url:", merged["wiki_url"].isna().sum())
print("Duplicate company/title/year rows:",
      merged.duplicated(subset=["company", "title", "year"]).sum())