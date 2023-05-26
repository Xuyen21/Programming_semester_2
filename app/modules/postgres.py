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

def execute_query(query, name: str) -> list[tuple]:
    # execute query
    try:
        t1 = time()
        cursor.execute(query)
        t2 = time()
        logging.debug(f'{name} query took: {t2 - t1:.3} seconds')
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

def author_relations(table: str, limit: int) -> list[tuple]:

    sub_query = sql.SQL("""
    (
        SELECT {select}
        FROM {table}
        LEFT JOIN entry_author ON {on} = entry_author.entry_key
        GROUP BY {group_by}
        ORDER BY COUNT(entry_author.author_id) DESC
        LIMIT {limit}
    ) as sub_col"""
    ).format(
        select = sql.SQL(f'{table}.entry_key'),
        table = sql.Identifier(table),
        group_by = sql.SQL(f'{table}.entry_key'),
        on = sql.SQL(f'{table}.entry_key'),
        limit = sql.Literal(limit)
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
        logging.debug(f'author_relations query took: {t2 - t1:.3} seconds')
    except errors.SyntaxError as err:
        logging.warning(err)
    except Exception as err:
        logging.error(err)

    # return results
    return cursor.fetchall()

def school_relations(table: str, limit: int) -> list[tuple]:

    sub_query = sql.SQL("""
    (
        SELECT {select}
        FROM {table}
        LEFT JOIN entry_school ON {on} = entry_school.entry_key
        GROUP BY {group_by}
        ORDER BY COUNT(entry_school.school_id) DESC
        LIMIT {limit}
    ) as sub_col"""
    ).format(
        select = sql.SQL(f'{table}.entry_key'),
        table = sql.Identifier(table),
        group_by = sql.SQL(f'{table}.entry_key'),
        on = sql.SQL(f'{table}.entry_key'),
        limit = sql.Literal(limit)
    )

    # generate sql query
    sql_query = sql.SQL("""
        SELECT sub_col.entry_key, school.name
        FROM {sub_query}
        LEFT JOIN entry_school ON sub_col.entry_key = entry_school.entry_key
        LEFT JOIN school ON entry_school.school_id = school.id;"""
    ).format(
        sub_query = sub_query
    )

    # execute query
    try:
        t1 = time()
        cursor.execute(sql_query)
        t2 = time()
        logging.debug(f'school_relations query took: {t2 - t1:.3} seconds')
    except errors.SyntaxError as err:
        logging.warning(err)
    except Exception as err:
        logging.error(err)

    # return results
    return cursor.fetchall()

def paper_date_title(key: str) -> list[tuple]:
    """
    This function gets the date and title of the paper with the given key.
    Parameters:
    - key: str => the paper key
    Return:
    - list[tuples] => the result of the query as list of tuples
    """
    # generate author sql query
    sql_query = sql.SQL("""
        SELECT sub_col."mdate", title."name"
        FROM (
            SELECT "key", mdate
            FROM entry
            WHERE "key" = {key}
        ) AS sub_col
        LEFT JOIN entry_title ON sub_col.key = entry_title.entry_key
        LEFT JOIN title ON entry_title.title_id = title.id;
        """
    ).format(
        key = sql.Literal(key)
    )

    # execute query
    try:
        t1 = time()
        cursor.execute(sql_query)
        t2 = time()
        logging.debug(f'paper_preview query took: {t2 - t1:.3} seconds')
    except errors.SyntaxError as err:
        logging.warning(err)
    except Exception as err:
        logging.error(err)

    # return results
    return cursor.fetchall()

def paper_authors(key: str) -> list[tuple]:
    """
    This function gets the authors of the paper with the given key.
    Parameters:
    - key: str => the paper key
    Return:
    - list[tuples] => the result of the query as list of tuples
    """
    # generate author sql query
    sql_query = sql.SQL("""
        SELECT author.name
        FROM (
            SELECT "key"
            FROM entry
            WHERE "key" = {key}
        ) AS sub_col
        LEFT JOIN entry_author ON sub_col.key = entry_author.entry_key
        LEFT JOIN author ON entry_author.author_id = author.id;
        """
    ).format(
        key = sql.Literal(key)
    )

    # execute query
    try:
        t1 = time()
        cursor.execute(sql_query)
        t2 = time()
        logging.debug(f'paper_authors query took: {t2 - t1:.3} seconds')
    except errors.SyntaxError as err:
        logging.warning(err)
    except Exception as err:
        logging.error(err)

    # return results
    return cursor.fetchall()

def paper_schools(key: str) -> list[tuple]:
    """
    This function gets the schools of the paper with the given key.
    Parameters:
    - key: str => the paper key
    Return:
    - list[tuples] => the result of the query as list of tuples
    """
    # generate author sql query
    sql_query = sql.SQL("""
        SELECT school.name
        FROM (
            SELECT "key"
            FROM entry
            WHERE "key" = {key}
        ) AS sub_col
        LEFT JOIN entry_school ON sub_col.key = entry_school.entry_key
        LEFT JOIN school ON entry_school.school_id = school.id;
        """
    ).format(
        key = sql.Literal(key)
    )

    # execute query
    try:
        t1 = time()
        cursor.execute(sql_query)
        t2 = time()
        logging.debug(f'paper_schools query took: {t2 - t1:.3} seconds')
    except errors.SyntaxError as err:
        logging.warning(err)
    except Exception as err:
        logging.error(err)

    # return results
    return cursor.fetchall()
