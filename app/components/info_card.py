"""
This Component represents the info card
visible on the left side of the dashboard.
"""
from dash import html
import dash_bootstrap_components as dbc

info_card = dbc.Card(
    dbc.CardBody(
        [
            html.H4('About DBLP'),
            html.P("""The dblp computer science bibliography provides open bibliographic
                information on major computer science journals and proceedings."""
            ),
        ]
    ),
    style={
        'margin': '10px', 
        'box-shadow': 'rgba(0,0,0,0.35) 0px 5px 5px'
    }
)
