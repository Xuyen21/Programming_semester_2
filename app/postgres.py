import psycopg2

conn = psycopg2.connect(
    database="Dashboard",
    host="localhost",
    user="postgres",
    password="festo",
    port="5432"
)

if __name__ == "__main__":
    cursor = conn.cursor()

    cursor.execute("SELECT title, author FROM view_article")

    print(cursor.fetchone())
