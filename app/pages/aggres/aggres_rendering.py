import pandas as pd
import plotly.express as px
from dash import dcc, Dash, html, Input, Output, dash, State, dash_table
from modules.postgres import sql_from_dropdown, author_pubs
from .aggres_contents import get_agres_contents
import logging


def aggres_render(app: Dash):
    """
    In Aggregation tab in the navbar, user selects one column
    Returns: description of the chosen column and aggregations of the it in different type of charts
    """

    @app.callback([Output("aggregation_chart", "figure"), Output("chart_content", "children"),
                   ],  # Output("top_popularity_slider", "value")
                  [Input("tabelle_dropdown", "value"), Input("chart_type", "value"),
                   Input("top_popularity_slider", "value")]
                  )
    # set author, and bar chart as default
    def draw_aggregation(selected_table: str = 'author', chart_type: str = 'bar chart', popularity_slider=10):
        # set data limit according to the slider in settings
        data_limit = popularity_slider

        content = get_agres_contents(column_name=selected_table)

        selected_columns: list[str] = [f'{selected_table}.name', 'sub_col.count']

        values = sql_from_dropdown(selected_columns, selected_table, "name", f'COUNT({selected_table}_{"id"})',
                                   limit=data_limit)

        selected_columns: list[str] = [f'{selected_table}', 'count']
        name = selected_columns[0]
        count = selected_columns[1]

        df = pd.DataFrame(values, columns=selected_columns)
        df = df.sort_values(by=[count], ascending=True)
        # print(df.head(3))
        chart_title = f'The {selected_table}s in top {data_limit} publications'

        logging.debug(df.head())
        if df.empty:
            return dash.no_update
        # copy_df = df
        # print('copy data: ',copy_df.head(3))
        bar_chart = px.bar(df, x=name, y=count, title=chart_title)
        pie_chart = px.pie(values=df.iloc[:, 1], names=df.iloc[:, 0], title=chart_title)

        if chart_type == 'bar chart':
            return bar_chart, content
        if chart_type == 'pie chart':
            return pie_chart, content

    # user click on the blue button, a modal of word_clouds image will be shown
    @app.callback(
        Output("modal", "is_open"),
        [Input("word_clouds_btn", "n_clicks"), Input("close-button", "n_clicks")],
        [State("modal", "is_open")],
    )
    def toggle_modal(open_clicks, close_clicks, is_open):
        if open_clicks or close_clicks:
            return not is_open
        return is_open

    # user click on a certain point in graph, the info will be shown accordinglly
    @app.callback([Output("data_table_modal", "is_open"), Output('data_table', 'children'),
                   Output('data_table_content', 'children')],
                  [Input("aggregation_chart", "clickData"), Input('close-data-table-btn', "n_clicks")],
                  State("data_table_modal", "is_open"))
    def show_data_table(click_data, close_click, is_open):
        """

        Args:
            click_data: get the value from the point where user clicked on
            close_click: check if user clicked on a close button
            is_open:  check if user clicked on a  certain point of the graph

        Returns: 10 latest publications of that author/school.. which contains year, title and the url

        """

        current_value = click_data['points'][0]['x']  # return name of the author/school... from dropdown
        total_publications = click_data['points'][0]['y']  # return number of publications
        # get data according to the chosen name
        data_info = author_pubs(current_value)
        result = dash_table.DataTable(data_info,
                                      style_data={'height': 'auto', 'whiteSpace': 'normal', 'textAlign': 'left',
                                                  'padding': '5px'}, style_header={'textAlign': 'center'})
        overview_discription = f'{current_value} has total of {total_publications} publications'

        if click_data or close_click:
            return not is_open, overview_discription, result
        return is_open
