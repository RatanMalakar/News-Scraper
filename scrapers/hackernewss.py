
import requests
from concurrent.futures import ThreadPoolExecutor
import pandas as pd 


# Getting the json file of hacker news 

topstories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
top_ids = requests.get(topstories_url).json()

# Collecting 100 id's cause we have to apply filter , after that the numbers of the stories decreases

stories_id = top_ids[:100]


stories =[]

def fetch_stories(s_id):
    try:
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{s_id}.json"
        data = requests.get(item_url , timeout=5).json()    

        if data and data.get("title"):
            title = data.get("title")

            if "ai" in title.lower() or "artificial" in title.lower():
                return{
                    "title" : title ,
                    "url" : data.get("url")
                }
    except requests.exceptions.RequestException :
        return None

with ThreadPoolExecutor(max_workers=10)as executor:
    results = list(executor.map(fetch_stories , stories_id))

stories = [story for story in results if story]

print(f"Found {len(stories)} AI - related stories:")
#for s in stories:
#    print(s)

for s in stories:
    print(s["title"])
    print(s["url"])
    print("-"*50)

#    saving data to CSV

# converting list of dict to dataframe
df = pd.DataFrame(stories)

df.to_csv("hackernews_ai_stories.csv", index=False, encoding='utf-8')

print("Saved to CSV")
# for s_id in stories_id:
#    story = fetch_stories(s_id)
#    if story:
#        stories.append(story)



#  print(len(stories))
#   print(stories)
 #   item_url = f"https://hacker-news.firebaseio.com/v0/item/{s_id}.json"
  #  try:
   #     data = requests.get(item_url , timeout=5).json()
   # except requests.exceptions.RequestException :
    ##   continue
    



# Step 4: Filter out failed requests
# stories = [story for story in results if story]