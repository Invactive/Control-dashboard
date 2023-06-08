import plotly.express as px
import pandas as pd
df = px.data.gapminder().query("continent=='Oceania'")
fig = px.line(df, x="year", y="lifeExp", color='country')

x = pd.DataFrame({"x": [], "y": []})
if x.empty:
    print("asdasd")
