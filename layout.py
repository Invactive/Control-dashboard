from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
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
                        title={
                            'text': '<b>' + f_title + '</b>',
                            'x': 0.5,
                            'y': 0.95,
                            'xanchor': 'center',
                            'yanchor': 'top',
                            'font': {
                                'size': 20  # Change the font weight to 'bold'
                            }
                        }
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


def drawParams(controller: str):
    if controller == "PID":
        return html.Div([html.H2("Controller Parameters", style={'textAlign': 'center'}),
                        "Parameter Kp: ",
                         dcc.Input(
            id="inpParKp",
            placeholder='Enter a value...',
            type='number',
            value='',
            style={'marginRight': '10px', 'width': '150px'}
        ),
            html.Br(),
            "Parameter Ti: ",
            dcc.Input(
            id="inpParTi",
            placeholder='Enter a value...',
            type='number',
            value='',
            style={'marginRight': '10px', 'width': '150px'}
        ),
            html.Br(),
            "Parameter Td: ",
            dcc.Input(
            id="inpParTd",
            placeholder='Enter a value...',
            type='number',
            value='',
            style={'marginRight': '10px', 'width': '150px'}
        ),
            html.Br(),
            html.Br(),
            html.Div(
            html.Button("Apply and Generate Graphs",
                        id="apply-button"),
            style={"text-align": "center"}
        ),
            html.Div(id='outputPar1', style={
                'textAlign': 'center'}
        ),
            html.Div(id='outputPar2', style={
                'textAlign': 'center'}
        ),
            html.Div(id='outputPar3', style={
                'textAlign': 'center'}
        )
        ])
    if controller == "FUZZY":
        return html.Div([html.H2("Controller Parameters", style={'textAlign': 'center'}),
                        html.H3("FUZZY PH", style={'textAlign': 'center'})])


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


def create_layout():
    layout = html.Div([
        dcc.Location(id='url', refresh=True),
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
                        html.Div([html.H2("Controllers", style={'textAlign': 'center'}),
                                  dcc.RadioItems(
                            style={'textAlign': 'center'},
                            id='controllersRB',
                            options=[
                                {'label': ' PID Controller', 'value': 'PID'},
                                {'label': ' Fuzzy Logic Controller', 'value': 'FUZZY'}
                            ]
                        ),
                        ], style={'textAlign': 'left'}),
                        html.Br(),
                        html.Br(),
                        html.Div(id="controllerParams", style={
                                 'textAlign': 'center'}),
                    ], width=4, align='start'),
                    dbc.Col([
                        drawFigure(df, "Speed v in time t")
                    ], width=4),
                    dbc.Col([
                        drawFigure(df2, "Position x in time t")
                    ], width=4),
                ]),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                    ], width=4, align='start'),
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
    return layout
