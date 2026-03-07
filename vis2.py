import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("films_with_budget.csv")

df["primary_genre"] = df["genre"].str.split(",").str[0].str.strip()

df["imdb_rating"] = pd.to_numeric(df["imdb_rating"], errors="coerce")
df["box_office"] = pd.to_numeric(df["box_office"], errors="coerce")
df["metascore"] = pd.to_numeric(df["metascore"], errors="coerce")
df["budget"] = pd.to_numeric(df["budget"], errors="coerce")

df = df.dropna(subset=["imdb_rating", "budget"])

plt.figure(figsize=(12,8))

ax = sns.scatterplot(
    data=df,
    x="budget",
    y="imdb_rating",
    hue="primary_genre",
    size="runtime",
    sizes=(20,400),
    alpha=0.7
)

sns.regplot(
    data=df,
    x="budget",
    y="imdb_rating",
    scatter=False,
    logx=True,
    color="black",
    line_kws={"linewidth":2}
)

# Remove runtime legend entries
handles, labels = ax.get_legend_handles_labels()

genre_count = df["primary_genre"].nunique()

ax.legend(
    handles[:genre_count+1],
    labels[:genre_count+1],
    title="Genre",
    bbox_to_anchor=(1.05,1),
    loc="upper left"
)

plt.xscale("log")

plt.title("Budget vs Critical Success of Independent Films")
plt.xlabel("Production Budget (log scale)")
plt.ylabel("IMDb Rating")

plt.tight_layout()
plt.show()