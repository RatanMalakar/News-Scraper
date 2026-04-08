
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
# def get_connection():
#     return psycopg2.connect(
#         host=os.getenv("DB_HOST"),
#         database=os.getenv("DB_NAME"),
#         user=os.getenv("DB_USER"),
#         password=os.getenv("DB_PASSWORD"),
#         port=os.getenv("DB_PORT")
#     )

# def create_table(cursor):
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS techcrunch(
#             id SERIAL PRIMARY KEY,
#             title TEXT UNIQUE,
#             url TEXT
#         )
#     """)

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


    
# def insert_articles(cursor , articles):
#     logging.info("Clearing old data")
#     cursor.execute("TRUNCATE TABLE techcrunch RESTART IDENTITY")

#     logging.info("Inserting new data")
#     cursor.executemany(
#         "INSERT INTO techcrunch (title , url) VALUES (%s,%s) ON CONFLICT DO NOTHING",
#         articles
#     )

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

    # print("Fteched articles")
    # logging.info(f"Fetched {len(articles)} articles")

    # print("Connecting Database")
    # conn = get_connection()
    # cursor = conn.cursor()

    # try:
    #     print("Creating table")
    #     create_table(cursor)
    #     print("Inserting data")
    #     insert_articles(cursor , articles)
    #     conn.commit()
    #     print("Data inserted successfully")
    #     logging.info("Data inserted successfully")

    # except Exception :
    #     conn.rollback()
    #     print("Database error occured")
    #     logging.exception("Database error occured")

    # finally:
    #     cursor.close()
    #     conn.close()

if __name__ =="__main__":
    main()