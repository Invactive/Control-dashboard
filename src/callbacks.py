from dash.dependencies import Input, Output
import layout
import dash
import pandas as pd
import modelPID
import modelFUZZY
import json
import os
import helpers

# importlib.reload(layout)  # for testing purposes


def get_callbacks(app):
    @app.callback(
        Output('hidden-div', 'children'),
        Input('url', 'pathname')
    )
    def page_load_callback(pathname):
        with open(helpers.DATA_OLD, 'w') as file:
            file.truncate()
        with open(helpers.DATA_NEW, 'w') as file:
            file.truncate()
        return ""

    @app.callback(
        # Callback for SimTime slider and inputBox
        Output("inpParamSimTime", "value"),
        Output("sliderSimTime", "value"),
        Input("inpParamSimTime", "value"),
        Input("sliderSimTime", "value")
    )
    def update_Sim_time(inp_value, slider_value):
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        value = inp_value if trigger_id == "inpParamSimTime" else slider_value
        modelPID.Tsim = value
        modelFUZZY.Tsim = value
        return value, value

    @app.callback(
        # Callback for Tp slider and inputBox
        Output("inpParamSimTp", "value"),
        Output("sliderSimTp", "value"),
        Input("inpParamSimTp", "value"),
        Input("sliderSimTp", "value")
    )
    def update_Tp(inp_value, slider_value):
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        value = inp_value if trigger_id == "inpParamSimTp" else slider_value
        modelPID.Tp = value
        modelFUZZY.Tp = value
        return value, value

    @app.callback(
        # Callback for SP slider and inputBox
        Output("inpParamSimSP", "value"),
        Output("sliderSimSP", "value"),
        Input("inpParamSimSP", "value"),
        Input("sliderSimSP", "value")
    )
    def update_SP(inp_value, slider_value):
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        value = inp_value if trigger_id == "inpParamSimSP" else slider_value
        modelPID.setpoint = value  # / 100.0
        modelFUZZY.setpoint = value  # / 100.0
        return value, value

    @app.callback(
        # Callback for controllers RadioButtons
        Output('controllerParams', 'children'),
        Input('controllersRB', 'value'),
        prevent_initial_call=True
    )
    def pick_Controller(value):
        helpers.PICKED_CONTROLLER = value
        return layout.drawControllerParams(value)

    @app.callback(
        # Callback for Kp slider and inputBox
        Output("inpParamKp", "value"),
        Output("sliderKp", "value"),
        Input("inpParamKp", "value"),
        Input("sliderKp", "value")

    )
    def update_Kp(inp_value, slider_value):
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        value = inp_value if trigger_id == "inpParamKp" else slider_value
        modelPID.Kp = value
        return value, value

    @app.callback(
        # Callback for Ti slider and inputBox
        Output("inpParamTi", "value"),
        Output("sliderTi", "value"),
        Input("inpParamTi", "value"),
        Input("sliderTi", "value")

    )
    def update_Ti(inp_value, slider_value):
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        value = inp_value if trigger_id == "inpParamTi" else slider_value
        modelPID.Ti = value
        return value, value

    @app.callback(
        # Callback for Td slider and inputBox
        Output("inpParamTd", "value"),
        Output("sliderTd", "value"),
        Input("inpParamTd", "value"),
        Input("sliderTd", "value")
    )
    def update_Td(inp_value, slider_value):
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        value = inp_value if trigger_id == "inpParamTd" else slider_value
        modelPID.Td = value
        return value, value

    @app.callback(
        Output('NB-output', 'children'),
        [Input('rangeSliderNegativeBig', 'value')])
    def updateNB(value):
        min = value[0]
        max = value[1]
        modelFUZZY.NB_l = min
        modelFUZZY.NB_h = max
        return value[0], value[1]

    @app.callback(
        # Callback for mass slider and inputBox
        Output("inpParamModelMass", "value"),
        Output("sliderModelMass", "value"),
        Input("inpParamModelMass", "value"),
        Input("sliderModelMass", "value")

    )
    def update_mass(inp_value, slider_value):
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        value = inp_value if trigger_id == "inpParamModelMass" else slider_value
        modelPID.m = value / 1000.0
        modelFUZZY.m = value / 1000.0
        return value, value

    @app.callback(
        # Callback for buttons
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
        with open(helpers.DATA_OLD, 'w') as file:
            file.truncate()
        with open(helpers.DATA_NEW, 'w') as file:
            file.truncate()

        empty_df = pd.DataFrame(
            {"x": [], "y": []})

        return (layout.drawFigures(
            df_list=[empty_df, empty_df],
            f_title="Speed v in time t",
            x_label="Time [s]",
            y_label="Speed [m/s]"
        ),
            layout.drawFigures(
            df_list=[empty_df, empty_df],
            f_title="Position x in time t",
            x_label="Time [s]",
            y_label="Position [m]"
        ),
            layout.drawFigures(
            df_list=[empty_df, empty_df],
            f_title="Error e in time t",
            x_label="Time [s]",
            y_label="Error [m]"
        ),
            layout.drawFigures(
            df_list=[empty_df, empty_df],
            f_title="Control signal u in time t",
            x_label="Time [s]",
            y_label="Control signal [V]"
        )
        )

    def draw_graphs():
        df_v_0 = df_x_0 = df_e_0 = df_u_0 = df_v_1 = df_x_1 = df_e_1 = df_u_1 = pd.DataFrame(
            {"x": [], "y": []})
        if os.path.getsize(helpers.DATA_NEW) == 0:
            if helpers.PICKED_CONTROLLER == "P" or "PI" or "PID":
                modelPID.generateData(mass=modelPID.m,
                                      Tsim=modelPID.Tsim,
                                      Tp=modelPID.Tp,
                                      kp=modelPID.Kp,
                                      Ti=modelPID.Ti,
                                      Td=modelPID.Td,
                                      setpoint=modelPID.setpoint,
                                      output=helpers.DATA_NEW)
                df_v_0, df_x_0, df_e_0, df_u_0 = helpers.readDATA(
                    helpers.DATA_NEW)
            if helpers.PICKED_CONTROLLER == "FUZZY":
                modelFUZZY.generateData(mass=modelFUZZY.m,
                                        Tsim=modelFUZZY.Tsim,
                                        Tp=modelFUZZY.Tp,
                                        Td=2.0,
                                        setpoint=modelFUZZY.setpoint,
                                        output=helpers.DATA_NEW)
                df_v_0, df_x_0, df_e_0, df_u_0 = helpers.readDATA(
                    helpers.DATA_NEW)
        else:
            with open(helpers.DATA_NEW, 'r+') as source_file:
                data = json.load(source_file)
                source_file.truncate()
            with open(helpers.DATA_OLD, 'w') as destination_file:
                json.dump(data, destination_file)

            if helpers.PICKED_CONTROLLER == "P" or "PI" or "PID":
                modelPID.generateData(mass=modelPID.m,
                                      Tsim=modelPID.Tsim,
                                      Tp=modelPID.Tp,
                                      kp=modelPID.Kp,
                                      Ti=modelPID.Ti,
                                      Td=modelPID.Td,
                                      setpoint=modelPID.setpoint,
                                      output=helpers.DATA_NEW)

            if helpers.PICKED_CONTROLLER == "FUZZY":
                modelFUZZY.generateData(mass=modelFUZZY.m,
                                        Tsim=modelFUZZY.Tsim,
                                        Tp=modelFUZZY.Tp,
                                        Td=2.0,
                                        setpoint=modelFUZZY.setpoint,
                                        output=helpers.DATA_NEW)

            df_v_1, df_x_1, df_e_1, df_u_1 = helpers.readDATA(
                helpers.DATA_NEW)
            df_v_0, df_x_0, df_e_0, df_u_0 = helpers.readDATA(
                helpers.DATA_OLD)

        return (layout.drawFigures(
            df_list=[df_v_0, df_v_1],
            f_title="Speed v in time t",
            x_label="Time [s]",
            y_label="Speed [m/s]"
        ),
            layout.drawFigures(
            df_list=[df_x_0, df_x_1],
            f_title="Position x in time t",
            x_label="Time [s]",
            y_label="Position [m]"
        ).add_hline(y=modelPID.setpoint,  # * 100.0,
                    line_dash="dash",
                    line_color="green"),
            layout.drawFigures(
            df_list=[df_e_0, df_e_1],
            f_title="Error e in time t",
            x_label="Time [s]",
            y_label="Error [m]"
        ),
            layout.drawFigures(
            df_list=[df_u_0, df_u_1],
            f_title="Control signal u in time t",
            x_label="Time [s]",
            y_label="Control signal [V]"
        )
        )

    @app.callback(
        Output('data-output', 'children'),
        [Input('show-button', 'n_clicks')]
    )
    def show_data(n_clicks):
        if n_clicks is None:
            return ''

        data = 'Mass:{}\n'.format(modelPID.m)
        data += 'Mass:{}\n'.format(modelFUZZY.m)
        data += 'SP:{}\n'.format(modelPID.setpoint)

        return dash.html.P(data)
