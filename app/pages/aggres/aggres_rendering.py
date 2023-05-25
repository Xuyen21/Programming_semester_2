import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, State
from flask_caching import Cache
from psycopg2 import sql
from modules.postgres import execute_query
from modules.postgres_queries import aggregate_column_query
from modules.column_descriptions import get_column_description

def aggres_render(app: Dash, cache: Cache, cache_timeout: int = 600):
    """
    In Aggregation tab in the navbar, user selects one column
    Returns: description of the chosen column and aggregations of the it in different type of charts
    """

    # define sql request
    @cache.memoize(timeout=cache_timeout)
    def aggregate_column(select: list[str], table: str, group_by: str, order_by: str, order: bool = False, limit: int = 10) -> list[tuple]:
        """
        This function gets the parameters provided by the dashboard, converts it to a sql query
        and returns the result as a list of tuples.
        Parameters:
        - select: list[str] => the columns to be selected
        - table: str => the table to select from
        - group_by: str => the column to group by
        - order_by: str => the column to order by
        - order: bool = False => ASC or DESC order (True = ASC)
        - limit: int = 10 => Row limitation
        Return:
        - list[tuples] => the result of the query as list of tuples
        """

        sql_query = aggregate_column_query(select, table, group_by, order_by, order, limit)

        return execute_query(sql_query, 'aggregation_chart')

    @app.callback(
        [
            Output("aggregation_chart", "figure"),
            Output("column_description_aggregation", "children"),
            Output("top_popularity_slider", "value")
        ],
        [
            Input("tabelle_dropdown", "value"),
            Input("chart_type", "value"),
            Input("top_popularity_slider", "value")
        ]
    )
    @cache.memoize(timeout=cache_timeout)
    # set author, and bar chart as default
    def draw_aggregation(selected_table: str = 'author', chart_type: str = 'bar chart', popularity_slider=10):

        data_limit = round(popularity_slider)

        content = get_column_description(column_name=selected_table)

        selected_columns: list[str] = [f'{selected_table}.name', 'sub_col.count']

        values = aggregate_column(
            selected_columns,
            selected_table,
            "name",
            f'COUNT({selected_table}_{"id"})',
            limit=data_limit
        )

        selected_columns: list[str] = [f'{selected_table}', 'count']
        name = selected_columns[0]
        count = selected_columns[1]

        df = pd.DataFrame(values, columns=selected_columns)
        df = df.sort_values(by=[count], ascending=True)

        if chart_type == 'bar chart':
            return px.bar(df, x=name, y=count), content, popularity_slider
        if chart_type == 'pie chart':
            return px.pie(values=df.iloc[:, 1], names=df.iloc[:, 0]), content, popularity_slider

    # user clicked button, a modal of word_clouds image will be shown
    @app.callback(
        Output("modal", "is_open"),
        [
            Input("word_clouds_btn", "n_clicks"),
            Input("close-button", "n_clicks")
        ],
        [
            State("modal", "is_open")
        ],
    )
    def toggle_modal(open_clicks, close_clicks, is_open):
        if open_clicks or close_clicks:
            return not is_open
        return is_open
