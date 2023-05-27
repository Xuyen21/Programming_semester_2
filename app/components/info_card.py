from dash import html
import dash_bootstrap_components as dbc

info_card = dbc.Card(
    dbc.CardBody([
        html.H4('About DBLP'),
        html.P('The dblp computer science bibliography provides open bibliographic information on major computer science journals and proceedings.'),
    ])
)
