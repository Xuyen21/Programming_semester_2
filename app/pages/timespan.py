"""
This module is responsible for the timespan tab of the DBLP Dashboard.

Created by: Karolina Thöny-Tyganova
"""
import plotly.express as px
from dash import dcc, html, Input, Output, Dash
import dash_bootstrap_components as dbc
import pandas as pd
from flask_caching import Cache

# modules
from modules.postgres import execute_query
from modules.postgres_queries import papers_per_year_query

# components
from components.filter_card import generate_filter_card
from components.settings_card import generate_settings_card
from components.info_card import info_card

# Define form
timespan_form = html.Div([
    dbc.Row([
        html.P("No Filter available")
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
    dbc.Col(
        dbc.Card(
            dbc.CardBody(
                dcc.Loading(
                    type="default",
                    children=timespan_chart
                )
            ),
            style={
                'margin': '10px', 
                'box-shadow': 'rgba(0,0,0,0.35) 0px 5px 5px'
            }
        ),
        width=10
    )
]

# define timespan_callbackcallback
def timespan_callback(app: Dash, cache: Cache, cache_timeout: int = 600):

    # define sql request
    @cache.memoize(timeout=cache_timeout)
    def papers_per_year() -> pd.DataFrame:
        sql_query = papers_per_year_query()

        results = execute_query(sql_query, 'papers_per_year')
        df_papers = pd.DataFrame(results, columns=['entry_key', 'entryType', 'year'])

        return df_papers

    @app.callback(
        Output("timespan_chart", "figure"),
        Input("chart_type_dropdown", "value")
    )
    @cache.memoize(timeout=cache_timeout)
    def draw_timespan(chart_type: str):
        df_papers = papers_per_year()
        grouped_df = df_papers.groupby(['year', 'entryType']).size().reset_index(name='count')

        if chart_type == "pie":
            fig = px.pie(grouped_df, values='count', names='entryType', title='Publications over the years', color='entryType')
        else:
            fig = px.bar(grouped_df, x='year', y='count', color='entryType')

        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Number of Publications",
        )

        return fig
