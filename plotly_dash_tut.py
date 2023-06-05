import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(id='element', children='Initial Element'),
        html.Button('Change Element', id='change-button'),
    ]
)


@app.callback(
    Output('element', 'children'),
    [Input('change-button', 'n_clicks')]
)
def change_element(n_clicks):
    if n_clicks is None:
        return 'Initial Element'

    if n_clicks % 2 == 0:
        return 'Even Clicks'
    else:
        return 'Odd Clicks'


if __name__ == '__main__':
    app.run_server(debug=True, port=8055)
