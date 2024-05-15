
import pandas as pd
from pydantic import BaseModel, ValidationError, validator
from datetime import datetime

# Definition of Pydantic models
class AirQualityData(BaseModel):
    aqi_value: int
    aqi_category: str
    co_aqi_value: int
    co_aqi_category: str
    ozone_aqi_value: int
    ozone_aqi_category: str
    no2_aqi_value: int
    no2_aqi_category: str
    pm25_aqi_value: int
    pm25_aqi_category: str
    
    @validator('aqi_value', 'co_aqi_value', 'ozone_aqi_value', 'no2_aqi_value', 'pm25_aqi_value', pre=True)
    def check_non_negative(cls, v):
        if v < 0:
            raise ValueError('AQI values must be non-negative')
        return v

class CityAirQuality(BaseModel):
    country: str
    city: str
    date_time: datetime
    air_quality_data: AirQualityData

# Load data from the new CSV file
df = pd.read_csv('air_quality_data.csv')

# Transform and create instances of Pydantic models
city_air_quality_instances = []

for _, row in df.iterrows():
    try:
        air_quality_data = {
            "aqi_value": row["AQI Value"],
            "aqi_category": row["AQI Category"],
            "co_aqi_value": row["CO AQI Value"],
            "co_aqi_category": row["CO AQI Category"],
            "ozone_aqi_value": row["Ozone AQI Value"],
            "ozone_aqi_category": row["Ozone AQI Category"],
            "no2_aqi_value": row["NO2 AQI Value"],
            "no2_aqi_category": row["NO2 AQI Category"],
            "pm25_aqi_value": row["PM2.5 AQI Value"],
            "pm25_aqi_category": row["PM2.5 AQI Category"]
        }
        
        city_air_quality = CityAirQuality(
            country=row["Country"],
            city=row["City"],
            date_time=pd.to_datetime(row["Date Time"]),
            air_quality_data=AirQualityData(**air_quality_data)
        )
        city_air_quality_instances.append(city_air_quality)
    except ValidationError as e:
        print(f"Error creating instance for {row['City']}: {e}")