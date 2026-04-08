
import pandas as pd
import logging
import os 

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

os.makedirs("data", exist_ok=True)

df1 = pd.read_csv("data/techcrunch.csv")
df2 = pd.read_csv("data/hackernews.csv")

df = pd.concat([df1,df2])

df.to_csv("data/raw_news.csv", index=False)
logging.info("Combined all news and saved raw data")

df3 = pd.read_csv("data/raw_news.csv")

df3.drop_duplicates(inplace=True)

df3.dropna(inplace=True)

df3 = df3[df3["title"].str.len() > 10]

df3.to_csv("data/cleaned_news.csv", index=False)

df4 = pd.read_csv("data/cleaned_news.csv")

keywords = ["ai",
            "gpt",
            "neural",
            "model",
            "artificial",
            "machine",
            "openai"]

def is_ai(title):
    title=title.lower()
    return any(word in title for word in keywords)

def categorize(title):
    title=title.lower()

    if any(word in title for word in ["openai", "anthropic", "google", "microsoft"]):
        return "AI Companies"
    elif any(word in title for word in ["data center", "gpu", "chip"]):
        return "Infrastructure"
    elif any(word in title for word in ["copilot", "assistant", "app"]):
        return "AI Products"
    elif any(word in title for word in ["research", "model", "llm"]):
        return "AI Research"
    else:
        return "Other"

df["category"]=df["title"].apply(categorize)
df = df[df["category"]!= "Other"]

df.to_csv("data/ai_news.csv", index=False)

logging.info("'Ai Related News Is Collected")