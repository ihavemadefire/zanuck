import pandas as pd

df = pd.read_csv("films_enriched.csv")

print(df.head())
print(df.describe())
print(df.groupby("company").size())