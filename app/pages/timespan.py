from dash import dcc, html
import dash_bootstrap_components as dbc

from components.filter_card import generate_filter_card
from components.settings_card import generate_settings_card
from components.info_card import info_card

# define form
timespan_form = html.Div([
    dbc.Row([
        dbc.Label("Tabelle"),
        dcc.Dropdown(
            ["2021", "2022"],
            placeholder="Jahr auswählen",
            id = "year_dropdown"
        )
    ])
])

# define chart
timespan_chart = dcc.Graph(id="timespan_chart")

# define aggregation tab
timespan_tab = dcc.Tab(label = "Timespan", children = [
    dbc.Row([
        dbc.Col([
            generate_filter_card(timespan_form),
            generate_settings_card(html.P("Not Implemented")),
            info_card
        ], width=2),
        dbc.Col(dbc.Card(
            dbc.CardBody(timespan_chart)
        ), width=6)
    ])
])