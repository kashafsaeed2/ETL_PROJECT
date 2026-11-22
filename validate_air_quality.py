
import pandas as pd
from pydantic import BaseModel, ValidationError
from datetime import datetime

class AirQualityRecord(BaseModel):
    time: datetime
    pm10: float
    pm2_5: float
    carbon_monoxide: float
    nitrogen_dioxide: float
    sulphur_dioxide: float
    ozone: float

# Read cleaned data
df = pd.read_csv("data/air_quality_cleaned.csv")

valid_records = []

# Validate each record
for record in df.to_dict(orient="records"):
    try:
        air_quality = AirQualityRecord(**record)
        valid_records.append(air_quality.model_dump())

    except ValidationError as error:
        print("Invalid record:", error)

# Save validated data
validated_df = pd.DataFrame(valid_records)

validated_df.to_csv(
    "data/air_quality_validated.csv",
    index=False
)

print("Air Quality validation completed!")
print("Total records:", len(df))
print("Valid records:", len(validated_df))
print("Invalid records:", len(df) - len(validated_df))
