import pandas as pd

films = pd.read_csv("films_cleaned.csv")

a24 = pd.read_csv("a24_released_2010s_2020s.csv")
neon = pd.read_csv("neon_released_2010s_2020s.csv")
mubi = pd.read_csv("mubi_released_2016_plus.csv")

urls = pd.concat([a24, neon, mubi])

urls = urls[["title","wiki_url"]]

# normalize titles for safer merging
films["title_norm"] = films["title"].str.lower().str.strip()
urls["title_norm"] = urls["title"].str.lower().str.strip()

merged = films.merge(
    urls[["title_norm","wiki_url"]],
    on="title_norm",
    how="left"
)

merged.drop(columns=["title_norm"], inplace=True)

merged.to_csv("films_with_urls.csv", index=False)

print("Rows:", len(merged))
print("Missing URLs:", merged["wiki_url"].isna().sum())