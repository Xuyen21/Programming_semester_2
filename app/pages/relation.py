"""
This module is responsible for the relations tab of the DBLP Dashboard.

Created by: Silvan Wiedmer
Created at: 1.5.2023
"""
# https://github.com/jimmybow/visdcc
from visdcc import Network
import pandas as pd
from dash import html, dcc, Input, Output, dash, State, Dash
import dash_bootstrap_components as dbc
from flask_caching import Cache
# modules
from modules.postgres import execute_query
from modules.postgres_queries import author_relations_query, school_relations_query
from modules.postgres_queries import paper_date_title_query
from modules.postgres_queries import paper_authors_query, paper_schools_query
from modules.column_descriptions import get_column_description

# components
from components.filter_card import generate_filter_card
from components.settings_card import generate_settings_card
from components.info_card import info_card

# define form
relation_form = html.Div([
    dbc.Row([
        dbc.Label("Attribute"),
        dcc.Dropdown(
            ["author", "school"],
            value = "author",
            id = "relation_attribute_dropdown"
        ),
        dbc.Label("Table"),
        dcc.Dropdown(
            ["phdthesis", "mastersthesis"],
            value = "phdthesis",
            id = "relation_dropdown"
        )
    ])
])

relation_settings = html.Div([
    dbc.Row([
        dbc.Label("Count"),
        dcc.Slider(5,20,5, value = 10, id="relation_limit_slider")
    ])
])

# define chart
relation_chart = Network(id = 'relation_network',
    options = {'height': '600px', 'width': '100%'},
    data = {
        'nodes': [],
        'edges': []
    }
)

def generate_network_relations(attribute: str, table: str, limit: int) -> dict:
    """
    Generate the Relationship graph from the database.

    Returns:
    - dict: Relationship graph data
    """
    if attribute == "school":
        relations_df_query = school_relations_query(table, limit)
        relations_df = pd.DataFrame(execute_query(relations_df_query, 'school_relations_query'))
    else:
        relations_df_query = author_relations_query(table, limit)
        relations_df = pd.DataFrame(execute_query(relations_df_query, 'author_relations_query'))

    # generate nodes
    unique_entries = relations_df.iloc[:, 1].unique()

    nodes: list[dict] = [
        {'id': author, 'label': author, 'color': '#79a9d1'} for author in unique_entries
    ]

    # generate edges
    unique_entries = relations_df.iloc[:, 0].unique()

    edges = []

    for entry in unique_entries:
        nodes.append({'id': entry, 'label': entry, 'color': '#7cea9c'})
        authors = relations_df[relations_df.iloc[:, 0] == entry].iloc[:, 1]
        for author in authors:
            edges.append({
                'id': f'{entry}_{author}',
                'from': entry,
                'to': author
            })

    # build data dict
    data: dict = {
        'nodes': nodes,
        'edges': edges
    }
    return data

relation_tab = dcc.Tab(label = "Relation", value="relation_tab")

# define relation_children
relation_children = [
    dbc.Col([
        generate_filter_card(relation_form),
        generate_settings_card(relation_settings),
        info_card
    ], width=2),
    dbc.Col(
        dbc.Card(
            dbc.CardBody(
                dcc.Loading(
                    type = "default",
                    children = [
                        relation_chart,
                        dbc.Modal([
                        dbc.ModalHeader(id='paper_preview_title'),
                        dbc.ModalBody(className="modal-content-fullscreen", id='paper_preview_body')
                        ], id="paper_preview", size="lg"),
                        dbc.CardBody(
                            id='column_description_relation',
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
        width=10
    )
]

# define relation_callback
def relation_callback(app: Dash, cache: Cache, cache_timeout: int = 600):
    """
    This function creates the callback for the Relation Tab.
    Parameters:
    - app: Dash => The App instance
    - cache: Cache => the cache of the Application
    - cache_timeout: int = 600 => The timeout before clearing the cache
    """
    @app.callback(
        Output("relation_network", "data"),
        Output("column_description_relation", "children"),
        Input("relation_attribute_dropdown", "value"),
        Input("relation_dropdown", "value"),
        Input("relation_limit_slider", "value")
    )
    @cache.memoize(timeout=cache_timeout)
    def draw_relation_network(attribute: str, table: str, limit: int):
        if attribute is None or table is None or limit is None:
            return dash.no_update, dash.no_update

        network_relations: dict = generate_network_relations(attribute, table, limit)
        column_descriptions: str = get_column_description(attribute)
        return network_relations, column_descriptions

    @app.callback(
        Output("paper_preview", "is_open"),
        Output("paper_preview_body", "children"),
        Output("paper_preview_title", "children"),
        Input('relation_network', 'selection'),
        State("paper_preview", "is_open"),
    )
    def toggle_paper_preview(selection: dict, is_open: bool):
        # no need to update when no selection
        if selection is None:
            return False, dash.no_update, dash.no_update

        # generate Paper Preview and show Modal
        nodes: list[str] = selection.get("nodes", None)
        if nodes is None:
            return not is_open , dash.no_update, dash.no_update

        # get data from database
        try:
            date_title_query = paper_date_title_query(nodes[0])
            date_title: list[tuple] = execute_query(date_title_query, 'paper_date_title_query')

            authors_query = paper_authors_query(nodes[0])
            authors: list[str] = [
                author[0] for author in execute_query(authors_query, 'paper_authors_query')
            ]

            schools_query = paper_schools_query(nodes[0])
            schools: list[str] = [
                school[0] for school in execute_query(schools_query, 'paper_schools_query')
            ]

            return not is_open, dbc.Row([
                dbc.Label(f'Date: {date_title[0][0]}'),
                dbc.Label(f'Authors: {", ".join(authors)}'),
                dbc.Label(f'Schools: {", ".join(schools)}'),
            ]), dbc.Label(date_title[0][1])
        except IndexError:
            return dash.no_update, dash.no_update, dash.no_update
