"""
This module is responsible for the timespan tab of the DBLP Dashboard.
"""
import plotly.express as px
from dash import dcc, html, Input, Output, Dash
import dash_bootstrap_components as dbc
import pandas as pd
from flask_caching import Cache

# modules
from modules.postgres import execute_query
from modules.postgres_queries import papers_per_month_query, update_year_dropdown_query

# components
from components.filter_card import generate_filter_card
from components.settings_card import generate_settings_card
from components.info_card import info_card

# Define form
timespan_form = html.Div([
    dbc.Row([
        dbc.Label("Table"),
        dcc.Dropdown(
            options=[
                {"label": str(year[0]), "value": str(year[0])} for year in execute_query(update_year_dropdown_query(), 'update_year_dropdown')
            ],
            placeholder="Choose the year",
            id="year_dropdown",
            value ="2022"
        )
    ])
])

# Define timespan_chart
timespan_chart = dcc.Graph(id="timespan_chart")

# Define timespan_tab
timespan_tab = dcc.Tab(label="Timespan", value="timespan_tab")

# Define timespan_children
timespan_children = [
    dbc.Col([
        generate_filter_card(timespan_form),
        generate_settings_card(
    dbc.Row([
        dbc.Label("Chart Type"),
        dcc.Dropdown(
            options=[
                {"label": "Bar Chart", "value": "bar"},
                {"label": "Pie Chart", "value": "pie"}
            ],
            value="bar",
            id="chart_type_dropdown"
        )
    ])),
        info_card
    ], width=2),
    dbc.Col(dbc.Card(
        dbc.CardBody(dcc.Loading(
            type="default",
            children=timespan_chart))
    ), width=10)
]

# define timespan_callbackcallback
def timespan_callback(app: Dash, cache: Cache, cache_timeout: int = 600):

    # define sql request
    @cache.memoize(timeout=cache_timeout)
    def papers_per_month(year: str) -> pd.DataFrame:
        sql_query = papers_per_month_query(year)

        results = execute_query(sql_query, 'papers_per_month')
        df_papers = pd.DataFrame(results, columns=['month', 'entryType', 'count'])

        return df_papers

    @app.callback(
        Output("timespan_chart", "figure"),
        Input("year_dropdown", "value"),
        Input("chart_type_dropdown", "value")
    )
    @cache.memoize(timeout=cache_timeout)
    def draw_timespan(selected_year: str, chart_type: str):
        if not selected_year:
            selected_year = "2022"

        df_papers = papers_per_month(selected_year)

        if chart_type == "pie":
            fig = px.pie(df_papers, values='count', names='entryType',color='entryType')
        else:
            fig = px.bar(df_papers, x='month', y='count', color='entryType')

        # https://dblp.org/faq/16154937.html
        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Number of modifications",
        )

        return fig
