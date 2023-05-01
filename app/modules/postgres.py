"""
Postgres Connector
Description: This module is resposible for the connection to the postgres database.
Created: 3.3.2023
"""
import os
from time import time
from psycopg2 import connect, sql, errors
from dotenv import load_dotenv
import logging

# load environments from .env file
load_dotenv()

# postgress connection
conn = connect(
    database = os.getenv('DATABASE_NAME'),
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

    sub_query = sql.SQL("""
        SELECT {table_id}, COUNT({table_id}) as count 
        FROM {entry_table} 
        GROUP BY {table_id} 
        ORDER BY {order_by} {order} 
        LIMIT {limit}
        """).format(
        entry_table = sql.Identifier(f'entry_{table}'),
        table_id = sql.Identifier(f'{table}_id'),
        order_by = sql.SQL(order_by),
        order = sql.SQL("ASC" if order else "DESC"),
        limit = sql.Literal(str(limit))
    )

    # generate sql query
    sql_query = sql.SQL("""
        SELECT {select} 
        FROM ({sub}) as sub_col 
        LEFT JOIN {table} ON {on}
        """).format(
        select = sql.SQL(",").join(map(sql.SQL, select)),
        sub = sub_query,
        table = sql.Identifier(table),
        on = sql.SQL(f'sub_col.{table}_id = {table}.id')
    )

    # execute query
    try:
        t1 = time()
        cursor.execute(sql_query)
        t2 = time()
        logging.debug(f'Query took: {t2 - t1:.3} seconds')
    except errors.SyntaxError as err:
        logging.warning(err)
    except Exception as err:
        logging.error(err)

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

def author_relations() -> list[tuple]:

    sub_query = sql.SQL("""
    (
        SELECT phdthesis.entry_key
        FROM phdthesis
        LEFT JOIN entry_author ON phdthesis.entry_key = entry_author.entry_key
        GROUP BY phdthesis.entry_key
        ORDER BY COUNT(entry_author.author_id) DESC
        LIMIT 10
    ) as sub_col"""
    )

    # generate sql query
    sql_query = sql.SQL("""
        SELECT sub_col.entry_key, author.name
        FROM {sub_query}
        LEFT JOIN entry_author ON sub_col.entry_key = entry_author.entry_key
        LEFT JOIN author ON entry_author.author_id = author.id;"""
    ).format(
        sub_query = sub_query
    )

    # execute query
    try:
        t1 = time()
        cursor.execute(sql_query)
        t2 = time()
        logging.debug(f'Query took: {t2 - t1:.3} seconds')
    except errors.SyntaxError as err:
        logging.warning(err)
    except Exception as err:
        logging.error(err)

    # return results
    return cursor.fetchall()

def papers_per_week(year: str) -> list[tuple]:
    sub_query = sql.SQL("""
    (
        SELECT key, mdate, DATE_PART('week',mdate) as week_number
        FROM entry
        WHERE EXTRACT(YEAR FROM mdate) = {year}
        ORDER BY week_number DESC 
    ) AS sub_col
    """).format(
        year = sql.Literal(year)
    )

    # generate sql query
    sql_query = sql.SQL("""
        SELECT week_number, COUNT(key)
        FROM {sub_query}
        GROUP BY week_number
        ORDER BY week_number"""
    ).format(
        sub_query = sub_query
    )

    # execute query
    try:
        t1 = time()
        cursor.execute(sql_query)
        t2 = time()
        logging.debug(f'Query took: {t2 - t1:.3} seconds')
    except errors.SyntaxError as err:
        logging.warning(err)
    except Exception as err:
        logging.error(err)

    # return results
    return cursor.fetchall()
