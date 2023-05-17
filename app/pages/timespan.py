from dash import dcc, html
import dash_bootstrap_components as dbc
from app import components

from app.components.filter_card import generate_filter_card
from app.components.settings_card import generate_settings_card
from app.components.info_card import info_card

# define form
timespan_form = html.Div([
    dbc.Row([
        dbc.Label("Tabelle"),
        dcc.Dropdown(
            ["2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021", "2022"],
            placeholder="Choose the year",
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
            dbc.CardBody(dcc.Loading(
                type = "default",
                children = timespan_chart))
        ), width=10)
    ])
])