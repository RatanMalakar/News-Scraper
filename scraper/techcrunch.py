
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


url = "https://techcrunch.com/category/artificial-intelligence/"

r = requests.get(url)
html_content = r.text

soup = BeautifulSoup(html_content , 'html.parser')

ai_articles = []

posts = soup.find_all("a")

for p in posts:
    title=p.text.strip()
    url=p.get("href")

    if not url :
        continue

    if re.search(r"techcrunch.com/\d{4}/\d{2}/\d{2}", url):
            ai_articles.append({'title':title , 'url':url})
            
    for a in ai_articles:
        print(a["title"])
        print(a["url"])
        print("-"*50)

df = pd.DataFrame(ai_articles)
df.to_csv("data/techcrunch_news.csv" , index=False)

print("Saved to CSV")