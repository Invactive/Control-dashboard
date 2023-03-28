# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json


app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

with open('DATA.json') as json_file:
    DATA = json.load(json_file)

df = pd.DataFrame(dict(
    x=DATA["t"],
    y=DATA["v"]
))
fig = px.line(df, x="x", y="y", title="Position x in time t")

df2 = pd.DataFrame(dict(
    x=DATA["t"],
    y=DATA["x"]
))
fig2 = px.line(df2, x="x", y="y", title="Position x in time t")

df3 = pd.DataFrame(dict(
    x=DATA["t"],
    y=DATA["e"]
))
fig3 = px.line(df3, x="x", y="y", title="Position x in time t")

df4 = pd.DataFrame(dict(
    x=DATA["t"],
    y=DATA["u"]
))
fig4 = px.line(df4, x="x", y="y", title="Position x in time t")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),



    dbc.Card(
        dbc.CardBody([
            dcc.Graph(
                id='example-graph',
                figure=fig
            ),
        ])
    ),


    dcc.Graph(
        id='example-graph2',
        figure=fig2
    ),

    dcc.Graph(
        id='example-graph3',
        figure=fig3
    ),

    dcc.Graph(
        id='example-graph4',
        figure=fig4
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
