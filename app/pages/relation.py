"""
This module is responsible for the relations tab of the DBLP Dashboard.

Created by: Silvan Wiedmer
Created at: 1.5.2023
"""
import visdcc
import pandas as pd
from itertools import combinations
from dash import html, dcc
import dash_bootstrap_components as dbc

from modules.postgres import author_relations

from components.filter_card import generate_filter_card
from components.settings_card import generate_settings_card
from components.info_card import info_card

# define form
relation_form = html.Div([
    dbc.Row([
        dbc.Label("Tabelle"),
        dcc.Dropdown(
            ["phdthesis", "mastersthesis"],
            value = "phdthesis",
            id = "relation_dropdown"
        )
    ])
])

# define chart
relation_chart = visdcc.Network(id = 'relation_network', 
    options = dict(height= '600px', width= '100%'),
    data = {
        'nodes': [],
        'edges': []
    }
)

def generate_network_relations() -> dict:
    """
    Generate the Relationship graph from the database.

    Returns:
    - dict: Relationship graph data
    """
    author_relations_df = pd.DataFrame(author_relations())

    # generate nodes
    unique_authors = author_relations_df.iloc[:, 1].unique()

    nodes: list[dict] = [{'id': author, 'label': author} for author in unique_authors]

    # generate edges
    unique_entries = author_relations_df.iloc[:, 0].unique()

    edges = []

    for entry in unique_entries:
        authors = author_relations_df[author_relations_df.iloc[:, 0] == entry].iloc[:, 1]
        for author_permutations in combinations(authors, 2):
            edges.append({
                'id': f'{entry}_{author_permutations[0]}_{author_permutations[1]}',
                'from': author_permutations[0],
                'to': author_permutations[1]
            })

    # build data dict
    data: dict = {
        'nodes': nodes,
        'edges': edges
    }
    return data

relation_tab = dcc.Tab(label = "Relation", children = [
    dbc.Row([
        dbc.Col([
            generate_filter_card(relation_form),
            generate_settings_card(html.P("Not Implemented")),
            info_card
        ], width=2),
        dbc.Col(dbc.Card(
            dbc.CardBody(dcc.Loading(
                type = "default",
                children = relation_chart)
            )
        ), width=10)
    ])
])
