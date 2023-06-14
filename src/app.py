import layout
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from callbacks import get_callbacks


app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE],
           suppress_callback_exceptions=True)
server = app.server
app.layout = layout.create_layout()

get_callbacks(app)

if __name__ == "__main__":
    app.run_server()  # debug=True
