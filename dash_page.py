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
                        id='controllersRB',
                        options=[
                            {'label': 'Controller 1', 'value': 'c1'},
                            {'label': 'Controller 2', 'value': 'c2'},
                            {'label': 'Controller 3', 'value': 'c3'}
                        ]
                    ),
                        html.Div(id='outputCon', style={'textAlign': 'center'})
                    ], style={'textAlign': 'left'})
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
                    html.Div([html.H2("Controller Parameters", style={'textAlign': 'center'}),
                              "Parameter 1: ",
                              dcc.Input(
                        id="inpPar1",
                        placeholder='Enter a value...',
                        type='number',
                        value='',
                        style={'marginRight': '10px'}
                    ),
                        html.Br(),
                        "Parameter 2: ",
                        dcc.Input(
                        id="inpPar2",
                        placeholder='Enter a value...',
                        type='number',
                        value='',
                        style={'marginRight': '10px'}
                    ),
                        html.Br(),
                        "Parameter 3: ",
                        dcc.Input(
                        id="inpPar3",
                        placeholder='Enter a value...',
                        type='number',
                        value='',
                        style={'marginRight': '10px'}
                    ),
                        html.Div(id='outputPar1', style={
                                 'textAlign': 'center'}
                                 ),
                        html.Div(id='outputPar2', style={
                            'textAlign': 'center'}
                    ),
                        html.Div(id='outputPar3', style={
                            'textAlign': 'center'}
                    ),

                    ])
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


@app.callback(
    Output('outputCon', 'children'),
    [Input('controllersRB', 'value')]
)
def update_output(value):
    return f'You have selected {value}'


@app.callback(
    Output('outputPar1', 'children'),
    [Input('inpPar1', 'value')]
)
def update_output(value):
    return f'Param 1 value: {value}'


@app.callback(
    Output('outputPar2', 'children'),
    [Input('inpPar2', 'value')]
)
def update_output(value):
    return f'Param 2 value: {value}'


@app.callback(
    Output('outputPar3', 'children'),
    [Input('inpPar3', 'value')]
)
def update_output(value):
    return f'Param 3 value: {value}'


# Run app
if __name__ == "__main__":
    app.run_server(debug=True)
