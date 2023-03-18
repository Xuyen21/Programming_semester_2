"""
Postgres Connector
Description: This module is resposible for the connection to the postgres database.
Created: 3.3.2023
"""
import os
from time import time
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

    # check types
    if not isinstance(select, (list, str)):
        raise TypeError("select must be of type: list[str]")

    if not isinstance(table, str):
        raise TypeError("table must be of type: str")

    if not isinstance(group_by, str):
        raise TypeError("group_by must be of type: str")

    if not isinstance(order_by, str):
        raise TypeError("order_by must be of type: str")

    if not isinstance(order, bool):
        raise TypeError("order must be of type: bool")

    if not isinstance(limit, int):
        raise TypeError("limit must be of type: int")

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

def table_column_names(table: str) -> list[tuple]:
    """
    This function gets the column names of the specified table.

    Parameters:
    - table: str => the table to get the columns from

    Return:
    - list[tuples] => the result of the query as list of tuples
    """
    # check type
    if not isinstance(table, str):
        raise TypeError("Table is not a str")

    # generate sql query
    sql_query = sql.SQL('SELECT "table_name", "column_name" FROM information_schema."columns" WHERE "table_schema" = {schema} AND "table_name" = {table};').format(
        schema = sql.Literal('public'),
        table = sql.Literal(table)
    )

    # execute query
    cursor.execute(sql_query)

    # return results
    return cursor.fetchall()

if __name__ == "__main__":
    # simulate expected dashboard input

    # test sql_from_dropdown
    t1 = time()
    grouped = sql_from_dropdown(["name", "COUNT(id)"], "author", "name", "COUNT(id)")
    t2 = time()

    for value in grouped:
        print(value)

    print(f'Query took: {t2 - t1:.3} seconds')

    print("-" * 50)

    # test table_column_names
    t1 = time()
    columns = table_column_names("entry")
    t2 = time()

    for value in columns:
        print(value)

    print(f'Query took: {t2 - t1:.3} seconds')
