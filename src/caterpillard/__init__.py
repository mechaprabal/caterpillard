import pkg_resources
import pandas as pd

from caterpillard.caterpillar import CaterpillarDiagram


def load_dataframe():
    stream = pkg_resources.resource_stream(__name__, "data/cd_input_data.csv")
    return pd.read_csv(stream, index_col=[0])


def load_series():
    stream = pkg_resources.resource_stream(__name__, "data/cd_input_data.csv")
    return pd.read_csv(stream, index_col=[0]).loc[92]
