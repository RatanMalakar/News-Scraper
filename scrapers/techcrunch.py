
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

# Getting html of the website 

url = "https://techcrunch.com/category/artificial-intelligence/"

r = requests.get(url)
html_content = r.text

# Parsing the html content

soup = BeautifulSoup(html_content , 'html.parser')


# Finding articles usually inside <a> tag with titles

ai_articles = []

posts = soup.find_all("a")

# Filtering AI news 

for p in posts:
    title=p.text.strip()
    url=p.get("href")

    if not url :
        continue

  #  if link and "techcrunch.com" in link :
   #     if "ai" in title.lower() or "artificial" in title.lower():
    #        print(title , link)


    if re.search(r"techcrunch.com/\d{4}/\d{2}/\d{2}", url):
        if "ai" in title.lower() or "artificial" in title.lower():

            # Save file to the list - ai_articles 
            ai_articles.append({'title':title , 'url':url})
            
            for a in ai_articles:
             print(a["title"])
             print(a["url"])
             print("-"*50)



# Saving data to CSV

df = pd.DataFrame(ai_articles)
df.to_csv("techcrunch_ai_news.csv" , index=False)

print("Saved to CSV")