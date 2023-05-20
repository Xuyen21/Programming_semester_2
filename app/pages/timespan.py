import os
from dotenv import load_dotenv
# load environments from .env file
load_dotenv()

# not working in VSCODE without that
if os.getenv('VSCODE') == "True":
    import sys
    sys.path.append('./')

from dash import dcc, html
import dash_bootstrap_components as dbc

from app.components.filter_card import generate_filter_card
from app.components.settings_card import generate_settings_card
from app.components.info_card import info_card

from app.modules.postgres import update_year_dropdown

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

# Define chart
timespan_chart = dcc.Graph(id="timespan_chart")

# Define timespan tab
timespan_tab = dcc.Tab(label="Timespan", children=[
    dbc.Row([
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
    ])
])
