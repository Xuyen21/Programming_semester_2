"""
Postgres Connector
Description: This module is resposible for the connection to the postgres database.
Created: 3.3.2023
Changelog:
- 10.03.2023: Added sqlFromDropdown function
"""
import os
from psycopg2 import connect, sql
from dotenv import load_dotenv

# load environments from .env file
load_dotenv()

# postgress connection
conn = connect(
    database = "Dashboard",
    host = "localhost",
    user = os.getenv('POSTGRES_USER'),
    password = os.getenv('POSTGRES_PASSWORD'),
    port="5432"
)

# initialize database cursor
cursor = conn.cursor()

def sql_from_dropdown(select: list[str], table: str, group_by: str, order_by: str, order: bool = False, limit: int = 10) -> list[tuple]:
    """
    This function gets the parameters provided by the dashboard, converts it to a sql query
    and returns the result as a list of tuples.

    Parameters:
    - select: list[str] => the columns to be selected
    - table: str => the table to select from
    - group_by: str => the column to group by
    - order_by: str => the column to order by
    - order: bool = False => ASC or DESC order (True = ASC)
    - limit: int = 10 => Row limitation

    Return:
    - list[tuples] => the result of the query as list of tuples
    """
    # generate sql query
    sql_query = sql.SQL('SELECT {select} FROM {table} GROUP BY {group_by} ORDER BY {order_by} {order} LIMIT {limit}').format(
        select = sql.SQL(",").join(map(sql.SQL, select)),
        table = sql.Identifier(table),
        group_by = sql.Identifier(group_by),
        order_by = sql.SQL(order_by),
        order = sql.SQL("ASC" if order else "DESC"),
        limit = sql.Literal(str(limit))
    )

    # execute query
    cursor.execute(sql_query)

    # return results
    return cursor.fetchall()

if __name__ == "__main__":
    # expected Dashboard input
    retData = sqlFromDropdown(["name", "COUNT(id)"], "author", "name", "COUNT(id)")

    for value in retData:
        print(value)
