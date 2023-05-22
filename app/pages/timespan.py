import os
from dotenv import load_dotenv
# load environments from .env file
load_dotenv()

# not working in VSCODE without that
if os.getenv('VSCODE') == "True":
    import sys
    sys.path.append('./')

import plotly.express as px

from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

from app.components.filter_card import generate_filter_card
from app.components.settings_card import generate_settings_card
from app.components.info_card import info_card

from app.modules.postgres import update_year_dropdown, papers_per_month

# Define form
timespan_form = html.Div([
    dbc.Row([
        dbc.Label("Table"),
        dcc.Dropdown(
            options=update_year_dropdown(),
            placeholder="Choose the year",
            id="year_dropdown"
        )
    ]),
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
        generate_settings_card(html.P("Not Implemented")),
        info_card
    ], width=2),
    dbc.Col(dbc.Card(
        dbc.CardBody(dcc.Loading(
            type="default",
            children=timespan_chart))
    ), width=10)
]

# define timespan_callbackcallback
def timespan_callback(app):
    @app.callback(
        Output("timespan_chart", "figure"),
        Input("year_dropdown", "value"),
        Input("chart_type_dropdown", "value")
    )
    def draw_timespan(selected_year: str, chart_type: str):
        if not selected_year:
            selected_year = "2022"

        df = papers_per_month(selected_year)

        if chart_type == "bar":
            fig = px.bar(df, x='month', y='count', color='entryType', barmode='group')
        elif chart_type == "pie":
            fig = px.pie(df, values='count', names='entryType')

        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Number of publications",
        )

        return fig