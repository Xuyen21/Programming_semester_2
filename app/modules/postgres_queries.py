"""
All the SQL requests get predefined in this File.
Created by: Silvan Wiedmer
Created at: 25.05.2023
"""
from psycopg2 import sql

# Aggregation
def aggregate_column_query(select: list[str], table: str, group_by: str, order_by: str, order: bool = False, limit: int = 10) -> sql.Composed:
    """
    This function generate the query for aggregate_column
    Parameters:
    - select: list[str] => the columns to be selected
    - table: str => the table to select from
    - group_by: str => the column to group by
    - order_by: str => the column to order by
    - order: bool = False => ASC or DESC order (True = ASC)
    - limit: int = 10 => Row limitation
    Return:
    - sql.Composed => the resulting query
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

    return sql_query

def publications_table_query(name: str) -> sql.Composed:
    """
    Args:
        name: value of the point on graph where user cliked on
    Returns: data of that chosen name, which contains year, title and url
    """
    sql_query = sql.SQL("""
        SELECT "year".name AS "year", title.name AS "title", ee.name AS "ee"
        FROM (
            SELECT "id"
            FROM author
            WHERE "name" = {name}
        ) AS sub_col
        LEFT JOIN entry_author ON sub_col.id = entry_author.author_id
        LEFT JOIN entry_year ON entry_year.entry_key = entry_author.entry_key
        LEFT JOIN "year" ON "year".id = entry_year.year_id
        LEFT JOIN entry_title ON entry_title.entry_key = entry_author.entry_key
        LEFT JOIN title ON title.id = entry_title.title_id
        LEFT JOIN entry_ee ON entry_ee.entry_key = entry_author.entry_key
        LEFT JOIN ee ON ee.id = entry_ee.ee_id
        WHERE "year" IS NOT null
        ORDER BY "year" DESC
        LIMIT 10;
    """).format(name=sql.Literal(name))

    return sql_query

# Relation
def author_relations_query(table: str, limit: int) -> sql.Composed:
    """
    This function get's the author relationships.
    Parameters:
    - table: str => the specified table
    - limit: int => the number of rows to return
    Return:
    - sql.Composed => the resulting query
    """
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

    return sql_query

def school_relations_query(table: str, limit: int) -> sql.Composed:
    """
    This function get's the school relationships.
    Parameters:
    - table: str => the specified table
    - limit: int => the number of rows to return
    Return:
    - sql.Composed => the resulting query
    """
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

    return sql_query

def paper_date_title_query(key: str) -> sql.Composed:
    """
    This function gets the date and title of the paper with the given key.
    Parameters:
    - key: str => the paper key
    Return:
    - sql.Composed => the resulting query
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

    return sql_query

def paper_authors_query(key: str) -> sql.Composed:
    """
    This function gets the authors of the paper with the given key.
    Parameters:
    - key: str => the paper key
    Return:
    - sql.Composed => the resulting query
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

    return sql_query

def paper_schools_query(key: str) -> sql.Composed:
    """
    This function gets the schools of the paper with the given key.
    Parameters:
    - key: str => the paper key
    Return:
    - sql.Composed => the resulting query
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

    return sql_query

# Timespan
def papers_per_year_query() -> sql.SQL:
    """
    This function gets the published papers per month of the specified year
    Return:
    - sql.SQL => the resulting query
    """

    sql_query = sql.SQL("""
        SELECT m.entry_key, 'mastersthesis' as entryType, y."name" as year
        FROM mastersthesis m
        LEFT JOIN entry e ON m.entry_key = e."key"
        LEFT JOIN entry_year ey ON ey.entry_key = e."key"
        LEFT JOIN "year" y ON y.id = ey.year_id
        UNION
        SELECT p.entry_key, 'phdthesis' as entryType, y."name" as year
        FROM phdthesis p
        LEFT JOIN entry e ON p.entry_key = e."key"
        LEFT JOIN entry_year ey ON ey.entry_key = e."key"
        LEFT JOIN "year" y ON y.id = ey.year_id
        UNION
        SELECT a.entry_key, 'article' as entryType, y."name" as year
        FROM article a
        LEFT JOIN entry e ON a.entry_key = e."key"
        LEFT JOIN entry_year ey ON ey.entry_key = e."key"
        LEFT JOIN "year" y ON y.id = ey.year_id
        UNION
        SELECT b.entry_key, 'book' as entryType, y."name" as year
        FROM book b
        LEFT JOIN entry e ON b.entry_key = e."key"
        LEFT JOIN entry_year ey ON ey.entry_key = e."key"
        LEFT JOIN "year" y ON y.id = ey.year_id
    """)

    return sql_query
