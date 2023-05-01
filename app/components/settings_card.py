from dash import html
import dash_bootstrap_components as dbc

def generate_settings_card(settings):
    settings_card = dbc.Card(
        dbc.CardBody(
            [
                html.H5("Settings"),
                settings
            ]
        )
    )

    return settings_card
