import re
import pandas as pd

A24_CSV = "a24_released_2010s_2020s.csv"
NEON_CSV = "neon_released_2010s_2020s.csv"
MUBI_CSV = "mubi_released_2016_plus.csv"

OUT_CSV = "seed_films.csv"


def year_from_release_date(s: str):
    """
    Extract 4-digit year from strings like 'March 15, 2013'.
    Returns int or None.
    """
    if pd.isna(s):
        return None
    m = re.search(r"\b(19|20)\d{2}\b", str(s))
    return int(m.group(0)) if m else None


def main():
    # -------------------------
    # A24: year derived from release_date
    # -------------------------
    a24 = pd.read_csv(A24_CSV)

    if "release_date" not in a24.columns:
        raise RuntimeError(f"{A24_CSV} missing required column 'release_date'")

    a24_seed = pd.DataFrame({
        "company": "A24",
        "title": a24["title"].astype(str).str.strip(),
        "year": a24["release_date"].apply(year_from_release_date),
    })

    # -------------------------
    # NEON: year already present
    # -------------------------
    neon = pd.read_csv(NEON_CSV)
    if "year" not in neon.columns:
        raise RuntimeError(f"{NEON_CSV} missing required column 'year'")

    neon_seed = pd.DataFrame({
        "company": "Neon",
        "title": neon["title"].astype(str).str.strip(),
        "year": neon["year"],
    })

    # -------------------------
    # MUBI: year already present
    # -------------------------
    mubi = pd.read_csv(MUBI_CSV)
    if "year" not in mubi.columns:
        raise RuntimeError(f"{MUBI_CSV} missing required column 'year'")

    mubi_seed = pd.DataFrame({
        "company": "Mubi",
        "title": mubi["title"].astype(str).str.strip(),
        "year": mubi["year"],
    })

    # -------------------------
    # Combine + clean
    # -------------------------
    df = pd.concat([a24_seed, neon_seed, mubi_seed], ignore_index=True)

    # Drop rows with missing essentials
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["title", "year"]).copy()

    # De-dupe within company (title + year is good enough for our seed)
    df["title_norm"] = df["title"].str.lower().str.replace(r"\s+", " ", regex=True).str.strip()
    df = df.drop_duplicates(subset=["company", "title_norm", "year"]).drop(columns=["title_norm"])

    # Sort for sanity
    df = df.sort_values(["company", "year", "title"]).reset_index(drop=True)

    df.to_csv(OUT_CSV, index=False)

    # -------------------------
    # Quick summary
    # -------------------------
    print(f"Wrote {len(df)} rows -> {OUT_CSV}")
    print(df.groupby("company").size())
    missing_a24_years = a24_seed["year"].isna().sum()
    if missing_a24_years:
        print(f"Warning: {missing_a24_years} A24 rows missing year from release_date")


if __name__ == "__main__":
    main()