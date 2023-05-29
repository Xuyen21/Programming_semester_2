import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, State, dash_table, dash
from flask_caching import Cache

# modules
from modules.postgres import execute_query
from modules.postgres_queries import aggregate_column_query, publications_table_query
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
            Output("column_description_aggregation", "children")
        ],
        [
            Input("tabelle_dropdown", "value"),
            Input("chart_type", "value"),
            Input("top_popularity_slider", "value")
        ]
    )
    @cache.memoize(timeout=cache_timeout)
    # set author, and bar chart as default
    def draw_aggregation(selected_table: str='author', chart_type: str='bar chart', popularity_slider=10):
        # set data limit according to the slider in settings
        data_limit = popularity_slider

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

        df_aggreg = pd.DataFrame(values, columns=selected_columns)
        df_aggreg = df_aggreg.sort_values(by=[count], ascending=True)

        chart_title = f'The top {data_limit} {selected_table}'
        bar_chart = px.bar(df_aggreg, x=name, y=count, title=chart_title)
        pie_chart = px.pie(values=df_aggreg.iloc[:, 1], names=df_aggreg.iloc[:, 0], title=chart_title)

        if chart_type == 'bar chart':
            return bar_chart, content
        if chart_type == 'pie chart':
            return pie_chart, content

    # user click on the blue button, a modal of word_clouds image will be shown
    @app.callback(
        Output("modal", "is_open"),
        [
            Input("word_clouds_btn", "n_clicks")
        ],
        [
            State("modal", "is_open")
        ],
    )
    def toggle_modal(open_clicks, is_open):
        # when first initialized => don't open
        if open_clicks == 0:
            return False

        return not is_open

    # user click on a certain point in graph, the info will be shown accordinglly
    @app.callback(
        [
            Output("data_table_modal", "is_open"),
            Output('data_table', 'children'),
            Output('data_table_content', 'children')
        ],
        [
            Input("aggregation_chart", "clickData"),
        ],
        State("data_table_modal", "is_open")
    )
    @cache.memoize(timeout=cache_timeout)
    def show_data_table(click_data, is_open):
        """

        Args:
            click_data: get the value from the point where user clicked on
            close_click: check if user clicked on a close button
            is_open:  check if user clicked on a  certain point of the graph

        Returns: 10 latest publications of that author/school.. which contains year, title and the url

        """
        if click_data is None:
            return False, dash.no_update, dash.no_update

        current_value = click_data['points'][0]['x']  # return name from dropdown
        total_publications = click_data['points'][0]['y']  # return number of publications

        # request data
        publications_query = execute_query(
            publications_table_query(current_value),
            'publications_table_query'
        )
        data_info = pd.DataFrame(publications_query, columns=['Year', 'Title', 'Url'])
        result = dash_table.DataTable(
            data_info.to_dict('records'),
            style_data={
                'height': 'auto',
                'whiteSpace': 'normal',
                'textAlign': 'left',
                'padding': '5px'
            },
            style_header={
                'textAlign': 'center'
            }
        )
        overview_discription = f'{current_value} has a total of {total_publications} publications'

        return not is_open, overview_discription, result
