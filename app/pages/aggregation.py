from dash import dcc, html
import dash_bootstrap_components as dbc

from components.filter_card import generate_filter_card
from components.settings_card import generate_settings_card
from components.info_card import info_card

# define form
aggregation_form = html.Div([
    dbc.Row([
        dbc.Label("Tabelle"),
        dcc.Dropdown(
            ["author", "editor", "pages", "publisher", "school", "year"],
            placeholder="Tabelle auswählen",
            id = "tabelle_dropdown"
        )
    ])
])

# define chart
aggregation_chart = dcc.Graph(id="aggregation_chart")

# define aggregation tab
aggregation_tab = dcc.Tab(label = "Aggregation", children = [
    dbc.Row([
        dbc.Col([
            generate_filter_card(aggregation_form),
            generate_settings_card(html.P("Not Implemented")),
            info_card
        ], width=2),
        dbc.Col(dbc.Card(
            dbc.CardBody(dcc.Loading(
                type = "default",
                children = aggregation_chart
            )
            )
        ), width=10)
    ])
])