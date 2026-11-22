
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load combined dataset
df = pd.read_csv("data/combined_data.csv")

# Convert time into datetime
df["time"] = pd.to_datetime(df["time"])

# Create charts folder
os.makedirs("charts", exist_ok=True)

# Graph 1: Temperature vs PM2.5
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="temperature_2m", y="pm2_5")
plt.title("Temperature vs PM2.5")
plt.xlabel("Temperature (°C)")
plt.ylabel("PM2.5")
plt.savefig("charts/temperature_pm25.png")
plt.show()

# Graph 2: Humidity vs PM2.5
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="relative_humidity_2m", y="pm2_5")
plt.title("Humidity vs PM2.5")
plt.xlabel("Humidity (%)")
plt.ylabel("PM2.5")
plt.savefig("charts/humidity_pm25.png")
plt.show()

# Graph 3: Weather and Air Quality Correlation
plt.figure(figsize=(10, 7))
correlation = df.select_dtypes(include="number").corr()
sns.heatmap(correlation, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Weather and Air Quality Correlation")
plt.savefig("charts/combined_correlation.png")
plt.show()

print("Combined EDA completed successfully!")
print("All combined graphs saved in charts folder.")
