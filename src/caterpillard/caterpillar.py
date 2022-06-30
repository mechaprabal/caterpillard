import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# TODO:
# Logging


class CaterpillarDiagram:
    def __init__(self, data, relative: bool) -> None:
        self.data = data
        self.relative = relative

        if relative and isinstance(self.data, pd.DataFrame):
            print("\nInitial Check:\tCorrect form of data input\n")

        elif not relative and not isinstance(self.data, pd.DataFrame):
            print("\nInitial Check:\tCorrect form of data input - Absolute analysis\n")

        else:
            sys.exit(
                "\nError:\tData input type mismatched with type of analysis required\n"
            )

    def data_summary(self):
        """
        Initial summary of the data provided as input
        for analysis
        """
        print(self.data.head())
        print(f"Length of data: {len(self.data.T)}")
        print(f"Number of cohorts in caterpillar: {len(self.data.T) - 2}")

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
                print("Fatal:\tSign combination Not Captured\n")
                print(f"Sign combination:\t{data['d11']}\t{data['d12']}\t{data['d2']}")
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
        the Differences of Difference (DoD) approach
        as explained in doi:

        Input: A series of values or a Pandas DataFrame

        Output: 
            1. Cohort details
            2. Color for each cohort
        """
        if isinstance(self.data, pd.DataFrame):
            print("DataFrame received")  # Log
            self.data.fillna(value=0, inplace=True)
            d11 = self.data.diff(periods=1, axis=1).iloc[:, 1:]
            d12 = d11.shift(periods=-1, axis=1).iloc[:, :-1]
            d2 = d11.diff(periods=1, axis=1).iloc[:, 1:]
            print(f"Original data:\n {self.data}\n")  # log
            print(f"d11:\n {d11.head()}")  # log
            print(f"d12:\n {d12.head()}")  # log
            print(f"d2:\n {d2.head()}")  # log

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
                cohort_data.loc[:, "index"] = d11.iloc[i, :].name
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
                "/home/prabal/cohort_df.csv", index=False
            )  # log
            self.complete_cohort_df = pd.concat(cohort_df)
            print(self.complete_cohort_df.head())

        else:
            print("Not a Dataframe... Converting to Pandas series")  # log
            self.data.fillna(value=0, inplace=True)
            d11 = self.data.diff(periods=1).iloc[1:]
            d12 = d11.shift(periods=-1).iloc[:-1]
            d2 = d11.diff(periods=1).iloc[1:]

            print(f"Original data:\n {self.data}\n")  # log
            print(f"d11:\n {d11}")  # log
            print(f"d12:\n {d12}")  # log
            print(f"d2:\n {d2}")  # log

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
            # cohort_data.loc[:, "index"] = d11.name
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
                "/home/prabal/cohort_df.csv", index=False
            )  # log
            self.complete_cohort_df = pd.concat(cohort_df)
            print(self.complete_cohort_df.head())

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
        quartiles_description_d11 = pd.Series(
            self.complete_cohort_df["d11"].abs().values.reshape(-1)
        ).describe()
        quartiles_description_d12 = pd.Series(
            self.complete_cohort_df["d12"].abs().values.reshape(-1)
        ).describe()
        print(quartiles_description_d11, "\n\n")
        print(quartiles_description_d12, "\n\n")

        self.complete_cohort_df.loc[:, "d11_radius"] = self.complete_cohort_df[
            "d11"
        ].apply(
            lambda x: self.caterpillar_assign_radius(
                diff=abs(x), quartiles_threshold=quartiles_description_d11
            )
        )
        print(self.complete_cohort_df["d11_radius"])  # log

        self.complete_cohort_df.loc[:, "d12_radius"] = self.complete_cohort_df[
            "d12"
        ].apply(
            lambda x: self.caterpillar_assign_radius(
                diff=abs(x), quartiles_threshold=quartiles_description_d12
            )
        )
        print(self.complete_cohort_df["d12_radius"])  # log

        self.complete_cohort_df.loc[
            :, "final_cohort_radius"
        ] = self.complete_cohort_df.apply(
            lambda x: np.mean([x["d11_radius"], x["d12_radius"]]), axis=1
        )

        print(self.complete_cohort_df["final_cohort_radius"])

        self.complete_cohort_df.to_csv("/home/prabal/complete_cohort_details.csv")

    def caterpillar_viz(self):
        """
        This method will take the data of each cohort and
        create a visualization of the caterpillar diagram
        """

        # circle1 = plt.Circle((0, 0), 0.2, color="r")
        # circle2 = plt.Circle((0.5, 0.5), 0.2, color="blue")
        # circle3 = plt.Circle((1, 1), 0.2, color="g", clip_on=False)

        # fig, ax = plt.subplots()  # note we must use plt.subplots, not plt.subplot
        # # (or if you have an existing figure)
        # # fig = plt.gcf()
        # # ax = fig.gca()

        # ax.add_patch(circle1)
        # ax.add_patch(circle2)
        # ax.add_patch(circle3)

        # fig.savefig("/home/prabal/plotcircles.png")
        # # fig.show("/home/prabal/plotcircles.png")

    def schema_transitions(self):
        """
        This method will collect the consecutive
        transitions between each cohort
        """
        temp_x = self.complete_cohort_df["color"]
        temp_y = temp_x.shift(periods=-1)
        temp_z = list(zip(temp_x, temp_y))[:-1]

        self.transition_count = Counter(temp_z)
        print(self.transition_count)  # log

        self.transition_mat = pd.DataFrame(
            index=["red", "orange", "yellow", "cyan", "blue", "green", "grey"],
            columns=["red", "orange", "yellow", "cyan", "blue", "green", "grey"],
        )

        for key, value in dict(self.transition_count).items():
            self.transition_mat.loc[key[0], key[1]] = value

        print(self.transition_mat)

    def stationary_matrix(self, simulation=True):
        """
        This method will generate the stationary 
        transition matrix using either simulation approach
        or algebraic approach
        """
        # trans_mat_array = self.transition_mat.fillna(value=0).to_numpy()
        self.trans_mat_prob = (
            self.transition_mat.div(self.transition_mat.sum(axis=1), axis=0)
            .fillna(value=0)
            .copy()
        )

        if simulation:
            n = 10 ** 6
            stationary_mat = self.trans_mat_prob

            while n != 0:
                stationary_mat = np.matmul(stationary_mat, self.trans_mat_prob)
                n -= 1

            print(
                pd.DataFrame(
                    stationary_mat,
                    index=["red", "orange", "yellow", "cyan", "blue", "green", "grey"],
                    columns=[
                        "red",
                        "orange",
                        "yellow",
                        "cyan",
                        "blue",
                        "green",
                        "grey",
                    ],
                )
            )


def main():
    data = pd.read_csv("/home/prabal/caterpillar_test_data.csv", index_col=[0])
    # data1 = pd.read_csv("/home/prabal/caterpillar_test_data.csv", index_col=[0])
    # series data
    # data = data1.iloc[80, :]

    c_d = CaterpillarDiagram(data=data, relative=True)
    # c_d = CaterpillarDiagram(data=data, relative=False)
    c_d.data_summary()
    c_d.color_schema()
    c_d.caterpillar_size()
    # c_d.caterpillar_viz()
    c_d.schema_transitions()
    c_d.stationary_matrix()


if __name__ == "__main__":
    main()
