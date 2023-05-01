import dash_bootstrap_components as dbc
from dash import html


def generate_filter_card():
    return dbc.Card(
        dbc.CardBody(
            [
                html.H5("Filter by", className="card-title"),
                html.P('poppular research topic'),
                html.P('influential researcher'),
            ]
        )
    )
