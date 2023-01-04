import sys
import logging
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from collections import Counter
from pathlib import Path
from time import sleep
from progressbar import progressbar
from caterpillar import CaterpillarDiagram

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("matplotlib.font_manager").disabled = True


def main():
    """
    Main Function
    """

    # full dataframe input - relative analysis as True
    data = pd.read_csv(
        "/home/prabal/code_testbed_general/caterd/input/caterpillar_test_data.csv",
        index_col=[0],
    )
    c_d = CaterpillarDiagram(data=data, relative=True, output_path=None)

    #########################################################

    c_d.data_summary()
    c_d.color_schema()
    c_d.caterpillar_size()
    c_d.schema_transitions()
    c_d.stationary_matrix(n_sim_iter=10 ** 4)
    c_d.generate(data_index=44, n_last_cohorts=None)

    # # Single series input
    # data1 = pd.read_csv(
    #     "/home/prabal/code_testbed_general/caterd/input/caterpillar_test_data.csv",
    #     index_col=[0],
    # )
    # # series data
    # data = data1.iloc[80, :]

    # c_d = CaterpillarDiagram(data=data, relative=False, output_path=None)
    # c_d.data_summary()
    # c_d.color_schema()
    # c_d.caterpillar_size()
    # c_d.schema_transitions()
    # c_d.stationary_matrix(n_sim_iter=10 ** 4)
    # # c_d.generate(data_index=4, n_last_cohorts=7)


if __name__ == "__main__":
    main()
