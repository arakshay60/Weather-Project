from datetime import datetime
import logging
import random
from datetime import datetime, timedelta
import requests
import os

def fetch_api():
    api_key=os.getenv("API_KEY")
    url=f"https://api.weatherstack.com/current?access_key={api_key}&query=Bangalore"
    try:
        response=requests.get(url)
        response.raise_for_status()
        print("API call successful")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occured: {e}")
        raise

def get_create_table_query():
    return """
    CREATE SCHEMA IF NOT EXISTS dev;
    CREATE TABLE IF NOT EXISTS dev.ods_weather (
        location_name TEXT,
        location_country TEXT,
        location_region TEXT,
        observation_time TEXT,
        temperature INT,
        weather_description TEXT,
        sunrise TIME,
        sunset TIME,
        moonrise TIME,
        moonset TIME,
        air_quality_co DOUBLE PRECISION,
        air_quality_no2 DOUBLE PRECISION,
        air_quality_o3 DOUBLE PRECISION,
        air_quality_so2 DOUBLE PRECISION,
        air_quality_pm2_5 DOUBLE PRECISION,
        air_quality_pm10 DOUBLE PRECISION,
        air_quality_us_epa_index INT,
        air_quality_gb_defra_index INT,
        precip DOUBLE PRECISION,
        humidity INT,
        uv_index INT,
        visibility INT,
        inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """


def get_insert_query():
    return """
    INSERT INTO dev.ods_weather (
        location_name, location_country, location_region, observation_time, temperature, weather_description,
        sunrise, sunset, moonrise, moonset,
        air_quality_co, air_quality_no2, air_quality_o3, air_quality_so2, air_quality_pm2_5, air_quality_pm10,
        air_quality_us_epa_index, air_quality_gb_defra_index,
        precip, humidity, uv_index, visibility, inserted_at
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW());
    """


def get_latest_view_query():
    return """
    CREATE OR REPLACE VIEW dev.v_latest_weather AS
    SELECT 
        location_name, location_country, location_region, observation_time, temperature, weather_description,
        sunrise, sunset, moonrise, moonset,
        air_quality_co, air_quality_no2, air_quality_o3, air_quality_so2, air_quality_pm2_5, air_quality_pm10,
        air_quality_us_epa_index, air_quality_gb_defra_index,
        precip, humidity, uv_index, visibility, inserted_at
    FROM (
        SELECT *, ROW_NUMBER() OVER (ORDER BY inserted_at DESC) AS rn
        FROM dev.ods_weather
    ) AS A
    WHERE rn = 1;
    """


def get_daily_view_query():
    return """
    CREATE OR REPLACE VIEW dev.v_daily_temperature_summary AS
    SELECT
        DATE(inserted_at) AS date,
        location_name,
        location_country,
        location_region,
        MAX(temperature) AS max_temperature,
        MIN(temperature) AS min_temperature
    FROM dev.ods_weather
    GROUP BY DATE(inserted_at), location_name, location_country, location_region;
    """
