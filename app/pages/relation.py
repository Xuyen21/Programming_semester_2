"""
This module is responsible for the relations tab of the DBLP Dashboard.

Created by: Silvan Wiedmer
Created at: 1.5.2023
"""
import logging

# https://github.com/jimmybow/visdcc
from visdcc import Network
import pandas as pd
from dash import html, dcc, Input, Output, dash, State
import dash_bootstrap_components as dbc

# modules
from modules.postgres import author_relations, school_relations, paper_date_title, paper_authors, paper_schools
from modules.column_descriptions import get_column_description

# dashboard components
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
        relations_df = pd.DataFrame(school_relations(table, limit))
    else:
        relations_df = pd.DataFrame(author_relations(table, limit))

    # generate nodes
    unique_entries = relations_df.iloc[:, 1].unique()

    nodes: list[dict] = [{'id': author, 'label': author, 'color': '#79a9d1'} for author in unique_entries]

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
    dbc.Col(dbc.Card(
        dbc.CardBody(
            dcc.Loading(
                type = "default",
                children = [relation_chart, dbc.CardBody(id='column_description_relation', children='', style={'background-color': 'lightgray'})],
            ),
        ),
    ), width=10)
]

# define relation_callback
def relation_callback(app):
    @app.callback(
        Output("relation_network", "data"),
        Output("column_description_relation", "children"),
        Input("relation_attribute_dropdown", "value"),
        Input("relation_dropdown", "value"),
        Input("relation_limit_slider", "value")
    )
    def draw_relation_network(attribute: str, table: str, limit: int):
        if attribute is None or table is None or limit is None:
            return dash.no_update, dash.no_update

        return generate_network_relations(attribute, table, limit), get_column_description(attribute)

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
        date_title: list[tuple] = paper_date_title(nodes[0])
        authors: list[str] = [author[0] for author in paper_authors(nodes[0])]
        schools: list[str] = [school[0] for school in paper_schools(nodes[0])]

        return not is_open, dbc.Row([
            dbc.Label(f'Date: {date_title[0][0]}'),
            dbc.Label(f'Authors: {", ".join(authors)}'),
            dbc.Label(f'Schools: {", ".join(schools)}'),
        ]), dbc.Label(date_title[0][1])
