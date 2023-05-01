import pandas as pd
from dash import dcc, html
import plotly.graph_objs as go


def generate_pie_chart(app):
    # app = dash.Dash()

    data = pd.read_csv('distributionofpublicationtype.csv', sep=";")
    types = data['type'].values
    pubs = data['#Publications'].values

    pie_chart = go.Pie(labels=types, values=pubs)
    layout = go.Layout(title='My Pie Chart')
    fig = go.Figure(data=[pie_chart], layout=layout)

    diagram = html.Div([
        dcc.Graph(id='my-pie-chart', figure=fig)
    ])

    return diagram
