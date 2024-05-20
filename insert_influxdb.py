import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "deusto-bucket"
org = "deusto-org"
token = "deusto2024-secret-token"

# Store the URL of your InfluxDB instance
url="http://localhost:8086"

client = InfluxDBClient(
   url=url,
   token=token,
   org=org
)

# Leer el archivo CSV con pandas
csv_file = 'air_quality_data.csv'
data = pd.read_csv(csv_file)
print(data.head())

write_api = client.write_api(write_options=SYNCHRONOUS)

# Iterar sobre las filas del DataFrame y escribir cada fila en InfluxDB
for index, row in data.iterrows():
    point = Point("air_quality") \
        .tag("country", row["Country"]) \
        .field("city", row["City"]) \
        .field("aqi_value", int(row["AQI Value"])) \
        .field("co_aqi_value", int(row["CO AQI Value"])) \
        .field("ozone_aqi_value", int(row["Ozone AQI Value"])) \
        .field("no2_aqi_value", int(row["NO2 AQI Value"])) \
        .field("pm25_aqi_value", int(row["PM2.5 AQI Value"])) \
        .field("aqi_category", row["AQI Category"]) \
        .field("co_aqi_category", row["CO AQI Category"]) \
        .field("ozone_aqi_category", row["Ozone AQI Category"]) \
        .field("no2_aqi_category", row["NO2 AQI Category"]) \
        .field("pm25_aqi_category", row["PM2.5 AQI Category"]) \
        .time(pd.to_datetime(row["Date Time"]), WritePrecision.NS)
    write_api.write(bucket=bucket, org=org, record=point)

# Cerrar el cliente
client.close()
