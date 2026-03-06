import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("films_with_budget.csv")

df["budget"] = pd.to_numeric(df["budget"], errors="coerce")
df["box_office"] = pd.to_numeric(df["box_office"], errors="coerce")

df = df.dropna(subset=["budget","box_office"])

plt.figure(figsize=(12,8))

sns.scatterplot(
    data=df,
    x="budget",
    y="box_office",
    hue="company",
    size="imdb_rating",
    sizes=(40,400),
    alpha=0.7
)

plt.xscale("log")
plt.yscale("log")

plt.title("Efficiency Frontier of Independent Film Investments")
plt.xlabel("Production Budget (log scale)")
plt.ylabel("Box Office Revenue (log scale)")

plt.legend(bbox_to_anchor=(1.05,1), loc="upper left")

plt.tight_layout()
plt.show()