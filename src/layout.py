from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go


def drawSlider(text: str):
    return html.Div(
        className="row-container-" + text,
        children=[
            html.Div(text,
                     style={"margin-top": "-5px",
                            "width": "25px"}),
            dcc.Slider(
                id="slider" + text,
                className="slider",
                min=0,
                max=500,
                value=0,
                step=0.1,
                marks=None,
                tooltip={"placement": "bottom",
                         "always_visible": True}
            ),
            dcc.Input(
                id="inpParam" + text,
                className="inputBox",
                type='number',
                value=0,
                style={"margin-top": "-5px"},
            ),
        ])


def drawFigures(df_list: list, f_title: str, x_label: str, y_label: str):
    layout = go.Layout(
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
        xaxis={'title': x_label},
        yaxis={'title': y_label},
        modebar={
            'orientation': 'v',
            'bgcolor': 'rgba(0,0,0,0.5)'
        }
    )
    lines = []
    for i in range(len(df_list)):
        if i == 0:
            if df_list[1].empty:
                line_color = 'royalblue'
            else:
                line_color = 'grey'
        elif i == 1:
            line_color = 'royalblue'
        lines.append(go.Scatter(x=df_list[i]["x"],
                                y=df_list[i]["y"],
                                line=dict(color=line_color),
                                name="Old trace" if i == 0 else "New Trace"))
    fig = go.Figure(data=lines, layout=layout)
    return fig


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
        className="row-container-Sim-Tp",
        children=[
            html.Div("Simulation Time [s]",
                     style={"margin-top": "-5px",
                            "width": "110px",
                            "margin-right": "-20px"}),
            dcc.Slider(
                id="sliderSimTime",
                className="sliderSim",
                min=0,
                max=1000,
                value=10,
                step=0.1,
                marks=None,
                tooltip={"placement": "bottom",
                         "always_visible": True},
            ),
            dcc.Input(
                id="inpParamSimTime",
                className="inputBox",
                placeholder='Enter a value...',
                type='number',
                min=0,
                max=1000,
                value=10,
                step=0.1,
                style={"margin-top": "-5px"},
            ),
        ]),
        dbc.Row(
        className="row-container-Sim-Tp",
        children=[
            html.Div("Sampling Time [s]",
                     style={"margin-top": "-5px",
                            "width": "110px",
                            "margin-right": "-20px"}),
            dcc.Slider(
                id="sliderSimTp",
                className="sliderSim",
                min=0.0,
                max=0.001,
                value=0.0001,
                step=0.00001,
                marks=None,
                tooltip={"placement": "bottom",
                         "always_visible": True},
            ),
            dcc.Input(
                id="inpParamSimTp",
                className="inputBox",
                type='number',
                min=0.0,
                max=0.001,
                value=0.0001,
                step=0.00001,
                style={"margin-top": "-5px"},
            ),
        ]),
        dbc.Row(
        className="row-container-Sim-Tp",
        children=[
            html.Div("Set Point [m]",
                     style={"margin-top": "-5px",
                            "width": "110px",
                            "margin-right": "-20px"}),
            dcc.Slider(
                id="sliderSimSP",
                className="sliderSim",
                min=0.0001,
                max=0.0105,
                value=0.005,
                step=0.0001,
                marks=None,
                tooltip={"placement": "bottom",
                         "always_visible": True},
            ),
            dcc.Input(
                id="inpParamSimSP",
                className="inputBox",
                type='number',
                min=0.0001,
                max=0.0105,
                value=0.005,
                step=0.0001,
                style={"margin-top": "-5px"},
            ),
        ],
        style={"margin-bottom": "20px"}),
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
            html.Div("Ball Mass [kg]",
                     style={"margin-top": "-5px",
                            "width": "100px"}),
            dcc.Slider(
                id="sliderModelMass",
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
                id="inpParamModelMass",
                className="inputBox",
                type='number',
                value=0,
                style={"margin-top": "-5px"},
            ),
        ]),
    ])


def create_layout():
    layout = html.Div([
        dcc.Location(id='url', refresh=True),
        dbc.Card(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        drawMainHeader("Control Dashboard")
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
                                                figure=drawFigures(df_list=[
                                                    pd.DataFrame(
                                                        {"x": [], "y": []}),
                                                    pd.DataFrame({"x": [], "y": []})],
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
                                                figure=drawFigures(df_list=[
                                                    pd.DataFrame(
                                                        {"x": [], "y": []}),
                                                    pd.DataFrame({"x": [], "y": []})],
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
                                                figure=drawFigures(df_list=[
                                                    pd.DataFrame(
                                                        {"x": [], "y": []}),
                                                    pd.DataFrame({"x": [], "y": []})],
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
                                                figure=drawFigures(df_list=[
                                                    pd.DataFrame(
                                                        {"x": [], "y": []}),
                                                    pd.DataFrame({"x": [], "y": []})],
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
        ),
        html.Div(id="hidden-div",
                 style={"display": "none"}),
        html.Div([
            html.Button('Show Data', id='show-button'),
            html.Div(id='data-output')
        ], style={"display": "none"})
    ])
    return layout
