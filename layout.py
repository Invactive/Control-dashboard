from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import json
import pandas as pd


def drawSlider(text: str):
    return html.Div(
        className="row-container",
        children=[
            html.Div(text + ":",
                     style={"margin-top": "-5px"}),
            dcc.Slider(
                id="slider" + text,
                className="slider",
                min=0,
                max=100,
                value=0,
                step=0.1,
                marks=None,
                tooltip={"placement": "bottom",
                         "always_visible": True}
            ),
            dcc.Input(
                id="inpParam" + text,
                className="inputBox",
                placeholder='Enter a value...',
                type='number',
                value=0,
                style={"margin-top": "-5px"},
            ),
        ])


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
                            "font_color": "#aaaaaa",
                            'font': {
                                'size': 20
                            }
                        },
                        modebar={
                            'orientation': 'v',
                            'bgcolor': 'rgba(0,0,0,0.5)'
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
    if controller == "P":
        return html.Div([html.H2("Controller Parameters",
                                 style={'textAlign': 'center'}
                                 ),
                         drawSlider("Kp"),
                         html.Div(
            html.Button("Update Graphs",
                        id="apply-button",
                        className="btn"),
            style={"text-align": "center"}
        ),
            html.Div(
            html.Button("Clear Graphs",
                        id="clear-button",
                        className="btn"),
            style={"text-align": "center"}
        )
        ])
    if controller == "PI":
        return html.Div([html.H2("Controller Parameters",
                                 style={'textAlign': 'center'}
                                 ),
                         drawSlider("Kp"),
                         html.Br(),
                         drawSlider("Ti"),
                         html.Div(
            html.Button("Update Graphs",
                        id="apply-button",
                        className="btn"),
            style={"text-align": "center"}
        ),
            html.Div(
            html.Button("Clear Graphs",
                        id="clear-button",
                        className="btn"),
            style={"text-align": "center"}
        )
        ])
    if controller == "PID":
        return html.Div([html.H2("Controller Parameters",
                                 style={'textAlign': 'center'}
                                 ),
                         drawSlider("Kp"),
                         html.Br(),
                         drawSlider("Ti"),
                         html.Br(),
                         drawSlider("Td"),
                         html.Div(
            html.Button("Update Graphs",
                        id="apply-button",
                        className="btn"),
            style={"text-align": "center"}
        ),
            html.Div(
            html.Button("Clear Graphs",
                        id="clear-button",
                        className="btn"),
            style={"text-align": "center"}
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
                                {'label': ' P Controller', 'value': 'P'},
                                {'label': ' PI Controller', 'value': 'PI'},
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
