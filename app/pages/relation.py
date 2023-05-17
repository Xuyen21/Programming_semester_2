"""
This module is responsible for the relations tab of the DBLP Dashboard.

Created by: Silvan Wiedmer
Created at: 1.5.2023
"""
import logging
from itertools import combinations
from visdcc import Network
import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc

# modules
from modules.postgres import author_relations, school_relations

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
    options = dict(height= '600px', width= '100%'),
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
    try:
        unique_entries = relations_df.iloc[:, 1].unique()
    except IndexError as e:
        logging.error(relations_df[:, 1].unique())

    nodes: list[dict] = [{'id': author, 'label': author} for author in unique_entries]

    # generate edges
    unique_entries = relations_df.iloc[:, 0].unique()

    edges = []

    for entry in unique_entries:
        authors = relations_df[relations_df.iloc[:, 0] == entry].iloc[:, 1]
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
            generate_settings_card(relation_settings),
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
