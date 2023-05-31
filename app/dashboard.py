"""
This it the main Python file of the DBLP Dashboard.
It creates the Dash instance and loads all the required resources.
"""
import logging
from dash import dcc, Dash, html, Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_components.themes import BOOTSTRAP

from flask_caching import Cache

from pages.aggres.aggregation import aggregation_children, aggregation_tab
from pages.aggres.aggres_rendering import aggres_render
from pages.relation import relation_tab, relation_children, relation_callback
from pages.timespan import timespan_tab, timespan_children, timespan_callback

# logging configuration
# https://stackoverflow.com/questions/73882299/python-logging-messages-not-showing-up-due-to-imports
logging.basicConfig(
    format='%(levelname)s : [%(filename)s:%(lineno)d] : %(message)s',
    level=logging.ERROR,
    force=True # needed due to override of logging.debug
)
logging.getLogger(__name__)

# available tabs
TABS: dict = {
    "aggregation_tab": aggregation_children,
    "relation_tab": relation_children,
    "timespan_tab": timespan_children
}

app_layout = dcc.Tabs([
    aggregation_tab,
    relation_tab,
    timespan_tab
], id="tabs", value="aggregation_tab")

app = Dash(
    name = "DBLP Dashboard",
    title = "Welcome to DBLP",
    external_stylesheets=[BOOTSTRAP]
)

# cache configuration
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': './.cache'
})

app.layout = html.Div(
    className="app-div",
    children=[
        app_layout,
        dbc.Row(id="content")
    ]
)

# tab callback
@app.callback(
    Output('content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab_name: str) -> dcc.Tab:
    """
    This function renders the required Tab.
    Parameters:
    - tab_name: str => Name of the tab to load
    Return:
    - dcc.Tab => The tab to load
    """
    return TABS.get(tab_name, aggregation_children)

if __name__ == '__main__':
    # initialize callbacks from external files
    aggres_render(app, cache, 3600)
    relation_callback(app, cache, 3600)
    timespan_callback(app, cache, 3600)

    # start app
    app.run(debug=False)
