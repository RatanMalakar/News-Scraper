import pandas as pd 

# Read the techcrunch_ai_news.csv and hackernews_ai_stories.csv
df1 = pd.read_csv("data/techcrunch_news.csv")
df2 = pd.read_csv("data/hackernews_stories.csv")

#Combine both
df = pd.concat([df1,df2])

# Save to combined_news.csv without index
# here I stucked almost half an hour jusct because when i named the combined csv i forgot a "_"  means i wrote combined csv instead of combined_csv
df.to_csv("data/combined_newss.csv", index=False)



print("Combined file created ")


