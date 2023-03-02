import psycopg2

conn = psycopg2.connect(
    database="Dashboard",
    host="localhost",
    user="",
    password="",
    port="5432"
)

if __name__ == "__main__":
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(id) FROM entry")

    print(cursor.fetchone())
