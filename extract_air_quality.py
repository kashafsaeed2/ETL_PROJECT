
import requests
import json

url = "https://air-quality-api.open-meteo.com/v1/air-quality"

params = {
    "latitude": 31.5204,
    "longitude": 74.3587,
    "hourly": [
        "pm10",
        "pm2_5",
        "carbon_monoxide",
        "nitrogen_dioxide",
        "sulphur_dioxide",
        "ozone"
    ],
    "past_days": 7,
    "forecast_days": 1,
    "timezone": "Asia/Karachi"
}

response = requests.get(url, params=params)

if response.status_code == 200:

    data = response.json()

    with open("air_quality_raw.json", "w") as file:
        json.dump(data, file, indent=4)

    print("Air Quality data fetched successfully!")
    print("Data saved in air_quality_raw.json")

else:
    print("Error:", response.status_code)
