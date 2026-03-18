import pandas as pd 

df1 = pd.read_csv("data/techcrunch_news.csv")
df2 = pd.read_csv("data/hackernews_stories.csv")

df = pd.concat([df1,df2])

df.to_csv("data/combined_newss.csv", index=False)

print("Combined file created ")


