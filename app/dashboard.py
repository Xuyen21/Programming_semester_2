# from app.layouts.layout import create_layout
from dash_bootstrap_components.themes import BOOTSTRAP

# from .layouts.distribution_diagram import generate_pie_chart
from dash import Dash, html
import dash_bootstrap_components as dbc
from layouts.filter_card import generate_filter_card

from layouts.search_card import search_card
from layouts.info_display_card import info_display_card

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

        ]
    )


def main():
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = 'WELCOME TO DBLP'
    app.layout = create_layout(app)
    app.run(debug=True)


if __name__ == '__main__':
    main()
