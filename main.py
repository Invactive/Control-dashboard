import layout
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

app = Dash(external_stylesheets=[dbc.themes.SLATE],
           suppress_callback_exceptions=True)
app.layout = layout.create_layout()


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


# Run app
if __name__ == "__main__":
    app.run_server(debug=True)
