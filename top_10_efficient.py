import pandas as pd

INPUT = "films_with_budget.csv"
OUTPUT = "top_10_capital_efficient.csv"

def main():
    df = pd.read_csv(INPUT)

    # Ensure numeric types
    df["budget"] = pd.to_numeric(df["budget"], errors="coerce")
    df["box_office"] = pd.to_numeric(df["box_office"], errors="coerce")

    # Drop unusable rows
    df = df.dropna(subset=["budget", "box_office"]).copy()
    df = df[df["budget"] > 0].copy()

    # Capital efficiency metric
    df["roi"] = df["box_office"] / df["budget"]

    # Sort descending and keep top 10
    top10 = (
        df.sort_values("roi", ascending=False)
          .loc[:, ["company", "title", "year", "budget", "box_office", "roi"]]
          .head(10)
          .reset_index(drop=True)
    )

    # Save output
    top10.to_csv(OUTPUT, index=False)

    # Pretty print
    print(f"Wrote {len(top10)} rows -> {OUTPUT}\n")
    print(top10.to_string(index=False))

if __name__ == "__main__":
    main()