"""
This Component represents the settings card
visible on the left side of the dashboard.
"""
from dash import html
import dash_bootstrap_components as dbc

def generate_settings_card(settings):
    """
    This function is used to customize the settings card.
    """
    settings_card = dbc.Card(
        dbc.CardBody(
            [
                html.H4("Settings"),
                settings
            ]
        ),
        style={
            'margin': '10px',
            'box-shadow': 'rgba(0,0,0,0.35) 0px 5px 5px'
        }
    )

    return settings_card
