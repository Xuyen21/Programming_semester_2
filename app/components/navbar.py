from dash import dcc
import dash_bootstrap_components as dbc

navbar_dropdown = dcc.Dropdown(
    ["Aggregation", "Relation", "Timespan"],
    "Aggregation",
    id = "navbar_dropdown"
)

# define navbar
navbar = dbc.NavbarSimple(
    brand = "Welcome to DBLP",
    color = "primary",
    dark = True
)
