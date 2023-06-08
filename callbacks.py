from dash.dependencies import Input, Output
import layout
import dash
import importlib
import pandas as pd
import model
import json
import os
import helpers

importlib.reload(layout)  # for testing purposes


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
        model.Tsim = value
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
        model.Tp = value
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
        model.setpoint = value
        return value, value

    @app.callback(
        # Callback for controllers RadioButtons
        Output('controllerParams', 'children'),
        Input('controllersRB', 'value'),
        prevent_initial_call=True
    )
    def pick_Controller(value):
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
        model.Kp = value
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
        model.Ti = value
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
        model.Td = value
        return value, value

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
        # model.m = value
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
            y_label="Speed [undefined]"
        ),
            layout.drawFigures(
            df_list=[empty_df, empty_df],
            f_title="Position x in time t",
            x_label="Time [s]",
            y_label="Position [undefined]"
        ),
            layout.drawFigures(
            df_list=[empty_df, empty_df],
            f_title="Error e in time t",
            x_label="Time [s]",
            y_label="Error [undefined]"
        ),
            layout.drawFigures(
            df_list=[empty_df, empty_df],
            f_title="Control signal u in time t",
            x_label="Time [s]",
            y_label="Control signal [undefined]"
        )
        )

    def draw_graphs():
        df_v_0 = df_x_0 = df_e_0 = df_u_0 = df_v_1 = df_x_1 = df_e_1 = df_u_1 = pd.DataFrame(
            {"x": [], "y": []})
        if os.path.getsize(helpers.DATA_NEW) == 0:
            model.generateData(Tsim=model.Tsim,
                               Tp=model.Tp,
                               kp=model.Kp,
                               Ti=model.Ti,
                               Td=model.Td,
                               setpoint=model.setpoint,
                               output=helpers.DATA_NEW)
            df_v_0, df_x_0, df_e_0, df_u_0 = helpers.readDATA(
                helpers.DATA_NEW)
        else:
            with open(helpers.DATA_NEW, 'r+') as source_file:
                data = json.load(source_file)
                source_file.truncate()
            with open(helpers.DATA_OLD, 'w') as destination_file:
                json.dump(data, destination_file)

            model.generateData(Tsim=model.Tsim,
                               Tp=model.Tp,
                               kp=model.Kp,
                               Ti=model.Ti,
                               Td=model.Td,
                               setpoint=model.setpoint,
                               output=helpers.DATA_NEW)
            df_v_1, df_x_1, df_e_1, df_u_1 = helpers.readDATA(
                helpers.DATA_NEW)
            df_v_0, df_x_0, df_e_0, df_u_0 = helpers.readDATA(
                helpers.DATA_OLD)

        return (layout.drawFigures(
            df_list=[df_v_0, df_v_1],
            f_title="Speed v in time t",
            x_label="Time [s]",
            y_label="Speed [undefined]"
        ),
            layout.drawFigures(
            df_list=[df_x_0, df_x_1],
            f_title="Position x in time t",
            x_label="Time [s]",
            y_label="Position [undefined]"
        ).add_hline(y=model.setpoint,
                    line_dash="dash",
                    line_color="green"),
            layout.drawFigures(
            df_list=[df_e_0, df_e_1],
            f_title="Error e in time t",
            x_label="Time [s]",
            y_label="Error [undefined]"
        ),
            layout.drawFigures(
            df_list=[df_u_0, df_u_1],
            f_title="Control signal u in time t",
            x_label="Time [s]",
            y_label="Control signal [undefined]"
        )
        )

    @app.callback(
        Output('data-output', 'children'),
        [Input('show-button', 'n_clicks')]
    )
    def show_data(n_clicks):
        if n_clicks is None:
            return ''

        data = 'Tsim:{}\n'.format(str(model.Tsim))
        data += 'Tp:{}\n'.format(str(model.Tp))
        data += 'SP:{}\n'.format(str(model.setpoint))
        data += 'Kp:{}\n'.format(str(model.Kp))
        data += 'Ti:{}\n'.format(str(model.Ti))
        data += 'Td:{}\n'.format(str(model.Td))
        data += 'Mass:{}\n'.format(str(model.m))

        return dash.html.P(data)
