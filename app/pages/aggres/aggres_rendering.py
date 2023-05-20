import pandas as pd
import plotly.express as px
from dash import dcc, Dash, html, Input, Output, dash
from modules.postgres import sql_from_dropdown
from .aggres_contents import get_agres_contents


def aggres_render(app: Dash):
    """
    In Aggregation tab in the navbar, user selects one column
    Returns: description of the chosen column and aggregations of the it in different type of charts
    """

    @app.callback([Output("aggregation_chart", "figure"), Output("chart_content", "children"),
                   ],
                  [Input("tabelle_dropdown", "value"), Input("chart_type", "value"),
                   Input("top_popularity_slider", "value")]
                  )
    # set author, and bar chart as default
    def draw_aggregation(selected_table: str = 'author', chart_type: str = 'bar chart', popularity_slider=None):

        # display content according to user-chosen column
        if popularity_slider is None:
            popularity_slider = [0, 10]
        # get the user-chosen popularity, use round because the limit must be an integer
        data_limit = round(popularity_slider[1])

        content = get_agres_contents(column_name=selected_table)

        selected_columns: list[str] = [f'{selected_table}.name', 'sub_col.count']

        values = sql_from_dropdown(selected_columns, selected_table, "name", f'COUNT({selected_table}_{"id"})',
                                   limit=data_limit)

        selected_columns: list[str] = [f'{selected_table}', 'count']
        name = selected_columns[0]
        count = selected_columns[1]

        df = pd.DataFrame(values, columns=selected_columns)
        df = df.sort_values(by=[count], ascending=True)

        if chart_type == 'bar chart':
            return px.bar(df, x=name, y=count), content
        if chart_type == 'pie chart':
            return px.pie(values=df.iloc[:, 1], names=df.iloc[:, 0]), content
