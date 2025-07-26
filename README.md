# 🌦️ Weather Data ETL Pipeline with Apache Airflow, Docker & PostgreSQL

This project is a **production-ready data pipeline** that extracts live weather data of Bangalore from the [WeatherStack API](https://weatherstack.com/), transforms it, and loads it into a PostgreSQL database using **Apache Airflow** orchestrated within **Docker containers**. It includes staging tables, automated DAGs, and materialized views for current and daily weather summaries.

---

## 🔧 Tech Stack

- **Apache Airflow 3.0 (TaskFlow API)**
- **PostgreSQL 14**
- **Docker & Docker Compose**
- **Python 3.12**
- **WeatherStack API**
- **SQL (DDL & DML for fact/views)**

---

## 📌 Project Features

✅ Modular and production-friendly project structure  
✅ Environment variable-based API key loading using `.env`  
✅ **ETL Pipeline** built using Airflow TaskFlow API  
✅ Automatically creates schema and table on first run  
✅ Inserts real-time weather + air quality data into a fact table  
✅ Creates 2 analytical views:
  - `v_latest_weather` – Shows the most recent weather reading
  - `v_daily_temperature_summary` – Aggregates daily temperature stats  
✅ Built for easy **Dockerized deployment**  
✅ Reusable `utils.py` for SQL queries and API logic

---

## 🔐 .env Configuration

Create a `.env` file in the root folder:

```env
API_KEY=your_weatherstack_api_key
```

Make sure your `.env` file is included in your `.gitignore`.

---

## 🐳 How to Run the Project

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/arakshay60/weather-project.git
cd weather-project
```

### 2️⃣ Set up Environment Variable

Create a `.env` file with your WeatherStack API key as shown above.

### 3️⃣ Start Docker Containers

```bash
docker-compose up --build
```

This will set up:

- Airflow Webserver: [http://localhost:8000](http://localhost:8000)  
- Postgres Database: exposed on port `5432`  
- Airflow Scheduler, Worker, Triggerer

Login with:

- **Username**: `airflow`  
- **Password**: `airflow`

### 4️⃣ Trigger the DAG

Once Airflow is running:

1. Go to the UI: [http://localhost:8000](http://localhost:8000)
2. Turn **ON** the DAG named `weather_etl_pipeline`
3. Trigger the DAG manually or wait for its schedule

<img width="1912" height="864" alt="image" src="https://github.com/user-attachments/assets/fa068494-f15e-4d0c-a22f-23aa31deba37" />


## 🧹 SQL Views for Analytics

### 🔍 `dev.v_latest_weather`

Shows the latest weather observation based on timestamp.

### 📊 `dev.v_daily_temperature_summary`

Groups by date + location and shows min/max temperature for the day.

## 🏁 Next Steps & Add-Ons

- Add Power BI / Metabase dashboard from the PostgreSQL views
- Schedule hourly or daily DAG triggers
- Extend pipeline to multiple cities (parameterize API)

---

## 📜 License

MIT License - free to use, fork, and contribute!

