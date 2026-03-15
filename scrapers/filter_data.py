import pandas as pd

df = pd.read_csv("data/cleaned_news_file.csv")

keywords = ["ai",
            "gpt",
            "neural",
            "model",
             "artificial", "machine", "learning", "openai"]

def is_ai(title):
    title=title.lower()
    return any(word in title for word in keywords)

df = df[df["title"].apply(is_ai)]

df.to_csv("data/filtered_news.csv" , index=False)

print("Saved final csv file")