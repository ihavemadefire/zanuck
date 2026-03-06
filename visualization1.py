import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("films_cleaned.csv")

df["genre"] = df["genre"].str.split(",").str[0]

genre_counts = df.groupby(["company","genre"]).size().unstack(fill_value=0)

genre_counts.plot(
    kind="bar",
    stacked=True,
    figsize=(12,6)
)

plt.title("Genre Composition by Distributor")
plt.ylabel("Number of Films")

plt.tight_layout()
plt.show()