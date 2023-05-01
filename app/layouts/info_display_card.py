import dash_bootstrap_components as dbc
from dash import html, dcc

from layouts.distribution_diagram import generate_pie_chart


# from distribution_diagram import generate_pie_chart
def info_display_card(app):
    return dbc.Card(
        dbc.CardBody(
            [
                # html.H5("About DBLP", className="card-title"),
                html.Div(
                    children=[html.H3('About DBLP'),
                              html.P(
                                  'The dblp computer science bibliography provides open bibliographic information on major computer science journals and proceedings.'),
                              html.H3(['Distribution of publication type']),
                              html.Br(),

                              ]
                ),
                generate_pie_chart(app)

            ]
        )
    )
