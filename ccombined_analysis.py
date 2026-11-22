
import pandas as pd
import os
import sqlite3

# Load both datasets
weather_df = pd.read_csv("data/weather_validated.csv")
air_df = pd.read_csv("data/air_quality_validated.csv")

# Merge datasets using time
combined_df = pd.merge(
    weather_df,
    air_df,
    on="time",
    how="inner"
)

# Create data folder if needed
os.makedirs("data", exist_ok=True)

# Save combined data
combined_df.to_csv("data/combined_data.csv", index=False)

# Save combined data in SQLite
connection = sqlite3.connect("database/weather.db")

combined_df.to_sql(
    "combined_weather_air_quality",
    connection,
    if_exists="replace",
    index=False
)

connection.close()

print("Weather and Air Quality data merged successfully!")
print("Total combined records:", len(combined_df))
print("\nFirst 5 records:")
print(combined_df.head())
print("\nCombined data saved in data/combined_data.csv")
