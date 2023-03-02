import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    database="Dashboard",
    host="localhost",
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    port="5432"
)

if __name__ == "__main__":
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(id) FROM entry")

    print(cursor.fetchone())
