from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import json
import pandas as pd


def drawSlider(text: str):
    return html.Div(
        className="row-container-" + text,
        children=[
            html.Div(text + ":",
                     style={"margin-top": "-5px",
                            "width": "25px"}),
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


def drawFigure(df: pd.DataFrame, f_title: str, x_label: str, y_label: str):
    return px.line(df, x=df.columns[0], y=df.columns[1], title=f_title,
                   labels={df.columns[0]: x_label, df.columns[1]: y_label}
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


def drawMainHeader(text: str):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2(text),
                ], style={'textAlign': 'center'})
            ])
        ),
    ])


def drawSimParams():
    return html.Div([html.H2("Simulation Parameters",
                             style={'textAlign': 'center'}
                             ),
                     dbc.Row(
        className="row-container-Sim",
        children=[
            html.Div("Simulation Time [s]" + ":",
                     style={"margin-top": "-5px",
                            "width": "150px"}),
            dcc.Slider(
                id="sliderSimTime",
                className="sliderSim",
                min=0,
                max=1000,
                value=0,
                step=1,
                marks=None,
                tooltip={"placement": "bottom",
                         "always_visible": True},
            ),
            dcc.Input(
                id="inpParamSimTime",
                className="inputBox",
                placeholder='Enter a value...',
                type='number',
                value=0,
                style={"margin-top": "-5px"},
            ),

        ]),
    ])


def drawButtons():
    return html.Div(
        className="btns-container",
        children=[
            html.Button("Clear Graphs",
                        id="clear-button",
                        className="btn"),
            html.Button("Update Graphs",
                        id="apply-button",
                        className="btn"),
        ])


def drawControllerParams(controller: str):
    layout = None
    if controller == "P":
        layout = html.Div([html.H2("Controller Parameters",
                                   style={'textAlign': 'center'}
                                   ),
                           drawSlider("Kp"),
                           ])
    if controller == "PI":
        layout = html.Div([html.H2("Controller Parameters",
                                   style={'textAlign': 'center'}
                                   ),
                           drawSlider("Kp"),
                           html.Br(),
                           drawSlider("Ti"),
                           ])
    if controller == "PID":
        layout = html.Div([html.H2("Controller Parameters",
                                   style={'textAlign': 'center'}
                                   ),
                           drawSlider("Kp"),
                           html.Br(),
                           drawSlider("Ti"),
                           html.Br(),
                           drawSlider("Td"),
                           ])
    if controller == "FUZZY":
        layout = html.Div([html.H2("Controller Parameters", style={'textAlign': 'center'}),
                           html.H3("FUZZY PH", style={'textAlign': 'center'})])

    if layout != None:
        return layout, drawButtons()


def drawModelParams():
    return html.Div([html.H2("Model Parameters",
                             style={'textAlign': 'center'}
                             ),
                     html.Div(
        className="row-container-Sim-Tp",
        children=[
            html.Div("Model Param PH" + ":",
                     style={"margin-top": "-5px",
                            "width": "150px"}),
            dcc.Slider(
                id="sliderModelTime",
                className="sliderSim",
                min=0,
                max=1000,
                value=0,
                step=1,
                marks=None,
                tooltip={"placement": "bottom",
                         "always_visible": True},
            ),
            dcc.Input(
                id="inpParamModelTime",
                className="inputBox",
                placeholder='Enter a value...',
                type='number',
                value=0,
                style={"margin-top": "-5px"},
            ),
        ]),
    ])


# Data
with open('DATA.json') as json_file:
    DATA = json.load(json_file)

df0 = pd.DataFrame(dict(
    x=DATA["t"],
    y=DATA["v"]
))
# fig = px.line(df0, x="x", y="y", title="Position x in time t")

df1 = pd.DataFrame(dict(
    x=DATA["t"],
    y=DATA["x"]
))
# fig1 = px.line(df1, x="x", y="y", title="Position x in time t")

df2 = pd.DataFrame(dict(
    x=DATA["t"],
    y=DATA["e"]
))
# fig2 = px.line(df1, x="x", y="y", title="Position x in time t")

df3 = pd.DataFrame(dict(
    x=DATA["t"],
    y=DATA["u"]
))
# fig3 = px.line(df3, x="x", y="y", title="Position x in time t")


def create_layout():
    layout = html.Div([
        dcc.Location(id='url', refresh=True),
        dbc.Card(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        drawMainHeader("Control Panel")
                    ], width=12),
                ], align='center'),
                dbc.Row(className="params-container",
                        children=[
                            dbc.Col([
                                drawSimParams(),
                            ], width=4),
                            dbc.Col([
                                html.Div([html.H2("Controllers", style={'textAlign': 'center'}),
                                          dcc.RadioItems(
                                    style={'textAlign': 'center'},
                                    id='controllersRB',
                                    options=[
                                        {'label': ' P Controller', 'value': 'P'},
                                        {'label': ' PI Controller', 'value': 'PI'},
                                        {'label': ' PID Controller', 'value': 'PID'},
                                        {'label': ' Fuzzy Logic Controller',
                                            'value': 'FUZZY'}
                                    ]
                                ),
                                ], style={'textAlign': 'left'}),
                                html.Br(),
                                html.Div(id="controllerParams", style={
                                    'textAlign': 'center'}),
                            ], width=4),
                            dbc.Col([
                                drawModelParams(),
                            ], width=4),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Card(
                                        dbc.CardBody([
                                            dcc.Graph(
                                                id="graph0",
                                                figure=drawFigure(df=pd.DataFrame(
                                                    {"x": [], "y": []}),
                                                    f_title="Speed v in time t",
                                                    x_label="Time [s]",
                                                    y_label="Speed [undefined]")
                                            )
                                        ])
                                    ),
                                ], width=3),
                                dbc.Col([
                                    dbc.Card(
                                        dbc.CardBody([
                                            dcc.Graph(
                                                id="graph1",
                                                figure=drawFigure(df=pd.DataFrame(
                                                    {"x": [], "y": []}),
                                                    f_title="Position x in time t",
                                                    x_label="Time [s]",
                                                    y_label="Position [undefined]")
                                            )
                                        ])
                                    ),
                                ], width=3),
                                dbc.Col([
                                    dbc.Card(
                                        dbc.CardBody([
                                            dcc.Graph(
                                                id="graph2",
                                                figure=drawFigure(df=pd.DataFrame(
                                                    {"x": [], "y": []}),
                                                    f_title="Error e in time t",
                                                    x_label="Time [s]",
                                                    y_label="Error [undefined]")
                                            )
                                        ])
                                    ),
                                ], width=3),
                                dbc.Col([
                                    dbc.Card(
                                        dbc.CardBody([
                                            dcc.Graph(
                                                id="graph3",
                                                figure=drawFigure(df=pd.DataFrame(
                                                    {"x": [], "y": []}),
                                                    f_title="Control signal u in time t",
                                                    x_label="Time [s]",
                                                    y_label="Control signal [undefined]")
                                            )
                                        ])
                                    ),
                                ], width=3),
                            ], align='center'),
                        ]),
                html.Br(),
            ]), color='dark'
        )
    ])
    return layout
