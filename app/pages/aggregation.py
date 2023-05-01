from dash import dcc, html
import dash_bootstrap_components as dbc

# define form
aggregation_form = html.Div([
    dbc.Row([
        dbc.Label("Tabelle"),
        dcc.Dropdown(
            ["author", "editor", "pages", "publisher", "school", "year"],
            placeholder="Tabelle auswählen",
            id = "tabelle_dropdown"
        )
    ])
])

# define chart
aggregation_chart = dcc.Graph(id="aggregation_chart")