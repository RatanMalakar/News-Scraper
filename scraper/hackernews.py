
import requests
from concurrent.futures import ThreadPoolExecutor
import pandas as pd 


topstories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
top_ids = requests.get(topstories_url).json()


stories_id = top_ids[:100]


stories =[]

def fetch_stories(s_id):
    try:
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{s_id}.json"
        data = requests.get(item_url , timeout=5).json()    

        if data and data.get("title"):
            title = data.get("title")
            return{
                    "title" : title ,
                    "url" : data.get("url")
                }
    except requests.exceptions.RequestException :
        return None

with ThreadPoolExecutor(max_workers=10)as executor:
    results = list(executor.map(fetch_stories , stories_id))

stories = [story for story in results if story]

print(f"Found {len(stories)} stories:")

for s in stories:
    print(s["title"])
    print(s["url"])
    print("-"*50)

df = pd.DataFrame(stories)

df.to_csv("data/hackernews_stories.csv", index=False, encoding='utf-8')

print("Saved to CSV")
