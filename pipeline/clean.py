import pandas as pd

df = pd.read_csv("data/combined_newss.csv")

# Removing duplicates 
df.drop_duplicates(inplace=True)

# Removing empty places
df.dropna(inplace=True)

# Removing short titles 
df = df[df["title"].str.len() > 10]

# Save to clean csv file
df.to_csv("data/cleaned_news.csv", index=False)

print("Cleand news is Saved")