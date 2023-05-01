from lxml import etree

from psycopg2 import sql
from postgres import conn

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
    'www',
    'data'
]

cursor = conn.cursor()

for event, element in etree.iterparse('dblp.xml', dtd_validation=True):
    if element.tag in types:
        # create new entry from parent tag
        INSERT_QUERY = 'INSERT INTO entry (publish_date, key) VALUES (%s, %s)'
        cursor.execute(INSERT_QUERY, (element.attrib["mdate"], element.attrib["key"]))
        conn.commit()

        non_duplicate = []

        # go trough all childs
        for child in element:

            # if child is duplicate => put in duplicate table
            if child.tag in duplicates:

                tag: str = str(child.tag).replace('"',"'")

                INSERT_SQL = sql.SQL('INSERT INTO {table} (name) VALUES (%s)').format(
                    table = sql.Identifier(tag)
                )

                cursor.execute(INSERT_SQL, (child.text,))
                conn.commit()

                INSERT_ENTRY_AUTHOR = sql.SQL('INSERT INTO {table} ({column}, entry_id) VALUES ((SELECT MAX(id) FROM {table2}), (SELECT MAX(id) FROM entry))').format(
                    table = sql.Identifier('entry_' + tag),
                    column = sql.Identifier(tag + '_id'),
                    table2 = sql.Identifier(tag)
                )
                cursor.execute(INSERT_ENTRY_AUTHOR)
                conn.commit()
            else:
                non_duplicate.append(child)

        columns = ['entry_id']
        values = []

        for c in non_duplicate:
            columns.append(c.tag)
            values.append(c.text)

        if len(values) != 0:
            # add to according table
            INSERT_PAPER = sql.SQL('INSERT INTO {table} ({column}) VALUES ({id}, {value})').format(
                table = sql.Identifier(element.tag),
                column = sql.SQL(', '.join(columns)),
                id = sql.SQL('(SELECT MAX(id) FROM entry)'),
                value = sql.SQL(",").join(map(sql.Literal, values))
            )

            cursor.execute(INSERT_PAPER)
            conn.commit()
        else:
            # add to according table
            INSERT_PAPER = sql.SQL('INSERT INTO {table} ({column}) VALUES ({id})').format(
                table = sql.Identifier(element.tag),
                column = sql.SQL(', '.join(columns)),
                id = sql.SQL('(SELECT MAX(id) FROM entry)')
            )

            cursor.execute(INSERT_PAPER)
            conn.commit()

        element.clear()
