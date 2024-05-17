from datetime import datetime, timedelta, timezone
from typing import List
from fastapi import FastAPI, HTTPException, Path, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from models import AirQualityData, CityAirQuality, city_air_quality_instances
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from concurrent.futures import ThreadPoolExecutor, as_completed

# InfluxDB Configuration
url = 'http://influxdb:8086'
token = 'AVniTEq3wnjzSyDT4ehfYKu-u52PMDLp86HLScgp9dNcgMkifnoe_ueoX3vJmLOKXGmZYhrLTIxh2roekdb9DA=='
org = 'my-org'
bucket = 'my-bucket'

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Security schema and JWT configuration
SECRET_KEY = "your_super_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

# List to store received air quality data
received_data: List[CityAirQuality] = []

# Function to decode JWT
def decode_jwt(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Convert timestamp to datetime for comparison
        exp_timestamp = decoded_token.get("exp")
        if exp_timestamp:
            exp = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)

            if exp >= datetime.now(timezone.utc):
                return decoded_token
            else:
                return None
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token") from e

# Function to create an access token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency to get the current user from the token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_jwt(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    return {"username": username}

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Implement authentication logic as per your needs
    user_username = form_data.username
    user_password = form_data.password
    if user_username != "admin" or user_password != "secret":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/load_csv_data/", response_model=List[CityAirQuality])
async def load_csv_data():
    if not city_air_quality_instances:
        raise HTTPException(status_code=404, detail="No data loaded from CSV")
    
    def write_point(data):
        point = Point("air_quality") \
            .field("city", data.city) \
            .field("country", data.country) \
            .field("aqi_value", data.air_quality_data.aqi_value) \
            .field("co_aqi_value", data.air_quality_data.co_aqi_value) \
            .field("ozone_aqi_value", data.air_quality_data.ozone_aqi_value) \
            .field("no2_aqi_value", data.air_quality_data.no2_aqi_value) \
            .field("pm25_aqi_value", data.air_quality_data.pm25_aqi_value) \
            .field("aqi_category", data.air_quality_data.aqi_category) \
            .field("co_aqi_category", data.air_quality_data.co_aqi_category) \
            .field("ozone_aqi_category", data.air_quality_data.ozone_aqi_category) \
            .field("no2_aqi_category", data.air_quality_data.no2_aqi_category) \
            .field("pm25_aqi_category", data.air_quality_data.pm25_aqi_category) \
            .time(data.date_time, WritePrecision.NS)
        write_api.write(bucket=bucket, org=org, record=point)

    # Usar ThreadPoolExecutor para escribir los datos en paralelo
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(write_point, data) for data in city_air_quality_instances]
        for future in as_completed(futures):
            future.result()  # Esperamos a que cada tarea se complete para manejar excepciones si ocurren

    return city_air_quality_instances


@app.get("/received_air_quality_data/", response_model=List[CityAirQuality])
async def get_all_air_quality_data(current_user: dict = Depends(get_current_user)):
    return city_air_quality_instances