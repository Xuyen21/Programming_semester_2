"""
Postgres Connector
Description: This module is responsible for the connection to the postgres database.
Created: 3.3.2023
"""
import os
import psycopg2
import environment

# from dotenv import load_dotenv
# load environments from .env file
# load_dotenv()

# postgress connection
# conn = psycopg2.connect(
#     database="Dashboard",
#     host="localhost",
#     user=os.getenv('POSTGRES_USER'),
#     password=os.getenv('POSTGRES_PASSWORD'),
#     port="5432"
# )


conn = psycopg2.connect(
    host=os.environ.get('DB_HOST'),
    port=os.environ.get('DB_PORT'),
    dbname=os.environ.get('DB_NAME'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD')
)

if __name__ == "__main__":
    cursor = conn.cursor()

    cursor.execute("SELECT count(name), name from title group by name")

    print(cursor.fetchone())
