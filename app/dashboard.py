import logging
import pandas as pd
import plotly.express as px
from dash import dcc, Dash, html, Input, Output, dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components.themes import BOOTSTRAP

from components.navbar import navbar

from modules.postgres import sql_from_dropdown, papers_per_month

from pages.aggres.aggregation import aggregation_tab
from pages.aggres.aggres_rendering import aggres_render
from pages.relation import relation_tab, generate_network_relations
from pages.timespan import timespan_tab

# logging configuration
logging.basicConfig(
    format='%(levelname)s : [%(filename)s:%(lineno)d] : %(message)s',
    level=logging.DEBUG
)
logging.getLogger(__name__)

app_layout = dcc.Tabs([
    aggregation_tab,
    relation_tab,
    timespan_tab
])

def create_layout() -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            navbar,
            app_layout
        ]
    )

app = Dash(
    name = "DBLP Dashboard",
    title = "Welcome to DBLP",
    external_stylesheets=[BOOTSTRAP]
)
app.layout = create_layout()

# aggregation callback
aggres_render(app)

# relation callback
@app.callback(
    Output("relation_network", "data"),
    Input("relation_dropdown", "value"),
)
def draw_relation_network(table: str):
    if table is None:
        return dash.no_update

    return generate_network_relations(table)

# timespan callback
@app.callback(
    Output("timespan_chart", "figure"),
    Input("year_dropdown", "value")
)
def draw_timespan(selected_year: str):
    if not selected_year:
        selected_year = "2022"

    df = papers_per_month(selected_year)

    fig = px.bar(df, x='month', y='count', color='entryType', barmode='group')
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Number of publications",
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)
