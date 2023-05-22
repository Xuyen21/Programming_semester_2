import logging
from dash import dcc, Dash, html, Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_components.themes import BOOTSTRAP

from pages.aggres.aggregation import aggregation_tab, aggregation_children
from pages.aggres.aggres_rendering import aggres_render
from pages.relation import relation_tab, relation_children, relation_callback
from pages.timespan import timespan_tab, timespan_children, timespan_callback


# logging configuration
logging.basicConfig(
    format='%(levelname)s : [%(filename)s:%(lineno)d] : %(message)s',
    level=logging.ERROR
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
def render_content(tab_name: str):
    return TABS.get(tab_name, aggregation_children)

if __name__ == '__main__':
    # initialize callbacks from external files
    aggres_render(app)
    relation_callback(app)
    timespan_callback(app)

    # start app
    app.run(debug=True)
