import json
import pandas as pd

DATA_NEW = "../data/DATA_new.json"
DATA_OLD = "../data/DATA_old.json"


def readDATA(src: str):
    with open(src) as json_file:
        DATA = json.load(json_file)

    df_v = pd.DataFrame(dict(
        x=DATA["t"],
        y=DATA["v"]
    ))

    df_x = pd.DataFrame(dict(
        x=DATA["t"],
        y=DATA["x"]
    ))

    df_e = pd.DataFrame(dict(
        x=DATA["t"],
        y=DATA["e"]
    ))

    df_u = pd.DataFrame(dict(
        x=DATA["t"],
        y=DATA["u"]
    ))

    return df_v, df_x, df_e, df_u
