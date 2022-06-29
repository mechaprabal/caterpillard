import sys
import pandas as pd

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


def main():
    # data = pd.read_csv("/home/prabal/caterpillar_test_data.csv", index_col=[0])
    data1 = pd.read_csv("/home/prabal/caterpillar_test_data.csv", index_col=[0])
    # series data
    data = data1.iloc[80, :]

    # c_d = CaterpillarDiagram(data=data, relative=True)
    c_d = CaterpillarDiagram(data=data, relative=False)
    c_d.data_summary()
    c_d.color_schema()


if __name__ == "__main__":
    main()
