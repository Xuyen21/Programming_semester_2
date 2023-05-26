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
    """
    This function executes all the queries for the Dashboard.
    Parameters:
    - query: Any => The sql query to execute
    - name: str => The name of the query (used for debugging)
    """
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
