from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from utils import *

default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
}

@dag(
    dag_id='weather_etl_dag',
    schedule='@hourly',
    start_date=datetime(2025, 7, 25),
    catchup=False,
    default_args=default_args,
    tags=['weather-etl']
)
def weather_etl_pipeline():

    @task()
    def create_table():
        hook = PostgresHook(postgres_conn_id='weather_postgres')
        hook.run(get_create_table_query())

    @task()
    def extract_weather():
        return fetch_api()

    @task()
    def insert_into_table(data: dict):
        hook = PostgresHook(postgres_conn_id='weather_postgres')
        conn = hook.get_conn()
        cursor = conn.cursor()
        
        loc = data['location']
        curr = data['current']
        astro = curr['astro']
        air = curr['air_quality']
        
        cursor.execute(
            get_insert_query(),
            (
                loc['name'], loc['country'], loc['region'],
                curr['observation_time'], curr['temperature'], curr['weather_descriptions'][0],
                astro['sunrise'], astro['sunset'], astro['moonrise'], astro['moonset'],
                air['co'], air['no2'], air['o3'], air['so2'], air['pm2_5'], air['pm10'],
                air['us-epa-index'], air['gb-defra-index'],
                curr['precip'], curr['humidity'], curr['uv_index'], curr['visibility']
            )
        )
        conn.commit()

    @task()
    def create_views():
        hook = PostgresHook(postgres_conn_id='weather_postgres')
        hook.run(get_latest_view_query())
        hook.run(get_daily_view_query())

    # DAG structure
    create_table_task = create_table()
    weather_data = extract_weather()
    insert_task = insert_into_table(weather_data)
    create_views_task = create_views()

    create_table_task >> weather_data >> insert_task >> create_views_task

weather_etl_pipeline()
