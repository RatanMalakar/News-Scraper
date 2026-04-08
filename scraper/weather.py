import requests
from bs4 import BeautifulSoup
import psycopg2


#connecting python to postgres

conn = psycopg2.connect(
    host="localhost",
    database="weather_db",
    user="postgres",
    password="ratan",
    port="5432"
)

cursor = conn.cursor()

#Creating Table

cursor.execute("""
CREATE TABLE IF NOT EXISTS weather (
               id SERIAL PRIMARY KEY,
               city TEXT,
               temperature TEXT
               )
               """)

url = "https://www.weather-india.in/"
    
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text,"html.parser")

cities = soup.find_all("div",class_="sib-container")

data = []

for city in cities :
    h2 = city.find("h2")

    if h2:
        full_text = h2.get_text(strip=True)
        city_name = full_text.replace("मौसम", "").strip()

        temp = h2.find("b").text.strip()

        if temp:
            data.append({
            "city": city_name,
            "temperature": temp
        })
            
# Inserting data 

for item in data :
    city = item["city"].replace(item["temperature"],"").strip()
    temp = item["temperature"]

    cursor.execute(
        "INSERT INTO weather (city , temperature) VALUES (%s,%s)",
        (city , temp)
    )

conn.commit()
cursor.close()
conn.close()
            
for item in data :
    city = item["city"]
    temp = item["temperature"]

    print(f"City: {city} | Temperature: {temp}")


