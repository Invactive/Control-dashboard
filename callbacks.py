from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import layout
import dash
import importlib
import plotly.express as px
import pandas as pd

importlib.reload(layout)


def get_callbacks(app):
    @app.callback(
        Output('controllerParams', 'children'),
        [Input('controllersRB', 'value')]
    )
    def update_output(value):
        return layout.drawControllerParams(value)

    @app.callback(
        Output('outputPar1', 'children'),
        [Input('inpParKp', 'value')]
    )
    def update_output(value):
        return f'Param 1 value: {value}'

    @app.callback(
        Output('outputPar2', 'children'),
        [Input('inpParTi', 'value')]
    )
    def update_output(value):
        return f'Param 2 value: {value}'

    @app.callback(
        Output('outputPar3', 'children'),
        [Input('inpParTd', 'value')]
    )
    def update_output(value):
        return f'Param 3 value: {value}'

    @app.callback(
        Output("inpParamKp", "value"),
        Output("sliderKp", "value"),
        Input("inpParamKp", "value"),
        Input("sliderKp", "value")

    )
    def update_values(inp_value, slider_value):
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        value = inp_value if trigger_id == "inpParamKp" else slider_value
        return value, value

    @app.callback(
        Output("inpParamTi", "value"),
        Output("sliderTi", "value"),
        Input("inpParamTi", "value"),
        Input("sliderTi", "value")

    )
    def update_values(inp_value, slider_value):
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        value = inp_value if trigger_id == "inpParamTi" else slider_value
        return value, value

    @app.callback(
        Output("inpParamTd", "value"),
        Output("sliderTd", "value"),
        Input("inpParamTd", "value"),
        Input("sliderTd", "value")

    )
    def update_values(inp_value, slider_value):
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        value = inp_value if trigger_id == "inpParamTd" else slider_value
        return value, value

    @app.callback(
        [Output("graph0", "figure"),
         Output("graph1", "figure"),
         Output("graph2", "figure"),
         Output("graph3", "figure")],
        Input('clear-button', 'n_clicks')
    )
    def clear_graphs(n_clicks):
        if n_clicks is None:
            raise PreventUpdate
        else:
            return (px.line().update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                title={
                    'text': '<b>' + "Speed v in time t" + '</b>',
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
            ),
                px.line().update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                title={
                    'text': '<b>' + "Position x in time t" + '</b>',
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
            ),
                px.line().update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                title={
                    'text': '<b>' + "Error e in time t" + '</b>',
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
            ),
                px.line().update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                title={
                    'text': '<b>' + "Control signal u in time t" + '</b>',
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
