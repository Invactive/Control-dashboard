from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import json
import pandas as pd


def drawFigure(df: pd.DataFrame, f_title: str):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.line(df, x="x", y="y", title=f_title
                                   ).update_layout(
                        template='plotly_dark',
                        plot_bgcolor='rgba(0, 0, 0, 0)',
                        paper_bgcolor='rgba(0, 0, 0, 0)',
                    )
                )
            ])
        ),
    ])


def drawText(text: str):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2(text),
                ], style={'textAlign': 'center'})
            ])
        ),
    ])


# Data
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

# Build App
app = Dash(external_stylesheets=[dbc.themes.SLATE])

app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    drawText("Control Panel")
                ], width=12),
            ], align='center'),
            html.Br(),
            dbc.Row([
                dbc.Col([

                ], width=4),
                dbc.Col([
                    drawFigure(df, "Speed v in time t")
                ], width=4),
                dbc.Col([
                    drawFigure(df2, "Position x in time t")
                ], width=4),
            ], align='center'),
            html.Br(),
            dbc.Row([
                dbc.Col([

                ], width=4),
                dbc.Col([
                    drawFigure(df3, "Error e in time t")
                ], width=4),
                dbc.Col([
                    drawFigure(df4, "Control signal u in time t")
                ], width=4),
            ], align='center'),
        ]), color='dark'
    )
])

# Run app and display result inline in the notebook
app.run_server()
