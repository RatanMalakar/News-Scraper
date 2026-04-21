
from dotenv import load_dotenv
# import psycopg2
import logging
import os
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd



load_dotenv()

REQUIRED_VARS = ["DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD", "DB_PORT"]
TARGET_URL = "https://techcrunch.com/category/artificial-intelligence/"
OUTPUT_FILE = os.path.join("data" , "techcrunch.csv")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s -%(levelname)s -%(message)s",
    filename="app.log",
    filemode="a"
)

def validate_env():
    for var in REQUIRED_VARS:
        if not os.getenv(var):
            raise ValueError(f"Missing env var:{var}")
    logging.info("Environment variables validate")

def fetch_html(url):
    try:
        print("Fetching webpage")
        logging.info("Fetching Webpage")
        response = requests.get(url,timeout=5)
        response.raise_for_status()
        return response.text
    
    except requests.exceptions.RequestException as e:
        print("Failed to fetch webpage")
        logging.exception(f"Failed to fetch web page: {e}")
        return None

def parse_articles(html):
    soup = BeautifulSoup(html , "html.parser")
    posts = soup.find_all("a")

    articles = []

    for post in posts :
        title = post.text.strip()
        url = post.get("href")

        if not url or not title:
            continue

        if re.search(r"techcrunch.com/\d{4}/\d{2}/\d{2}",url):
            articles.append((title,url))

    print("Extracted articles")
    logging.info(f"Extracted {len(articles)} articles")
    
    return articles

def save_to_csv(articles):
    try:
        logging.info("Converting into data frame")

        df = pd.DataFrame(articles , columns=["title" , "url"])
        df["scraped_at"] = pd.Timestamp.now()

        logging.info(f"Saving {len(df)} articles to CSV")
        df.to_csv(OUTPUT_FILE,index=False)
        print("Saved to OUTPUT_FILE")

    except Exception:
        logging.exception("Failed to save csv")


def main():
    logging.info("Pipeline satarted...")

    print("Fetching html")
    logging.info("Fetching html")

    html = fetch_html(TARGET_URL)
    articles = parse_articles(html)

    if not html:
        logging.error("No HTML fetched . Exiting...")
        return
    
    if not articles :
        logging.warning("No articles found")
        return

    print("Fetched articles")
    logging.info(f"Fetched {len(articles)}articles")

    save_to_csv(articles)

if __name__ =="__main__":
    main()