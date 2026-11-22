
import pandas as pd
from pydantic import BaseModel, ValidationError
from datetime import datetime

# Define data structure
class WeatherRecord(BaseModel):
    time: datetime
    temperature_2m: float
    relative_humidity_2m: float
    precipitation: float
    wind_speed_10m: float


# Read cleaned CSV file
df = pd.read_csv("data/weather_cleaned.csv")

valid_records = []

# Validate each record
for record in df.to_dict(orient="records"):
    try:
        weather = WeatherRecord(**record)
        valid_records.append(weather.model_dump())

    except ValidationError as error:
        print("Invalid record:", error)

# Save validated data
validated_df = pd.DataFrame(valid_records)
validated_df.to_csv("data/weather_validated.csv", index=False)

print("Data validation completed!")
print("Total records:", len(df))
print("Valid records:", len(validated_df))
print("Invalid records:", len(df) - len(validated_df))
