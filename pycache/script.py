import requests
import os
import time
from datetime import datetime   # 🟢 ADDED
from dotenv import load_dotenv
import snowflake.connector

# Delay between API pages
DELAY_SECONDS = 12
load_dotenv()

# Polygon API
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

# Snowflake connection parameters
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "********")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD", "*******")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "*******")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "SNOWFLAKE_LEARNING_WH")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "LEOPRIYAM")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN")

SNOWFLAKE_TABLE = "STOCK_TICKERS"
limit = 1000

def get_snowflake_connection():
    """Create and return a Snowflake connection"""
    return snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
        role=SNOWFLAKE_ROLE
    )

def create_tickers_table(conn):
    """Ensure the tickers table exists"""
    cursor = conn.cursor()
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {SNOWFLAKE_TABLE} (
        ticker VARCHAR,
        name VARCHAR,
        market VARCHAR,
        locale VARCHAR,
        primary_exchange VARCHAR,
        type VARCHAR,
        active BOOLEAN,
        currency_name VARCHAR,
        clk VARCHAR,
        composite_figi VARCHAR,
        share_class_figi VARCHAR,
        last_updated_utc TIMESTAMP,
        ds DATE    -- 🟢 ADDED new column
    );
    """
    cursor.execute(create_table_sql)
    print(f"✅ Table {SNOWFLAKE_TABLE} created or already exists")
    cursor.close()

def insert_tickers_to_snowflake(tickers):
    """Insert ticker data into Snowflake table"""
    conn = get_snowflake_connection()
    create_tickers_table(conn)
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM {SNOWFLAKE_TABLE}")  # Clear existing data
    print(f"🧹 Cleared existing data from {SNOWFLAKE_TABLE}")

    insert_sql = f"""
    INSERT INTO {SNOWFLAKE_TABLE} 
    (ticker, name, market, locale, primary_exchange, type, active, 
     currency_name, clk, composite_figi, share_class_figi, last_updated_utc, ds)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)   -- 🟢 ADDED ds placeholder
    """

    data_to_insert = []
    for t in tickers:
        row = (
            t.get('ticker', ''),
            t.get('name', ''),
            t.get('market', ''),
            t.get('locale', ''),
            t.get('primary_exchange', ''),
            t.get('type', ''),
            t.get('active', False),
            t.get('currency_name', ''),
            t.get('cik', ''),  # polygon uses "cik", but your table column is "clk"
            t.get('composite_figi', ''),
            t.get('share_class_figi', ''),
            t.get('last_updated_utc', ''),
            datetime.now().strftime('%Y-%m-%d')   # 🟢 ADDED ds value
        )
        data_to_insert.append(row)

    cursor.executemany(insert_sql, data_to_insert)
    conn.commit()
    print(f"✅ Successfully inserted {len(tickers)} tickers into {SNOWFLAKE_TABLE}")

    cursor.close()
    conn.close()

def run_stock_job():
    tickers = []
    url = f'https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={limit}&sort=ticker&apiKey={POLYGON_API_KEY}'

    while url:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code}")
            break

        data = response.json()
        tickers.extend(data.get('results', []))
        url = data.get('next_url')

        if url:
            url += f"&apiKey={POLYGON_API_KEY}"
            print(f"Requesting next page: {url}")
            time.sleep(DELAY_SECONDS)

    print(f"Total tickers fetched: {len(tickers)}")
    insert_tickers_to_snowflake(tickers)

if __name__ == "__main__":
    run_stock_job()
