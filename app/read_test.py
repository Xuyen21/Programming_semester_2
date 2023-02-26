from lxml import etree
from postgres import conn

types: list[str] = [
    'article',
    'inproceedings',
    'proceedings',
    'book',
    'incollection',
    'phdthesis',
    'mastersthesis',
    'www',
    'person',
    'data'
]

cursor = conn.cursor()

for event, element in etree.iterparse('dblp.xml', dtd_validation=True):
    if element.tag == 'phdthesis':

        print(element.attrib)
        INSERT_QUERY = 'INSERT INTO entry (publish_date, key) VALUES (%s, %s)'
        cursor.execute(INSERT_QUERY, (element.attrib["mdate"], element.attrib["key"]))
        conn.commit()

        for child in element:
            print(f'{child.tag}: {child.text}')
            if child.tag == 'author':
                INSERT_AUTHOR: str = 'INSERT INTO author (name) VALUES (%s)'
                cursor.execute(INSERT_AUTHOR, (child.text, ))
                conn.commit()

                INSERT_ENTRY_AUTHOR: str = """
                    INSERT INTO entry_author (author_id, entry_id) 
                    VALUES ((SELECT MAX(id) FROM author), (SELECT MAX(id) FROM entry))
                    """
                cursor.execute(INSERT_ENTRY_AUTHOR)
                conn.commit()

        element.clear()
        break
