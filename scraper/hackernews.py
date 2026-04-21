from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import os 
import requests
import logging
import pandas as pd
from datetime import datetime



# Loading env variables

load_dotenv()

REQUIRED_VARS = ["DB_HOST","DB_NAME","DB_USER","DB_PASSWORD","DB_PORT"]
TARGER_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
OUTPUT_FILE = os.path.join("data", "hackernews.csv")
session = requests.Session()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app.log",
    filemode="a"
)

def validate_environment():
    for var in REQUIRED_VARS:
        if not os.getenv(var):
            raise ValueError(f"Missing environment variable: {var}")

def get_top_stories_ids(url):
    response = requests.get(url,timeout=5)
    return response.json()[:200]

def fetch_story(story_id):
    try:
        url=f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        response = session.get(url,timeout=5)

        if response.status_code == 200:
            data = response.json()

            if data and data.get("title"):
                return (
                    data.get("title").strip(),
                    data.get("url")
                )
    except requests.exceptions.RequestException:
        return None
    
def fetch_all_stories(story_ids):
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_story, story_ids))

    return [story for story in results if story]

def save_to_csv(stories):
    try:
        logging.info("Converting to dataframe")

        df = pd.DataFrame(stories , columns=["title" , "url"])
        df["scraped_at"] = pd.Timestamp.now()
        logging.info(f"Saving {len(df)} stories to csv")
        df.to_csv(OUTPUT_FILE ,index=False)
        print("Saved to csv")

    except Exception:
        logging.exception("Falied to save csv")


#main function

def main():
    logging.info("Pipeline started")
    print("Fetching data")
    logging.info("Fetching data...")

    story_ids = get_top_stories_ids(TARGER_URL)
    stories = fetch_all_stories(story_ids)

    print("Fetched stories")
    logging.info(f"Fetched {len(stories)} stories \n")

    save_to_csv(stories)


if __name__ == "__main__":
    main()