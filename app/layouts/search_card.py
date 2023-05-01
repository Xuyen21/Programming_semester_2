import dash_bootstrap_components as dbc
from dash import html


search_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("What do you want to search for?", className="card-title"),
            html.P('author'),
            html.P('book'),
            html.P('year'),
            html.Button('Search', id='search_button')
        ]
    )
)
