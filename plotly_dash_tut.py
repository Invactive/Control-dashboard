import plotly.express as px
import pandas as pd
import json


with open('DATA.json') as json_file:
    DATA = json.load(json_file)

df = pd.DataFrame(dict(
    x=DATA["t"],
    y=DATA["x"]
))
fig = px.line(df, x="x", y="y", title="Position x in time t")
fig.show()

