from dash import dcc, html
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
        )
    ])
])

# define chart
aggregation_chart = dcc.Graph(id="aggregation_chart")

# define aggregation tab
aggregation_tab = dcc.Tab(label="Aggregation", children=[
    dbc.Row([
        dbc.Col([
            generate_filter_card(form=aggregation_form),
            generate_settings_card(html.P("Not Implemented")),
            info_card
        ], width=2),
        dbc.Col(
            [dbc.Card(
                [dbc.CardBody(id='chart_content', children=''), # show content of a particular column
                 dbc.CardBody(children=[
                     html.P(f'Drag the slider to see the top popularity'),
                     dcc.RangeSlider(0, 50, value=[0, 10], allowCross=False,
                                     tooltip={"placement": "bottom", "always_visible": True},
                                     id='top_popularity_slider')
                 ])]), # allow user to slide the popularity range, default value is top 10
                dcc.Dropdown(['bar chart', 'pie chart'], placeholder='choose your preferable chart', value='bar chart',
                             style={'margin-left': 5, "width": "18rem"}, id='chart_type'), # different type of charts
                dbc.Card(
                    dbc.CardBody(dcc.Loading(
                        type="default",
                        children=aggregation_chart
                    )
                    )
                )], width=10)
    ])
])
