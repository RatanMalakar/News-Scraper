
import os

print("Starting News Scraper Pipeline ")
print("Running Scrapers ........")

os.system(r"python scraper\techcrunch.py")

print("Running Scrapers ........")

os.system(r"python scraper\hackernews.py")

print("Combining Files.......")
os.system(r"python pipeline\combine_data.py")

print("CLeaning Data")
os.system(r"python pipeline\clean.py")

print("Filtering AI News ")
os.system(r"python pipeline\filter_data.py")

print("Pipeline finished")