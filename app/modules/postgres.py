"""
Postgres Connector
Description: This module is resposible for the connection to the postgres database.
Created: 3.3.2023
"""
import os
import logging
from time import time
from psycopg2 import connect, errors, sql
import pandas as pd
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

def get_publications_table(name: str):
    """
    Args:
        name: value of the point on graph where user cliked on
    Returns: data of that chosen name, which contains year, title and url
    """
    query = sql.SQL("""
  select y.name as year, t.name as title, u.name as ee from author a
	join  entry_author ea on a.id = ea.author_id
	join  entry_year ey on ey.entry_key = ea.entry_key
	join year y on y.id = ey.year_id
	join entry_title et on et.entry_key = ea.entry_key
	join title t on t.id = et.title_id
	join entry_ee eu on eu.entry_key = ea.entry_key
	join ee u on u.id = eu.ee_id
	where a.name={name} limit 10
  """).format(name=sql.Literal(name))
    # execute query
    try:
        t1 = time()
        cursor.execute(query)
        t2 = time()
        logging.debug(f'author"s publications query took: {t2 - t1:.3} seconds')
    except errors.SyntaxError as err:
        logging.warning(err)
    except Exception as err:
        logging.error(err)
    fetch_data_table = cursor.fetchall()
    data_info = pd.DataFrame(fetch_data_table, columns=['Year', 'Title', 'Url'])
    result = data_info.to_dict('records')
    # print(result)
    return result
