from dash.dependencies import Input, Output
import layout
import dash


def get_callbacks(app):
    @app.callback(
        Output('controllerParams', 'children'),
        [Input('controllersRB', 'value')]
    )
    def update_output(value):
        return layout.drawParams(value)

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
