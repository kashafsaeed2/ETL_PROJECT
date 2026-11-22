
import pandas as pd
import json
import os

# Read raw JSON data
with open("weather_raw.json", "r") as file:
    data = json.load(file)

# Convert into DataFrame
df = pd.DataFrame(data["hourly"])

# Convert time into datetime
df["time"] = pd.to_datetime(df["time"])

# Remove duplicate records
df = df.drop_duplicates()

# Sort records
df = df.sort_values(by="time")

# Check missing values
print("Missing Values:")
print(df.isnull().sum())

# Remove missing values
df = df.dropna()

# Create data folder
os.makedirs("data", exist_ok=True)

# Save cleaned data
df.to_csv("data/weather_cleaned.csv", index=False)

print("\nData cleaned successfully!")
print(df.head())
