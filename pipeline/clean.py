import pandas as pd

df = pd.read_csv("data/combined_newss.csv")

df.drop_duplicates(inplace=True)

df.dropna(inplace=True)

df = df[df["title"].str.len() > 10]

df.to_csv("data/cleaned_news.csv", index=False)

print("Cleand news is Saved")