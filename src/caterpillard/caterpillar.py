import sys
import logging
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas.api.types as ptypes

from collections import Counter
from pathlib import Path
from time import sleep
from progressbar import progressbar


class CaterpillarDiagram:
    """Main class for generating Caterpillar Diagram and subsequent forecasting

    
    """

    def __init__(self, data, relative: bool, output_path=None) -> None:
        """Constructor

        The class constructor will initialize the ``data`` 
        variable for input, a boolean ``relative`` variable 
        for choosing either relative or individual analysis
        and let users choose an output directory for storing
        the generated data.

        :ivar data: input data
        :ivar relative: boolean variable
        :ivar output_path: path for writing output

        Parameters
        ----------
        data : Pandas Series or DataFrame
            Univariate data as an input for the package
             in wide format.

            If the input is a dataframe, then the column
            must represent the time-axis (in years/months
            etc.) while each row represents a unique entity
            in the dataset. Refer to the example dataset or
            tutorial section for further details. 

        relative : bool
            Boolean argument for executing a relative analysis
            or an individual analysis
        output_path : str
            User-defined path for output data.

            When user doesn't specify an output path, the 
            constructor will create a ``caterpillard_output``
            directory in the current working directory.
        
        Returns
        -------
        None

        """
        self.logger = logging.getLogger(__name__)

        # Raise exceptions for non-compliant inputs from user
        if isinstance(data, pd.DataFrame) or isinstance(data, pd.Series):
            self.logger.info("Input Data type is correct")
            self.data = data
            try:
                self.logger.debug(len(self.data.T))

                assert (
                    len(self.data.T) >= 3
                ), "Inappropriate length of wide format input data"
            except AssertionError as e:
                sys.exit(e)

        else:
            raise TypeError(
                "Input parameter 'data' should be Pandas Series or Pandas DataFrame"
            )

        if isinstance(relative, bool):
            self.logger.info("Parameter relative is of correct data type")
            self.relative = relative
        else:
            raise TypeError("Parameter relative must be of Boolean Type")

        # Check if input data columns are numeric
        if isinstance(data, pd.DataFrame):

            try:
                assert all(
                    ptypes.is_numeric_dtype(self.data.loc[:, col])
                    for col in self.data.columns
                )
            except AssertionError as e:
                sys.exit("Input data values are non-numeric")

        elif isinstance(data, pd.Series):
            # Check if input data columns are numeric
            try:
                assert ptypes.is_numeric_dtype(self.data)

            except AssertionError as e:
                sys.exit("Input data values are non-numeric")

        if output_path is not None:
            # Check if user-defined path is in string format
            if isinstance(output_path, str):
                self.logger.info("Parameter output_path is of correct data type")

                # Check if the user-defined output path exists and is a directory
                if Path(output_path).exists():
                    self.output_path = output_path
                else:

                    try:
                        os.mkdir(output_path)
                        self.output_path = output_path
                    except FileExistsError as e:
                        sys.exit(
                            "Not able to create directory for output path" + str(e)
                        )
                    except PermissionError as e:
                        sys.exit(
                            "Operating System level error when creating directory"
                            + str(e)
                        )
            else:
                raise TypeError("Parameter output_path must be of String")

        else:
            out_path = Path.cwd() / "caterpillard_output"
            if out_path.is_dir():
                self.logger.debug("Output directory already exists")
                self.output_path = out_path
            else:
                try:
                    out_path.mkdir()
                except FileExistsError:
                    sys.exit("Not able to create directory for output path")
                except OSError:
                    sys.exit(
                        "Operating System level error when creating mentioned directory"
                    )

                self.logger.info(
                    f"Directory created:\t{Path.cwd() / 'caterpillard_output'}"
                )
                self.output_path = out_path

        if relative and isinstance(self.data, pd.DataFrame):
            self.logger.debug(
                "\nInitial Check:\tCorrect form of data input for relative analysis\n"
            )

        elif not relative and not isinstance(self.data, pd.DataFrame):
            self.logger.debug(
                "\nInitial Check:\tCorrect form of data input for Individual analysis\n"
            )

        else:
            sys.exit("\nError:\tData input type mismatched with type of analysis\n")

    def data_summary(self):
        """Initial data summary

        This method provides an initial data summary by 
        logging the head of the data, length of the data
        (length of transposed dataframe due to wide form
        data as input) and calculates the length of cohorts.
        
        This method also evaluates the number of cohorts
        based on the number of columns provided in the 
        wide format data as input.


        :ivar data: Pandas Series or Pandas DataFrame.

            This method utilizes the self.data variable 
            instantiated by the 
            :meth:`caterpillar.CaterpillarDiagram.__init__`
        
        :ivar n_cohorts: int

            n_cohorts store the number of cohorts possible in
            the input data as an integer number

        """
        self.logger.debug("Summarizing Data")
        print("Summarizing Data")
        if self.relative:
            self.logger.info(self.data.info())
            self.logger.debug(f"Length of data: {len(self.data.T)}")
        else:
            self.logger.info(self.data.describe())
            self.logger.debug(f"Length of data: {len(self.data.T)}")

        self.logger.debug(f"Number of cohorts in caterpillar: {len(self.data.T) - 2}")
        self.n_cohorts = len(self.data.T) - 2

        return

    def schema(self, data, out="color"):
        """Method for color assignment using proposed color schema.
        
        This method assigns a color or a level based on the proposed
        color schema in the original article available at 
        https://doi.org/10.1177/20597991221144577. The method will 
        return only one out of the 
        following three choices of color, level
        or color number.
        
        The following is the proposed color schema based on the
        combination of d\ :sub:`11` \, d\ :sub:`12` \ and 
        d\ :sub:`2` \.

        ============== ============== =========== ====== ======= =========
        :math:`d_{11}` :math:`d_{12}` :math:`d_2` level  color    n_color
        ============== ============== =========== ====== ======= =========
        \+             \+             \+          level1 red       1
        0              \+             \+          level1 red       1
        \+             \+             \-          level2 orange    2
        \+             0              \-          level2 orange    2
        \-             \+             \+          level3 yellow    3
        \+             \-             \-          level4 cyan      4
        \-             \-             \+          level5 blue      5
        \-             0              \+          level5 blue      5
        \-             \-             \-          level6 green     6
        0              0              0           level7 grey      7
        0              \-             \-          level6 green     6
        ============== ============== =========== ====== ======= =========

        
        Parameters
        ----------
        data : Pandas Series
            The input data series that contains three values of
            :math:`d_{11}`, :math:`d_{12}` and :math:`d_2`

        out : str
            Argument can take value as ``color`` or ``level``
            or ``n_color`` to modify the data returned by this
            method.


        Returns
        -------
        color : str

        level : str

        n_color : int
        """
        try:
            error_msg = (
                "Output type for this method doesn't match. Check Documentation."
            )
            assert out in ["color", "level", "n_color"], error_msg
        except AssertionError as e:
            sys.exit(e)

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
                raise ValueError("Fatal:\tSign combination Not Captured\n")
                sys.exit()

        # Conditional return
        if out == "color":
            return color
        elif out == "level":
            return level
        elif out == "n_color":
            return n_color
            # {"level": level, "color": color, "n_color": n_color}

    def color_schema(self):
        """Generate the color schema using DoD

        This method will generate the color schema using
        the Difference of Differences (DoD) approach
        as explained in doi: https://doi.org/10.1177/20597991221144577

        
        Input: A series of values or a Pandas DataFrame

        Pre-processing: NAs in the input data will get 
        filled with zero

        This method utilizes 
        :meth:`caterpillar.CaterpillarDiagram.schema()`
        to assign a color and level to the combination of 
        first and second differences in each cohort.

        Writes complete cohort details to the filesystem
        at the given output_path
        
        :ivar cohort_df: Pandas DataFrame

            Stores all cohort details like color of the cohort,
            level of the cohort, and the respective first and 
            second differences for each cohort in a class variable
        """
        self.logger.debug("Generating Schema")
        if isinstance(self.data, pd.DataFrame):
            self.logger.debug("DataFrame received")  # Log
            self.logger.debug("Filling NAs with zero")
            self.data = self.data.fillna(value=0)
            d11 = self.data.diff(periods=1, axis=1).iloc[:, 1:]
            d12 = d11.shift(periods=-1, axis=1).iloc[:, :-1]
            d2 = d11.diff(periods=1, axis=1).iloc[:, 1:]

            self.logger.debug(f"Original data:\n {self.data}\n")  # log
            self.logger.info(f"d11:\n {d11.head()}")  # log
            self.logger.info(f"d12:\n {d12.head()}")  # log
            self.logger.info(f"d2:\n {d2.head()}")  # log
            self.logger.debug(f"d11 len:\t {len(d11)}")  # log
            self.logger.debug(f"d12 len:\t {len(d12)}")  # log
            self.logger.debug(f"d2 len:\t {len(d2)}")  # log

            self.logger.debug(f"shape: {d11.shape}")
            cohort_df = []
            # in relative analysis, d11, d12 and d2 is a
            # dataframe. So, iter as many times as there are
            # unique index rows in d11. So, d11.shape[0]-1
            for i in range(d11.shape[0]):
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
                    lambda x: self.schema(x, out="color"), axis=1,
                )

                cohort_data.loc[:, "level"] = cohort_data.apply(
                    lambda x: self.schema(x, out="level"), axis=1
                )

                cohort_data.loc[:, "n_color"] = cohort_data.apply(
                    lambda x: self.schema(x, out="n_color"), axis=1
                )
                cohort_df.append(cohort_data)

            self.complete_cohort_df = pd.concat(cohort_df, axis=0)
            self.logger.debug(
                f"Complete_cohort info:\n{self.complete_cohort_df.info()}"
            )
            self.complete_cohort_df.to_csv(
                f"{self.output_path}/cohort_df.csv", index=False,
            )  # log
            # self.complete_cohort_df = pd.concat(cohort_df)
            # self.logger.debug(
            #     f"Complete_cohort info:\n{self.complete_cohort_df.info()}"
            # )

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

            try:
                pd.concat(cohort_df).to_csv(
                    f"{self.output_path}/cohort_df.csv", index=False,
                )
            except Exception as e:
                sys.exit(e)
            else:
                self.logger.info("Cohort DataFrame saved to filesystem\n")  # log
            self.complete_cohort_df = pd.concat(cohort_df)
            self.logger.debug(self.complete_cohort_df.head())

    def caterpillar_assign_radius(self, diff, quartiles_threshold):
        """This function will assign the radius to each
        cohort in a Caterpillar Diagram.

        Employing the box-plot threshold of each quartile
        resulted from the absolute first difference, this
        function assign radius in following fashion:

        Radius of 2 units: :math:`min.\ of\ box-plot \le x < first\ quartile`

        Radius of 4 units: :math:`first\ quartile \le x < second\ quartile`
        
        Radius of 6 units: :math:`second\ quartile \le x < third\ quartile`
        
        Radius of 8 units: :math:`third\ quartile \le x`

        Parameters
        ----------
        diff : float
            First differences value, :math:`d_{11}\ or\ d_{12}`

        quartiles_threshold : dictionary
            Dictionary that contains the key and values of the
            box-plot of the data

        Returns
        -------

        radius : int
            radius of the cohort
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
        the first differences, :math:`d_{11}\ and\ d_{12}`
        and utilizes 
        :meth:`caterpillar.CaterpillarDiagram.caterpillar_assign_radius`

        The method will assign the radius to :math:`d_{11}` 
        and :math:`d_{12}` separately.
        Since a cohort constitutes two first differences
        :math:`d_{11}` and
        :math:`d_{12}`, this function
        will find the mean of the radius of 
        :math:`d_{11}` and :math:`d_{12}` and mark this
        mean as the final radius for this cohort.

        The method will write the `complete_cohort_df` attribute to
        the filesystem as per the `output_path`

        :ivar complete_cohort_df: Pandas DataFrame

            The `complete_cohort_df` is an instance attribute that
            contains the color and radius for each cohort
        """
        # Check if complete cohort df is available
        try:
            self.complete_cohort_df
        except AttributeError as e:
            sys.exit(e)
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
        self.logger.debug(f"length check 1: {len(self.complete_cohort_df)}")
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
        self.logger.info(
            f"ccd length before writing:\n" f"{len(self.complete_cohort_df)}"
        )
        try:
            self.complete_cohort_df.to_csv(
                f"{self.output_path}/complete_cohort_details.csv",
            )
        except Exception as e:
            sys.exit(e)
        else:
            self.logger.info("Complete cohort details saved to filesystem\n")

    def schema_transitions(self):
        """
        This method will collect the consecutive
        transitions between each cohort for complete
        dataset

        :ivar transition_count: dictionary

            It contains the number of times a particular transition
            was observed between two consecutive years

        :ivar transition_mat: Pandas DataFrame
        
            Stores the consecutive color transitions as a
            Pandas Dataframe 
        """
        # Check if complete cohort df is available
        try:
            self.complete_cohort_df
        except AttributeError as e:
            sys.exit(e)

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

    def stationary_matrix(self, n_sim_iter=10 ** 4):
        """
        This method will generate the stationary
        transition matrix using simulation approach

        :ivar trans_mat_prob: Pandas DataFrame

            Stores the probability of color transitions in a 
            DataFrame 

        Parameters
        ----------
        n_sim_iter : int
       
            Number of iterations for finding the stationary transition matrix

        Returns
        -------
        stationary_mat_final_df : Pandas DataFrame
       
            Final stationary Matrix
        
        """
        try:
            assert isinstance(n_sim_iter, int)
        except AssertionError as e:
            sys.exit("Type Error " + str(e))

        try:
            assert n_sim_iter > 0
        except AssertionError as e:
            sys.exit("Value Error " + str(e))

        # Check if complete cohort df is available
        try:
            self.transition_mat
        except AttributeError as e:
            sys.exit(e)

        self.logger.debug("Finding stationary matrix")
        print("Finding stationary matrix")
        # trans_mat_array = self.transition_mat.fillna(value=0).to_numpy()
        try:
            # Replace zero row sum with 1 to remove zeroDivision error
            self.trans_mat_prob = (
                self.transition_mat.div(
                    self.transition_mat.sum(axis=1).replace({0: 1}), axis=0
                )
                .fillna(value=0)
                .copy()
            )
        except ZeroDivisionError as e:
            sys.exit(e)
        else:
            self.logger.info("Transition matrix probabilities evaluation complete")

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

        return self.stationary_mat_final_df

    def generate(self, data_index=None, n_last_cohorts=None):
        """
        This method fetches the specified 
        data and creates the caterpillar visualization. It will
        evaluate the X axis coordinates for the cohort 
        circles and the start & end coordinates of the lines
        in-between cohorts circle.

        This method will write the Caterpillar image to the filesystem
        and provides the figure object as instance attribute for
        any downstream application by the user. 

        :ivar lx_s:

            List of coordinates of start of lines in Caterpillar

        :ivar lx_e:

            List of coordinates of end of lines in Caterpillar
        
        :ivar cx:

            List of coordinates for center point of Caterpillar

        :ivar caterpillar_fig:

            Caterpillar figure object

        Parameters
        ----------

        data_index : int

            Choose the row for which Caterpillar Diagram needs to
            be generated. In case of individual analysis, this
            parameter is not required.
        
        n_last_cohorts : int
        
            Specify the number of last cohorts for which the
            Caterpillar Diagram
            needs to be generated 
        """
        try:
            err_msg = "data_index should be an integer"
            assert type(data_index) is int or data_index is None, err_msg
        except AssertionError as e:
            sys.exit(f"data_index parameter error \n {e}")
        else:
            self.logger.debug("data_index parameter Type correct")

        try:
            err_msg = "n_last_cohort should be an integer"
            assert type(n_last_cohorts) is int or n_last_cohorts is None, err_msg
        except AssertionError as e:
            sys.exit(f"n_last_cohort parameter error \n {e}")
        else:
            self.logger.debug("n_last_cohort parameter Type correct")

        self.logger.debug("Generating caterpillar diagram")
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
            try:
                err_msg = (
                    "User-defined n_last_cohorts integer is more than available cohorts"
                )
                assert self.n_cohorts >= n_last_cohorts, err_msg
            except AssertionError as e:
                sys.exit(e)
            else:
                self.logger.debug("n_last_cohorts value checked")
                n = n_last_cohorts

        if self.relative and data_index is not None:
            """
            When the input data is a dataframe then
            the following code will allow to choose
            an index from the data to create caterpillar
            """
            sleep(1)
            self.logger.info(f"ccd length:\n" f"{len(self.complete_cohort_df)}")
            sleep(1)
            self.logger.info(
                f"Available options:\n"
                f"{self.complete_cohort_df['data_index'].unique()}"
            )
            self.logger.info(f"Chosen:\t{data_index}")
            sleep(0.7)
            # TODO: ask the user to choose the index

            try:
                err_msg = "chosen data index is not in processed cohort details"
                assert (
                    data_index in self.complete_cohort_df["data_index"].unique()
                ), err_msg
            except AssertionError as e:
                sys.exit(e)
            else:
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

        elif self.relative and data_index is None:
            # relative analysis is true and data_index is not provided by
            # user then the package will raise an error
            sys.exit(
                "Relative analysis must have a data_index parameter for diagram generation"
            )
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
        self.logger.debug(f"Radius list:\n{radii}")
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
        fig, ax = plt.subplots(figsize=(n / 5 * 7, 9))
        ax.set_facecolor("white")
        circle_patch = []
        style_cohort = dict(
            size=7, color="black", rotation=90, fontfamily="Palatino Linotype",
        )
        style_radii = dict(
            size=5, color="black", rotation=0, fontfamily="Palatino Linotype",
        )

        for i in range(n):
            circle_patch.append(
                plt.Circle((cx[i], cy), radii[i], facecolor=colors[i], edgecolor="None")
            )
            ax.text(
                cx[i] - 0.5, -18, f"Cohort {i+1}", **style_cohort,
            )
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
        ax.autoscale_view()
        ax.set_aspect(1)
        plt.grid(False)
        plt.axis("off")
        plt.savefig(
            f"{self.output_path}/caterpillar.jpeg", dpi=400,
        )

        self.caterpillar_fig = fig
        self.cx = cx
        self.lx_e = lx_e
        self.lx_s = lx_s

        return

