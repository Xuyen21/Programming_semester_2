from dash import Dash, html
import dash_bootstrap_components as dbc
from filter_card import generate_filter_card


from search_card import search_card
from info_display_card import info_display_card


search_filter_cards = html.Div([
    dbc.Row(search_card),
    html.Hr(),
    dbc.Row(generate_filter_card())
])

app_layout = dbc.Row(
    [
        dbc.Col(search_filter_cards, width=3),
        dbc.Col(info_display_card, width=7)
    ]
)


def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            app_layout,

        ],
    )



