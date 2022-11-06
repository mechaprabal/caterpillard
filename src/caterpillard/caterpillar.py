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

# logger_cd = logging.getLogger(__name__)

# # handler
# console_hand = logging.StreamHandler()
# console_hand.setLevel(logging.DEBUG)
# # Format log
# log_format = logging.Formatter("%(name)s-%(levelname)s-%(message)s")
# console_hand.setFormatter(log_format)
# # add handler to logger_cd
# logger_cd.addHandler(console_hand)

# logger_cd.warning("This is a warning")


class CaterpillarDiagram:
    # TODO: Write the documentation for this class
    # TODO: design output variables generated by the class object like sklearn
    def __init__(self, data, relative: bool, output_path=None) -> None:
        self.logger = logging.getLogger(__name__)
        self.data = data
        self.relative = relative
        if output_path is not None:
            self.output_path = output_path
        else:
            out_path = Path.cwd() / "caterpillard_output"
            if out_path.is_dir():
                self.logger.debug("Output directory already exists")
                self.output_path = out_path
            else:
                out_path.mkdir()  # TODO: create try-except here
                self.logger.info(
                    f"Directory created:\t{Path.cwd() / 'caterpillard_output'}"
                )
                self.output_path = out_path

        if relative and isinstance(self.data, pd.DataFrame):
            self.logger.debug("\nInitial Check:\tCorrect form of data input\n")

        elif not relative and not isinstance(self.data, pd.DataFrame):
            self.logger.debug(
                "\nInitial Check:\tCorrect form of data input - Individual\n"
            )

        else:
            sys.exit("\nError:\tData input type mismatched with type of analysis\n")

    def data_summary(self):
        """
        Initial summary of the data provided as input
        for analysis
        """
        self.logger.debug("Summarizing Data")
        print("Summarizing Data")
        self.logger.info(self.data.head())
        self.logger.debug(f"Length of data: {len(self.data.T)}")
        self.logger.debug(f"Number of cohorts in caterpillar: {len(self.data.T) - 2}")
        self.n_cohorts = len(self.data.T) - 2

        return

    def schema(self, data, out="color"):
        """
            This function will assign the colors

            d11, d12, d2, level, color
            +, +, +, level1, red
            0, +, +, level1, red
            +, +, -, level2, orange
            +, 0, -, level2, orange
            -, +, +, level3, yellow
            +, -, -, level4, cyan
            -, -, +, level5, blue
            -, 0, +, level5, blue
            -, -, -, level6, green
            0, 0, 0, level7, grey
            0, -, -, level6, green

            """
        level = []
        color = []
        if data["d11"] == 0 and data["d12"] == 0 and data["d2"] == 0:
            level = "level7"
            color = "grey"
            n_color = 7

        else:
            if data["d11"] > 0 and data["d12"] > 0 and data["d2"] > 0:
                # and not(data["d11"]==0 and data["d12"]==0 and
                # data["d2"]==0):
                level = "level1"
                color = "red"
                n_color = 1
            elif data["d11"] > 0 and data["d12"] > 0 and data["d2"] < 0:
                level = "level2"
                color = "orange"
                n_color = 2
            elif data["d11"] < 0 and data["d12"] > 0 and data["d2"] > 0:
                level = "level3"
                color = "yellow"
                n_color = 3
            elif data["d11"] > 0 and data["d12"] < 0 and data["d2"] < 0:
                level = "level4"
                color = "cyan"
                n_color = 4
            elif data["d11"] < 0 and data["d12"] < 0 and data["d2"] > 0:
                level = "level5"
                color = "blue"
                n_color = 5
            elif data["d11"] < 0 and data["d12"] < 0 and data["d2"] < 0:
                level = "level6"
                color = "green"
                n_color = 6
            elif data["d11"] == 0 and data["d12"] > 0 and data["d2"] > 0:
                level = "level1"
                color = "red"
                n_color = 1
            elif data["d11"] == 0 and data["d12"] < 0 and data["d2"] < 0:
                level = (
                    "level6"  # Error rectified on Mar15, 2022.. showing this as level4
                )
                color = "green"
                n_color = 6
            elif data["d11"] < 0 and data["d12"] == 0 and data["d2"] > 0:
                level = "level5"
                color = "blue"
                n_color = 5
            elif data["d11"] > 0 and data["d12"] == 0 and data["d2"] < 0:
                level = "level2"
                color = "orange"
                n_color = 2
            elif data["d11"] > 0 and data["d12"] > 0 and data["d2"] == 0:
                level = "level1"
                color = "red"
                n_color = 1
            elif data["d11"] < 0 and data["d12"] < 0 and data["d2"] == 0:
                level = "level6"
                color = "green"
                n_color = 6
            else:
                self.logger.debug("Fatal:\tSign combination Not Captured\n")
                self.logger.debug(
                    f"Sign combination:\t{data['d11']}\t{data['d12']}\t{data['d2']}"
                )
        # Conditional return
        if out == "color":
            return color
        elif out == "level":
            return level
        elif out == "n_color":
            return n_color
            # {"level": level, "color": color, "n_color": n_color}

    def color_schema(self):
        """
        This method will generate the color schema using
        the Difference of Differences (DoD) approach
        as explained in doi: #TODO:enter doi once generated

        Input: A series of values or a Pandas DataFrame
        Pre-processing: NAs in the input data will get 
        filled with zero
        Output:
            1. Cohort details
            2. Color for each cohort
        """
        self.logger.debug("Generating Schema")
        print("Generating Schema")
        if isinstance(self.data, pd.DataFrame):
            self.logger.debug("DataFrame received")  # Log
            self.logger.debug("Filling NAs with zero")
            self.data.fillna(value=0, inplace=True)
            d11 = self.data.diff(periods=1, axis=1).iloc[:, 1:]
            d12 = d11.shift(periods=-1, axis=1).iloc[:, :-1]
            d2 = d11.diff(periods=1, axis=1).iloc[:, 1:]
            self.logger.debug(f"Original data:\n {self.data}\n")  # log
            self.logger.info(f"d11:\n {d11.head()}")  # log
            self.logger.info(f"d12:\n {d12.head()}")  # log
            self.logger.info(f"d2:\n {d2.head()}")  # log

            cohort_df = []
            for i in range(d11.shape[1] - 1):
                cohort_data = pd.concat(
                    [
                        pd.Series(d11.iloc[i, :-1].values),
                        pd.Series(d12.iloc[i, :].values),
                        pd.Series(d2.iloc[i, :].values),
                    ],
                    keys=["d11", "d12", "d2"],
                    axis=1,
                )
                cohort_data.loc[:, "data_index"] = d11.iloc[i, :].name
                cohort_name_list = [f"Cohort{i+1}" for i in range(len(cohort_data))]
                cohort_data.loc[:, "Cohort"] = cohort_name_list

                cohort_data.loc[:, "color"] = cohort_data.apply(
                    lambda x: self.schema(x, out="color"), axis=1
                )

                cohort_data.loc[:, "level"] = cohort_data.apply(
                    lambda x: self.schema(x, out="level"), axis=1
                )

                cohort_data.loc[:, "n_color"] = cohort_data.apply(
                    lambda x: self.schema(x, out="n_color"), axis=1
                )
                cohort_df.append(cohort_data)

            pd.concat(cohort_df).to_csv(
                f"{self.output_path}/cohort_df.csv", index=False,
            )  # log
            self.complete_cohort_df = pd.concat(cohort_df)
            self.logger.debug(self.complete_cohort_df.head())

        else:
            self.logger.debug("Not a Dataframe... Converting to Pandas series")  # log
            self.logger.debug("Filling NAs with zero")
            self.data.fillna(value=0, inplace=True)
            d11 = self.data.diff(periods=1).iloc[1:]
            d12 = d11.shift(periods=-1).iloc[:-1]
            d2 = d11.diff(periods=1).iloc[1:]

            self.logger.debug(f"Original data:\n {self.data}\n")  # log
            self.logger.debug(f"d11:\n {d11}")  # log
            self.logger.debug(f"d12:\n {d12}")  # log
            self.logger.debug(f"d2:\n {d2}")  # log

            cohort_df = []
            cohort_data = pd.concat(
                [
                    pd.Series(d11.iloc[:-1].values),
                    pd.Series(d12.values),
                    pd.Series(d2.values),
                ],
                keys=["d11", "d12", "d2"],
                axis=1,
            )
            # cohort_data.loc[:, "data_index"] = d11.name
            cohort_name_list = [f"Cohort{i+1}" for i in range(len(cohort_data))]
            cohort_data.loc[:, "Cohort"] = cohort_name_list

            cohort_data.loc[:, "color"] = cohort_data.apply(
                lambda x: self.schema(x, out="color"), axis=1
            )

            cohort_data.loc[:, "level"] = cohort_data.apply(
                lambda x: self.schema(x, out="level"), axis=1
            )

            cohort_data.loc[:, "n_color"] = cohort_data.apply(
                lambda x: self.schema(x, out="n_color"), axis=1
            )
            cohort_df.append(cohort_data)

            pd.concat(cohort_df).to_csv(
                f"{self.output_path}/cohort_df.csv", index=False,
            )  # log
            self.complete_cohort_df = pd.concat(cohort_df)
            self.logger.debug(self.complete_cohort_df.head())

    def caterpillar_assign_radius(self, diff, quartiles_threshold):
        """
        This function will assign the radius to each
        cohort in a color strip.

        Employing the box-plot threshold of each quartile
        resulted from the absolute first difference, this
        function assign radius in following fashion:

        Radius of 2 units: min. of box-plot <= x < first quartile
        Radius of 4 units: first quartile <= x <  second quartile
        Radius of 6 units: second quartile <= x < third quartile
        Radius of 8 units: third quartile <= x

        The function will assign the radius to d11 and d12
        separately.
        Since a time period is created by d11 and d12, this function
        will find the mean of the radius of d11 and d12 and mark this
        mean as the final radius for this time period.
        """
        #     print(d11, d12, quartiles_threshold["50%"],"\n")

        minimum = quartiles_threshold["min"]
        q1 = quartiles_threshold["25%"]
        q2 = quartiles_threshold["50%"]
        q3 = quartiles_threshold["75%"]
        maximum = quartiles_threshold["max"]

        if diff >= minimum and diff < q1:
            radius = 2
            return radius
        elif diff >= q1 and diff < q2:
            radius = 4
            return radius
        elif diff >= q2 and diff < q3:
            radius = 6
            return radius
        elif diff >= q3:
            radius = 8
            return radius
        else:
            return "Error in decision"

        # return d11_radius, d12_radius, final_radius

    def caterpillar_size(self):
        """
        This method will provide the size to each
        cohort of the caterpillar diagram based on
        the first differences, d11 and d12
        """
        self.logger.debug("Calculating sizes for each cohort")
        print("Calculating sizes for each cohort")
        quartiles_description_d11 = pd.Series(
            self.complete_cohort_df["d11"].abs().values.reshape(-1)
        ).describe()
        quartiles_description_d12 = pd.Series(
            self.complete_cohort_df["d12"].abs().values.reshape(-1)
        ).describe()
        self.logger.info(quartiles_description_d11)
        self.logger.info(quartiles_description_d12)

        self.complete_cohort_df.loc[:, "d11_radius"] = self.complete_cohort_df[
            "d11"
        ].apply(
            lambda x: self.caterpillar_assign_radius(
                diff=abs(x), quartiles_threshold=quartiles_description_d11
            )
        )
        self.logger.debug(self.complete_cohort_df["d11_radius"])  # log

        self.complete_cohort_df.loc[:, "d12_radius"] = self.complete_cohort_df[
            "d12"
        ].apply(
            lambda x: self.caterpillar_assign_radius(
                diff=abs(x), quartiles_threshold=quartiles_description_d12
            )
        )
        self.logger.debug(self.complete_cohort_df["d12_radius"])  # log

        self.complete_cohort_df.loc[
            :, "final_cohort_radius"
        ] = self.complete_cohort_df.apply(
            lambda x: np.mean([x["d11_radius"], x["d12_radius"]]), axis=1
        )

        self.logger.debug(self.complete_cohort_df["final_cohort_radius"])

        self.complete_cohort_df.to_csv(
            f"{self.output_path}/complete_cohort_details.csv",
        )

    def schema_transitions(self):
        """
        This method will collect the consecutive
        transitions between each cohort for complete
        dataset
        """
        self.logger.debug("Finding transitions")
        print("Finding transitions")

        temp_x = self.complete_cohort_df["color"]
        temp_y = temp_x.shift(periods=-1)
        temp_z = list(zip(temp_x, temp_y))[:-1]

        self.transition_count = Counter(temp_z)
        self.logger.debug(self.transition_count)  # log

        self.transition_mat = pd.DataFrame(
            index=["red", "orange", "yellow", "cyan", "blue", "green", "grey"],
            columns=["red", "orange", "yellow", "cyan", "blue", "green", "grey"],
        )

        for key, value in dict(self.transition_count).items():
            self.transition_mat.loc[key[0], key[1]] = value

        self.transition_mat.fillna(value=0, inplace=True)
        self.logger.info(f"Transition matrix:\n{self.transition_mat}")

    def stationary_matrix(self, simulation=True, n_sim_iter=10 ** 4):
        """
        This method will generate the stationary
        transition matrix using either simulation approach
        or algebraic approach
        """
        self.logger.debug("Finding stationary matrix")
        print("Finding stationary matrix")
        # trans_mat_array = self.transition_mat.fillna(value=0).to_numpy()
        self.trans_mat_prob = (
            self.transition_mat.div(self.transition_mat.sum(axis=1), axis=0)
            .fillna(value=0)
            .copy()
        )

        if simulation:
            stationary_mat = self.trans_mat_prob

            for i in progressbar(range(n_sim_iter), redirect_stdout=True):
                stationary_mat = np.matmul(stationary_mat, self.trans_mat_prob)
                sleep(0.0005)

            self.stationary_mat_final_df = pd.DataFrame(
                stationary_mat,
                index=["red", "orange", "yellow", "cyan", "blue", "green", "grey"],
                columns=["red", "orange", "yellow", "cyan", "blue", "green", "grey",],
            )
            self.logger.debug(f"\nStationary Matrix:\n{self.stationary_mat_final_df}")

    def generate(self, data_index=None, n_last_cohorts=None):
        """
        A single method that fetches the specified 
        data,creates the caterpillar visualization 
        and generates stationary matrix sequentially
        """
        # TODO: create this method using the main function
        self.logger.debug("Generating caterpillar diagram")
        print("Generating caterpillar diagram")
        # Initialize
        # cx and cy are the initial center of the first cohort
        cx = [0]
        cy = [0]
        # number of cohorts, n, calculated earlier as per input data
        # n = 7
        if n_last_cohorts is None:
            # all cohorts will be used for generating caterpillar
            n = self.n_cohorts
        else:
            n = n_last_cohorts

        if self.relative and data_index is not None:
            """
            When the input data is a dataframe then
            the following code will allow to choose
            an index from the data to create caterpillar
            """
            sleep(2)
            self.logger.info(
                f"Available options:\n"
                f"{self.complete_cohort_df['data_index'].unique()}"
            )
            self.logger.info(f"Chosen:\t{data_index}")
            sleep(0.7)

            chosen_subset = self.complete_cohort_df[
                self.complete_cohort_df["data_index"] == data_index
            ].copy()

            # radii will use the list of radius of each consecutive
            # cohort calculated earlier
            # radii = [4, 2, 6, 8, 2, 2, 6]
            radii = chosen_subset["final_cohort_radius"][-n:].to_list()

            # list of colors
            # colors = ["red", "green", "cyan", "yellow", "orange", "red", "red"]
            colors = chosen_subset["color"][-n:].to_list()

        else:
            # radii will use the list of radius of each consecutive
            # cohort calculated earlier
            # radii = [4, 2, 6, 8, 2, 2, 6]
            radii = self.complete_cohort_df["final_cohort_radius"].to_list()

            # list of colors
            # colors = ["red", "green", "cyan", "yellow", "orange", "red", "red"]
            colors = self.complete_cohort_df["color"].to_list()

        # lx_s is a list of initiating coordinate of the line
        # between each cohort
        lx_s = []

        # ll is the length of line between each cohort

        ll = 1  # line length between cohorts circle

        # lx_e is the list of ending coordinates for line
        # between each cohort
        lx_e = []

        # Process
        for i in range(n):
            if i < n - 1:
                cx.append(cx[i] + radii[i] + ll + radii[i + 1])
                lx_s.append(cx[i] + radii[i])
                lx_e.append(lx_s[i] + ll)
            else:
                break

        self.logger.info(f"Circle X-coordinate list:\n{cx}")
        self.logger.info(f"Line Start X-coordinate list:\n{lx_s}")
        self.logger.info(f"Line End X-coordinate list:\n{lx_e}")

        cy = ly = 0

        # Preparing figure
        fig, ax = plt.subplots(figsize=(70, 7))
        ax.set_facecolor("white")
        circle_patch = []
        style_cohort = dict(
            # size=7,
            color="black",
            rotation=90,
            fontfamily="Times New Roman",
        )
        style_radii = dict(
            size=5, color="black", rotation=0, fontfamily="Times New Roman",
        )

        for i in range(n):
            circle_patch.append(plt.Circle((cx[i], cy), radii[i], color=colors[i]))
            ax.text(cx[i] - 0.5, -18, f"Cohort {i+1}", **style_cohort)
            ax.text(cx[i] - 1, cy + 1, f"R={radii[i]}", **style_radii)
            ax.add_patch(circle_patch[i])
            if i != n - 1:
                ax.plot(
                    [lx_s[i], lx_e[i]],
                    [ly, ly],
                    color="black",
                    linewidth=0.5,
                    linestyle="-",
                )
            else:
                pass

        ax.set_aspect(1)
        plt.grid(False)
        plt.axis("off")
        plt.savefig(
            f"{self.output_path}/caterpillar.jpeg", dpi=300,
        )
        # TODO:save fig object as object self variable for user usage
        # plt.show()

        return


def main():
    """
    Main Function
    """

    # # full dataframe input - relative analysis as True
    # data = pd.read_csv(
    #     "/home/prabal/code_testbed_general/caterd/input/caterpillar_test_data.csv",
    #     index_col=[0],
    # )
    # c_d = CaterpillarDiagram(data=data, relative=True, output_path=None)

    # #########################################################

    # c_d.data_summary()
    # c_d.color_schema()
    # c_d.caterpillar_size()
    # c_d.schema_transitions()
    # c_d.stationary_matrix(n_sim_iter=10 ** 4)
    # c_d.generate(data_index=44, n_last_cohorts=None)

    # Single series input
    data1 = pd.read_csv(
        "/home/prabal/code_testbed_general/caterd/input/caterpillar_test_data.csv",
        index_col=[0],
    )
    # series data
    data = data1.iloc[80, :]

    c_d = CaterpillarDiagram(data=data, relative=False, output_path=None)
    c_d.data_summary()
    c_d.color_schema()
    c_d.caterpillar_size()
    c_d.schema_transitions()
    c_d.stationary_matrix(n_sim_iter=10 ** 4)
    c_d.generate(data_index=4, n_last_cohorts=7)


if __name__ == "__main__":
    main()
