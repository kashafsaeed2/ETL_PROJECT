
import pandas as pd
import sqlite3
import os

# Read validated datasets
weather_df = pd.read_csv("data/weather_validated.csv")
air_df = pd.read_csv("data/air_quality_validated.csv")

# Create database folder
os.makedirs("database", exist_ok=True)

# Connect to database
connection = sqlite3.connect("database/weather.db")

# Save weather data
weather_df.to_sql(
    "weather_records",
    connection,
    if_exists="replace",
    index=False
)

# Save air quality data
air_df.to_sql(
    "air_quality_records",
    connection,
    if_exists="replace",
    index=False
)

# Check records
cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM weather_records")
print("Weather records:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM air_quality_records")
print("Air quality records:", cursor.fetchone()[0])

print("Both datasets saved successfully!")

connection.close()
