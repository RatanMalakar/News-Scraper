import pandas as pd

df = pd.read_csv("data/combined_news.csv")

# Removing duplicates 
df.drop_duplicates(inplace=True)

# Removing empty places
df.dropna(inplace=True)

# Removing short titles 
df = df[df["title"].str.len() > 10]

# Save to clean csv file
df.to_csv("data/cleaned_news_file.csv", index=False)

print("Cleand news is Saved")