
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Read weather data
df = pd.read_csv("data/weather_validated.csv")

# Convert time into datetime
df["time"] = pd.to_datetime(df["time"])

# Create charts folder
os.makedirs("charts", exist_ok=True)

# Display basic statistics
print("WEATHER DATA ANALYSIS")
print(df.describe())

# 1. Temperature Graph
plt.figure(figsize=(10, 5))
plt.plot(df["time"], df["temperature_2m"])
plt.title("Lahore Temperature Analysis")
plt.xlabel("Date and Time")
plt.ylabel("Temperature (Celsius)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/temperature.png")
plt.show()

# 2. Humidity Graph
plt.figure(figsize=(10, 5))
plt.plot(df["time"], df["relative_humidity_2m"])
plt.title("Lahore Humidity Analysis")
plt.xlabel("Date and Time")
plt.ylabel("Humidity (%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/humidity.png")
plt.show()

# 3. Wind Speed Graph
plt.figure(figsize=(10, 5))
plt.plot(df["time"], df["wind_speed_10m"])
plt.title("Lahore Wind Speed Analysis")
plt.xlabel("Date and Time")
plt.ylabel("Wind Speed (km/h)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/wind_speed.png")
plt.show()

# 4. Precipitation Graph
plt.figure(figsize=(10, 5))
plt.plot(df["time"], df["precipitation"])
plt.title("Lahore Precipitation Analysis")
plt.xlabel("Date and Time")
plt.ylabel("Precipitation (mm)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/precipitation.png")
plt.show()

# Correlation Heatmap
plt.figure(figsize=(8, 5))
sns.heatmap(
    df.select_dtypes(include="number").corr(),
    annot=True,
    cmap="coolwarm"
)
plt.title("Weather Data Correlation")
plt.tight_layout()
plt.savefig("charts/correlation.png")
plt.show()

print("EDA completed successfully!")
print("All graphs saved in charts folder.")
