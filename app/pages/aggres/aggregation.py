from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

from components.filter_card import generate_filter_card
from components.settings_card import generate_settings_card
from components.info_card import info_card

# define form
aggregation_form = html.Div([
    dbc.Row([
        dbc.Label("Tabelle"),
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
                    html.Img(src='/assets/word_clouds.png',
                             style={"width": "100%", "height": "100%", "object-fit": "contain"}),
                ], className="modal-content-fullscreen"),

                dbc.ModalFooter(
                    dbc.Button("Close", id="close-button", className="ml-auto")
                ),
            ], id="modal", size="xl"),
        ]),
        html.Div([
            dbc.Modal([
                dbc.ModalHeader(html.H5(id='data_table')),
                dbc.ModalBody(id='data_table_content'),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-data-table-btn", className="ml-auto")
                ),
            ], id="data_table_modal", size="xl"),
        ]),
    ])
])

# define chart
aggregation_chart = dcc.Graph(id="aggregation_chart")

# define aggregation tab
aggregation_tab = dcc.Tab(label="Aggregation", value="aggregation_tab")

# define settings
setting = html.Div(children=[
    dbc.Row(
        [
            dbc.Label('Top popularity'),
            dcc.Slider(5, 20, 5, value=10, id='top_popularity_slider'),
            # allow user to slide the popularity range, default value is top 10
            dcc.Dropdown(['bar chart', 'pie chart'], placeholder='choose your preferable chart', value='bar chart',
                         style={'margin-top': 10},
                         id='chart_type')
        ]
    )

])
# define aggregation children
aggregation_children = dcc.Tab(label="Aggregation", children=[
    dbc.Row([
        dbc.Col([
            generate_filter_card(form=aggregation_form),
            generate_settings_card(settings=setting),
            info_card
        ], width=2),

        dbc.Col(
            [dbc.Card(
                children=[dbc.CardBody(id='chart_content', children=''),  # show content of a particular column
                          ]),

                dbc.Card(
                    dbc.CardBody(dcc.Loading(
                        type="default",
                        children=aggregation_chart
                    )
                    )
                ),
            ], id='diagram_display', width=10),

    ])
])
