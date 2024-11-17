from dagster import asset, DailyPartitionsDefinition, job, schedule
from resources import source_api_resource, target_db_resource
import pandas as pd
import httpx
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from datetime import timedelta

# Asset definition for the ETL process
@asset(
    partitions_def=DailyPartitionsDefinition(start_date="2023-01-01"),  # Partitioning by day
    required_resource_keys={"source_api", "target_db"},
)
def etl_process(context, date):
    source_api = context.resources.source_api
    target_db_url = context.resources.target_db

    # Convert date to datetime and calculate the next day
    start_date = pd.to_datetime(date)
    end_date = start_date + timedelta(days=1)

    # Fetch data from FastAPI for the date range (start to end)
    response = source_api.get(f"/data?start={start_date}&end={end_date}&variables=wind_speed&variables=power")
    data = response.json()["data"]

    # Convert data to DataFrame
    df = pd.DataFrame(data, columns=["timestamp", "wind_speed", "power"])

    # Convert the 'timestamp' column to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Set the timestamp as index
    df.set_index('timestamp', inplace=True)

    # Aggregate data in 10-minute intervals
    df_resampled = df.resample('10T').agg({
        'wind_speed': ['mean', 'min', 'max', 'std'],
        'power': ['mean', 'min', 'max', 'std']
    })

    # Flatten the MultiIndex columns
    df_resampled.columns = ['_'.join(col).strip() for col in df_resampled.columns.values]

    context.log.info(f"Length of resampled data: {len(df_resampled)}")
    
    # Prepare the connection to the database
    engine = create_engine(target_db_url)
    conn = engine.connect()

    try:
        # Ensure 'wind_speed' and 'power' signals exist in the 'signal' table
        aggregation_types = ['mean', 'min', 'max', 'std']
        signal_prefixes = ['wind_speed', 'power']
        signal_names = [f"{prefix}_{stat}" for prefix in signal_prefixes for stat in aggregation_types]
        for signal_name in signal_names:
            # Check if the signal already exists
            signal_query = text(f"SELECT id FROM signal WHERE name = :signal_name")
            result = conn.execute(signal_query, {"signal_name": signal_name}).fetchone()

            # If the signal doesn't exist, insert it
            if not result:
                context.log.info(f"Signal '{signal_name}' not found in database. Inserting...")
                conn.execute(text(f"INSERT INTO signal (name) VALUES (:signal_name)"), {"signal_name": signal_name})

        # Insert the aggregated data into the 'data' table
        for timestamp, row in df_resampled.iterrows():
            # Prepare a list of insert queries to minimize database calls
            insert_data = []
            for signal_name in signal_names:
                    signal_query = text(f"SELECT id FROM signal WHERE name = :signal_name")
                    signal_id = conn.execute(signal_query, {"signal_name": signal_name}).fetchone()[0]
                    value = float(row[f"{signal_name}"])  
                    insert_data.append({
                        "timestamp": timestamp, 
                        "signal_id": signal_id, 
                        "value": value
                    })

            # Perform the bulk insert in one go
            conn.execute(text("""
                INSERT INTO data (timestamp, signal_id, value)
                VALUES (:timestamp, :signal_id, :value)
            """), insert_data)
        conn.commit()
        context.log.info("Data successfully inserted into database")   
    except SQLAlchemyError as e:
        context.log.error(f"Error saving data to database: {e}")
    finally:
        conn.close()

# Job that uses the etl_process asset
@job(resource_defs={"source_api": source_api_resource, "target_db": target_db_resource})
def etl_job():
    etl_process()

# Schedule that runs the job daily at midnight
@schedule(cron_schedule="0 0 * * *", job=etl_job)
def daily_etl_schedule():
    return {}

