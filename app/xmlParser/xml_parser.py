"""
This module parses the dblp.xml file into sql and stores it in a postgres database.
Created by: Silvan Wiedmer
Created at: 17.03.2023
"""
import os
from time import time
from multiprocessing import Process, Queue

from psycopg2 import connect, sql, errors
from dotenv import load_dotenv
from lxml import etree

# load environment variables from .env file
load_dotenv()

# define worker amount
WORKERS: int = 5

duplicates: list[str] = [
    "cdrom",
    "cite",
    "publisher",
    "author",
    "note",
    "school",
    "editor",
    "url",
    "ee",
    "crossref",
    "isbn",
    "pages",
    "year",
    "title",
    "series"
]

types: list[str] = [
    'article',
    'inproceedings',
    'proceedings',
    'book',
    'incollection',
    'phdthesis',
    'mastersthesis',
    'www'
]

# postgress connection
conn = connect(
    database = "Test",
    host = "localhost",
    user = os.getenv('POSTGRES_USER'),
    password = os.getenv('POSTGRES_PASSWORD'),
    port="5432"
)

def elements(queue_sql: Queue, element) -> None:
    """
    The elements function generates the sql for the entire element and sends it to the sql queue.

    Parameters:
    - queue_sql: Queue => The queue to transfer sql commands to different processes
    - element => The current xml element to parse
    """
    # create sql query for insertion
    query = sql.SQL('INSERT INTO entry ({columns}) VALUES ({values});').format(
        columns = sql.SQL(",").join(map(sql.Identifier, element.attrib)),
        values = sql.SQL(",").join(map(sql.Literal, element.attrib.values()))
    )

    non_duplicate = []

    # check all childs of element
    for child in element:

        # check if tag is duplicate
        if child.tag in duplicates:
            tag: str = str(child.tag)

            insert_child_tag = sql.SQL(
                'INSERT INTO {table} (name) VALUES ({text}) ON CONFLICT (name) DO NOTHING;'
                ).format(
                table = sql.Identifier(tag),
                text = sql.Literal(child.text)
            )

            insert_entry_child = sql.SQL(
                'INSERT INTO {table} ({column}, entry_key) VALUES ((SELECT id FROM {table2} WHERE name = {text}), {key});'
                ).format(
                table = sql.Identifier('entry_' + tag),
                column = sql.Identifier(tag + '_id'),
                table2 = sql.Identifier(tag),
                key = sql.Literal(element.attrib["key"]),
                text = sql.Literal(child.text)
            )

            query += insert_child_tag
            query += insert_entry_child
        else:
            non_duplicate.append(child)

    columns = ['entry_key']
    values = []

    for childs in non_duplicate:
        columns.append(childs.tag)
        values.append(childs.text)

    if len(values) != 0:
        # add to according table
        insert_non_duplicates = sql.SQL(
            'INSERT INTO {table} ({column}) VALUES ({id}, {value});'
            ).format(
            table = sql.Identifier(element.tag),
            column = sql.SQL(', '.join(columns)),
            id = sql.Literal(element.attrib["key"]),
            value = sql.SQL(",").join(map(sql.Literal, values))
        )
    else:
        # add to according table
        insert_non_duplicates = sql.SQL('INSERT INTO {table} ({column}) VALUES ({id});').format(
            table = sql.Identifier(element.tag),
            column = sql.SQL(', '.join(columns)),
            id = sql.Literal(element.attrib["key"])
        )

    query += insert_non_duplicates

    queue_sql.put(query)

def read(queue_sql: Queue):
    """
    The read function reads the xml file and calls the elements function for every element

    Parameters: 
    - queue_sql: Queue => The queue required for the elements function
    """
    before = time()
    # read file
    for _, element in etree.iterparse('dblp.xml', dtd_validation=True):
        # check if current tag in types
        if element.tag in types:

            # process elements
            elements(queue_sql, element)

            # clear element from memory
            element.clear()

    after = time()

    print(f'Read file in {after - before:.3} seconds')
    print("-" * 75)

    # stop workers
    for _ in range(WORKERS):
        queue_sql.put('STOP')

def insert(queue: Queue):
    """
    The insert function executes all the sql querys from the provided queue until 'Stop' is received

    Parameters:
    - queue: Queue => The queue to get the queries from
    """
    cursor = conn.cursor()
    before = time()
    for query in iter(queue.get, 'STOP'):
        try:
            cursor.execute(query)
        except errors.InvalidColumnReference as error:
            print(error)
            print(query)
            print("-" * 75)
        conn.commit()
    after = time()

    print(f'Executed SQL commands in {after - before:.3} seconds')
    return

if __name__ == "__main__":
    sql_queue = Queue()

    read_process = Process(target=read, args=(sql_queue, ))
    read_process.start()

    insert_processes: list[Process] = []
    for _ in range(WORKERS):
        insert_processes.append(Process(target=insert, args=(sql_queue,)))

    for process in insert_processes:
        process.start()

    read_process.join()

    for process in insert_processes:
        process.join()
