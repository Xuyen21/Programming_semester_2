"""
Postgres Connector
Description: This module is resposible for the connection to the postgres database.
Created: 3.3.2023
"""
import os
import logging
from time import time
from psycopg2 import connect, errors
from dotenv import load_dotenv

# load environments from .env file
load_dotenv()

# postgress connection
conn = connect(
    database=os.getenv('DATABASE_NAME'),
    host="localhost",
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
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
    Return:
    - list[tuple] => The results of the query
    """
    # execute query
    try:
        before = time()
        cursor.execute(query)
        after = time()
        logging.debug("%s query took: %s seconds", name, (round(after-before, 2)))
    except errors.SyntaxError as error:
        logging.warning(error)

    # return results
    return cursor.fetchall()
