
import requests
import json

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 31.5204,
    "longitude": 74.3587,
    "hourly": [
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "wind_speed_10m"
    ],
    "past_days": 7,
    "forecast_days": 1,
    "timezone": "Asia/Karachi"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()

    with open("weather_raw.json", "w") as file:
        json.dump(data, file, indent=4)

    print("Weather data fetched successfully!")
    print("Data saved in weather_raw.json")

else:
    print("Error:", response.status_code)
