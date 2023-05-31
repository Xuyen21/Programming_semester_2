"""
This module is responsible for the aggregation tab of the DBLP Dashboard.

Created by: Xuyen Furmanczuk
"""
from dash import dcc, html
import dash_bootstrap_components as dbc

from components.filter_card import generate_filter_card
from components.settings_card import generate_settings_card
from components.info_card import info_card

# define form
aggregation_form = html.Div([
    dbc.Row([
        dbc.Label("Table"),
        dcc.Dropdown(
            ["author", "editor", "pages", "publisher", "school"],
            placeholder="Tabelle auswählen",
            value='author',
            id="tabelle_dropdown"
        ),
        # create button top popover the word_clouds image
        html.Div([
            dbc.Button('See top words in titles', id='word_clouds_btn', n_clicks=0, color="info",
                       className="me-md-2",
                       style={'margin-top': '20px'}),
            dbc.Modal([
                dbc.ModalHeader("Explore the frequency of keywords in title"),
                dbc.ModalBody([
                    html.Img(src='assets/word_clouds.png',
                             style={"width": "100%", "height": "100%", "object-fit": "contain"}),
                ], className="modal-content-fullscreen")
            ], id="modal", size="xl"),
        ]),
        # modal for data-table after user clicked on graph
        html.Div([
            dbc.Modal([
                dbc.ModalHeader(html.H5(id='data_table')),
                dbc.ModalBody(id='data_table_content')
            ], id="data_table_modal", size="xl"),
        ]),
    ])
])

# define chart
aggregation_chart = dcc.Graph(id="aggregation_chart")

# define aggregation tab
aggregation_tab = dcc.Tab(label="Aggregation", value="aggregation_tab")

# define settings
setting = html.Div([
    dbc.Row([
        dbc.Label('Top popularity'),
        dcc.Slider(5, 20, 5, value=10, id='top_popularity_slider'),
        # allow user to slide the popularity range, default value is top 10
        dbc.Label('Chart Type'),
        dcc.Dropdown(
            ['bar chart', 'pie chart'],
            placeholder='choose your preferable chart',
            value='bar chart',
            id='chart_type'
        )
    ])
])
# define aggregation children
aggregation_children = dcc.Tab(label="Aggregation", children=[
    dbc.Row([
        dbc.Col([
            generate_filter_card(form=aggregation_form),
            generate_settings_card(settings=setting),
            info_card
        ], width=2),

        dbc.Col([
            dbc.Card(
                dbc.CardBody(
                    dcc.Loading(
                        type="default",
                        children=[
                            aggregation_chart,
                            dbc.CardBody(
                                id='column_description_aggregation',
                                children='',
                            style={'background-color': 'lightgray'}
                            )
                        ]
                    )
                ),
                style={
                    'margin': '10px', 
                    'box-shadow': 'rgba(0,0,0,0.35) 0px 5px 5px'
                }
            ),
        ], id='diagram_display', width=10),

    ])
])
