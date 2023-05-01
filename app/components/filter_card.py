import dash_bootstrap_components as dbc
from dash import html

def generate_filter_card(form):
    filter_card = dbc.Card(
        dbc.CardBody(
            [
                html.H5("What do you want to filter ?", className="card-title"),
                form
            ]
        )
    )

    return filter_card