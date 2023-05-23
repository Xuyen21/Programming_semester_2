import pandas as pd
import plotly.express as px
from dash import dcc, Dash, html, Input, Output, dash, State
from modules.postgres import sql_from_dropdown
from .aggres_contents import get_agres_contents


def aggres_render(app: Dash):
    """
    In Aggregation tab in the navbar, user selects one column
    Returns: description of the chosen column and aggregations of the it in different type of charts
    """
    @app.callback([Output("aggregation_chart", "figure"), Output("chart_content", "children"),
                   Output("top_popularity_slider", "value")],
                  [Input("tabelle_dropdown", "value"), Input("chart_type", "value"),
                   Input("top_popularity_slider", "value")]
                  )
    # set author, and bar chart as default
    def draw_aggregation(selected_table: str = 'author', chart_type: str = 'bar chart', popularity_slider=10):

        data_limit = round(popularity_slider)

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
            return px.bar(df, x=name, y=count), content, popularity_slider
        if chart_type == 'pie chart':
            return px.pie(values=df.iloc[:, 1], names=df.iloc[:, 0]), content, popularity_slider

    # user clicked button, a modal of word_clouds image will be shown
    @app.callback(
        Output("modal", "is_open"),
        [Input("word_clouds_btn", "n_clicks"), Input("close-button", "n_clicks")],
        [State("modal", "is_open")],
    )
    def toggle_modal(open_clicks, close_clicks, is_open):
        if open_clicks or close_clicks:
            return not is_open
        return is_open