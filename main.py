
import os

print("Starting News Scraper Pipeline ")
print("Running Scrapers ........")

os.system(r"python scraper\techcrunch.py")

print("Running Scrapers ........")

os.system(r"python scraper\hackernews.py")

print("Collecting AI News.......")
os.system(r"python pipeline\pipeline.py")

print("Pipeline finished")