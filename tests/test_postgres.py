import pytest
from psycopg2 import errors
from app.modules.postgres import table_column_names, sql_from_dropdown

def test_table_column_names():
    table_column_names("author")

def test_table_column_names_invalid_type():
    with pytest.raises(TypeError):
        table_column_names(1)

def test_table_column_names_return_type():
    assert isinstance(table_column_names("author"), (list, tuple))

def test_sql_from_dropdown():
    sql_from_dropdown(["name", "COUNT(id)"], "school", "name", "COUNT(id)")

def test_sql_from_dropdown_invalid_type():
    # select
    with pytest.raises(TypeError):
        sql_from_dropdown([1, 2], "school", "name", "COUNT(id)")

    # table
    with pytest.raises(TypeError):
        sql_from_dropdown(["name", "COUNT(id)"], 1, "name", "COUNT(id)")

    # group_by
    with pytest.raises(TypeError):
        sql_from_dropdown(["name", "COUNT(id)"], "school", 1, "COUNT(id)")

    # order_by
    with pytest.raises(TypeError):
        sql_from_dropdown(["name", "COUNT(id)"], "school", "name", 1)

    # order
    with pytest.raises(TypeError):
        sql_from_dropdown(["name", "COUNT(id)"], "school", "name", "COUNT(id)", "True")

    # limit
    with pytest.raises(TypeError):
        sql_from_dropdown(["name", "COUNT(id)"], "school", "name", "COUNT(id)", limit="4")

def test_sql_from_dropdown_sql_error():
    with pytest.raises(errors.UndefinedColumn):
        sql_from_dropdown(["name", "test"], "school", "name", "COUNT(id)")
