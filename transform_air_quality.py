
import pandas as pd
import json
import os

# Read raw air quality data
with open("air_quality_raw.json", "r") as file:
    data = json.load(file)

# Convert into DataFrame
df = pd.DataFrame(data["hourly"])

# Convert time into datetime
df["time"] = pd.to_datetime(df["time"])

# Remove duplicate records
df = df.drop_duplicates()

# Sort records by time
df = df.sort_values(by="time")

# Check missing values
print("Missing Values:")
print(df.isnull().sum())

# Remove rows with missing values
df = df.dropna()

# Create data folder
os.makedirs("data", exist_ok=True)

# Save cleaned data
df.to_csv("data/air_quality_cleaned.csv", index=False)

print("\nAir Quality data cleaned successfully!")
print("\nFirst 5 Records:")
print(df.head())
