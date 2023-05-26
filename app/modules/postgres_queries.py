"""
All the SQL requests get predefined in this File.
Created by: Silvan Wiedmer
Created at: 25.05.2023
"""
from psycopg2 import sql

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

def papers_per_month_query(year: str) -> sql.Composed:
    sub_query = sql.SQL("""
        SELECT entry_key, 'phdthesis' as entryType
        FROM phdthesis
        UNION
        SELECT entry_key, 'mastersthesis' as entryType
        FROM mastersthesis
        UNION
        SELECT entry_key, 'article' as entryType
        FROM article
        UNION
        SELECT entry_key, 'book' as entryType
        FROM book
    """)

    sql_query = sql.SQL("""
        SELECT DATE_TRUNC('month', e.mdate) as month, n.entryType, COUNT(n.entryType)
        FROM entry e
        JOIN ({sub_query}) n ON e.key = n.entry_key
        WHERE EXTRACT(YEAR FROM e.mdate) = {year}
        GROUP BY month, n.entryType
        ORDER BY month
    """).format(
        sub_query=sub_query,
        year=sql.Literal(year)
    )

    return sql_query

def update_year_dropdown_query() -> sql.SQL:
    sql_query: sql.SQL = sql.SQL("""
    SELECT DISTINCT EXTRACT(YEAR FROM mdate) as year
    FROM entry
    WHERE EXTRACT(YEAR FROM mdate) != EXTRACT(YEAR FROM NOW())
    """)

    return sql_query
