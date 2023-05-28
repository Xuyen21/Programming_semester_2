import dash_bootstrap_components as dbc
from dash import html

def generate_filter_card(form):
    filter_card = dbc.Card(
        dbc.CardBody(
            [
                html.H4("Filter", className="card-title"),
                form
            ]
        ),
        style={
            'margin': '10px', 
            'box-shadow': 'rgba(0,0,0,0.35) 0px 5px 5px'
        }
    )

    return filter_card