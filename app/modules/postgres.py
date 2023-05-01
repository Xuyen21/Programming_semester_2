"""
Postgres Connector
Description: This module is responsible for the connection to the postgres database.
Created: 3.3.2023
"""
import os
import psycopg2

from dotenv import load_dotenv
load_dotenv()

# postgress connection
conn = psycopg2.connect(
database="Dashboard_V2",
host="localhost",
user=os.getenv('POSTGRES_USER'),
password=os.getenv('POSTGRES_PASSWORD'),
port="5432")

if __name__ == "__main__":
    cursor = conn.cursor()

    cursor.execute("SELECT count(name), name from title group by name")

    print(cursor.fetchone())
