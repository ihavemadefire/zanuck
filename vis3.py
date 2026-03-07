import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("films_with_budget.csv")

df["budget"] = pd.to_numeric(df["budget"], errors="coerce")
df["box_office"] = pd.to_numeric(df["box_office"], errors="coerce")
df["imdb_rating"] = pd.to_numeric(df["imdb_rating"], errors="coerce")

# Keep only the first genre
df["genre"] = df["genre"].astype(str).str.split(",").str[0].str.strip()

# Drop bad rows
df = df.dropna(subset=["budget", "box_office", "genre"])

# Revenue efficiency metric
df["roi"] = df["box_office"] / df["budget"]

plt.figure(figsize=(12,8))

sns.scatterplot(
    data=df,
    x="budget",
    y="roi",
    hue="genre",
    size="imdb_rating",
    sizes=(40,400),
    alpha=0.7
)

plt.xscale("log")

plt.title("Revenue Efficiency of Independent Film Investments")
plt.xlabel("Production Budget (log scale)")
plt.ylabel("Revenue Efficiency (Box Office / Budget)")

plt.legend(bbox_to_anchor=(1.05,1), loc="upper left")

plt.tight_layout()
plt.show()