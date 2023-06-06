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
        Output("graph0", "figure"),
        Output("graph1", "figure"),
        Output("graph2", "figure"),
        Output("graph3", "figure"),
        Input('clear-button', 'n_clicks'),
        Input('apply-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def update_graphs(btn_clear, btn_apply):
        triggered_id = dash.ctx.triggered_id
        if triggered_id == 'clear-button':
            return clear_graphs()
        elif triggered_id == 'apply-button':
            return draw_graphs()

    def clear_graphs():
        return (layout.drawFigure(
            df=pd.DataFrame(
                {"x": [], "y": []}),
            f_title="Speed v in time t",
            x_label="Time [s]",
            y_label="Speed [undefined]"
        ),
            layout.drawFigure(
            df=pd.DataFrame(
                {"x": [], "y": []}),
            f_title="Position x in time t",
            x_label="Time [s]",
            y_label="Position [undefined]"
        ),
            layout.drawFigure(
            df=pd.DataFrame(
                {"x": [], "y": []}),
            f_title="Error e in time t",
            x_label="Time [s]",
            y_label="Error [undefined]"
        ),
            layout.drawFigure(
            df=pd.DataFrame(
                {"x": [], "y": []}),
            f_title="Control signal u in time t",
            x_label="Time [s]",
            y_label="Control signal [undefined]"
        )
        )

    def draw_graphs():
        return (layout.drawFigure(
            df=layout.df0,
            f_title="Speed v in time t",
            x_label="Time [s]",
            y_label="Speed [undefined]"
        ),
            layout.drawFigure(
            df=layout.df1,
            f_title="Position x in time t",
            x_label="Time [s]",
            y_label="Position [undefined]"
        ),
            layout.drawFigure(
            df=layout.df2,
            f_title="Error e in time t",
            x_label="Time [s]",
            y_label="Error [undefined]"
        ),
            layout.drawFigure(
            df=layout.df3,
            f_title="Control signal u in time t",
            x_label="Time [s]",
            y_label="Control signal [undefined]"
        )
        )
