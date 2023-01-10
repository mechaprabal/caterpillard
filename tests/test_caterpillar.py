import pytest
import numpy as np
import pandas as pd
from caterpillard import CaterpillarDiagram
import importlib.resources

# TODO: check data values as float or integer not any other type
@pytest.fixture
def test_data():
    test_file_path_str = str(
        importlib.resources.files("tests").joinpath("test_data.csv")
    )
    data = pd.read_csv((test_file_path_str), index_col=[0])
    print(len(data))
    return data


def test_init_data_type():
    with pytest.raises(TypeError):
        assert CaterpillarDiagram(data=[1, 2, 3, 4], relative=True, output_path=None,)


def test_init_data_len(test_data):

    assert CaterpillarDiagram(data=test_data, relative=True, output_path=None,)


def test_init_data_less_col(test_data):
    with pytest.raises(SystemExit):
        assert CaterpillarDiagram(
            data=test_data.iloc[:, :1], relative=True, output_path=None,
        )


def test_init_relative_type(test_data):
    # Non bool type relative param raises exception
    with pytest.raises(TypeError):
        assert CaterpillarDiagram(data=test_data, relative=1, output_path=None,)


def test_init_outpath_type(test_data):
    # Non str type output_path param raises exception
    with pytest.raises(TypeError):
        assert CaterpillarDiagram(data=test_data, relative=True, output_path=1,)


def test_init_outpath_permission(test_data):
    # output_path param raises exception when permissions are not present to rw
    with pytest.raises(PermissionError):
        assert CaterpillarDiagram(
            data=test_data, relative=True, output_path="/root/x/",
        )


def test_init_input_data_type_mismatch(test_data):
    with pytest.raises(SystemExit):
        assert CaterpillarDiagram(data=test_data, relative=False, output_path=None,)


def test_caterpillarsize_early_invoke(test_data):
    """
    This test will check whether an error gets raised due
    to an early invoking of caterpillar size method
    """
    with pytest.raises(SystemExit):
        cd = CaterpillarDiagram(data=test_data, relative=True, output_path=None,)
        cd.data_summary()
        assert cd.caterpillar_size()


def test_schematrans_early_invoke(test_data):
    """
    This test will check whether an error gets raised due
    to an early invoking of schema transitions method
    """
    with pytest.raises(SystemExit):
        cd = CaterpillarDiagram(data=test_data, relative=True, output_path=None,)
        cd.data_summary()
        assert cd.schema_transitions()


def test_stationary_mat_early_invoke(test_data):
    """
    This test will check whether an error gets raised due
    to an early invoking of staionary matrix method
    """
    with pytest.raises(SystemExit):
        cd = CaterpillarDiagram(data=test_data, relative=True, output_path=None,)
        cd.data_summary()
        assert cd.stationary_matrix()


def test_n_sim_iter_type(test_data):
    """
    This test will check the input of n_sim_iter as an int
    It will pass if the method raises an exception on input
    other than int
    """
    with pytest.raises(SystemExit):
        cd = CaterpillarDiagram(
            data=test_data.iloc[:10], relative=True, output_path=None,
        )
        cd.data_summary()
        cd.color_schema()
        cd.caterpillar_size()
        cd.schema_transitions()
        assert cd.stationary_matrix(n_sim_iter="10")


def test_n_sim_iter_val(test_data):
    """
    This test will check the input of n_sim_iter
    It will pass if the method raises an exception on input
    less than or equal to zero
    """
    with pytest.raises(SystemExit):
        cd = CaterpillarDiagram(
            data=test_data.iloc[:10], relative=True, output_path=None,
        )
        cd.data_summary()
        cd.color_schema()
        cd.caterpillar_size()
        cd.schema_transitions()
        assert cd.stationary_matrix(n_sim_iter=-1)


def test_data_index_param_type(test_data):
    """
    Test passes when method raises an error for 
    wrong kind of data type input in data_index param
    """
    with pytest.raises(SystemExit):
        cd = CaterpillarDiagram(
            data=test_data.iloc[:10], relative=True, output_path=None,
        )
        cd.data_summary()
        cd.color_schema()
        cd.caterpillar_size()
        cd.schema_transitions()
        cd.stationary_matrix(n_sim_iter=100)
        assert cd.generate(data_index="92", n_last_cohorts=15)


def test_data_index_param_value(test_data):
    """
    Test passes when method raises an error for 
    wrong/out of bounds data input in data_index param
    """
    with pytest.raises(SystemExit):
        cd = CaterpillarDiagram(
            data=test_data.iloc[:10], relative=True, output_path=None,
        )
        cd.data_summary()
        cd.color_schema()
        cd.caterpillar_size()
        cd.schema_transitions()
        cd.stationary_matrix(n_sim_iter=100)
        assert cd.generate(data_index=340, n_last_cohorts=15)


def test_n_last_cohort_param_type(test_data):
    """
    Test passes when method raises an error for 
    wrong kind of data type input in n_last_cohort param
    """
    with pytest.raises(SystemExit):
        cd = CaterpillarDiagram(
            data=test_data.iloc[:10], relative=True, output_path=None,
        )
        cd.data_summary()
        cd.color_schema()
        cd.caterpillar_size()
        cd.schema_transitions()
        cd.stationary_matrix(n_sim_iter=100)
        assert cd.generate(data_index=92, n_last_cohorts="15")


def test_n_last_cohort_param_value(test_data):
    """
    Test passes when method raises an error for 
    wrong data input in n_last_cohort param
    """
    with pytest.raises(SystemExit):
        cd = CaterpillarDiagram(
            data=test_data.iloc[:10], relative=True, output_path=None,
        )
        cd.data_summary()
        cd.color_schema()
        cd.caterpillar_size()
        cd.schema_transitions()
        cd.stationary_matrix(n_sim_iter=100)
        assert cd.generate(data_index=92, n_last_cohorts=55)


def test_input_dataframe_numeric():
    """
    This test will pass if it catches the exception when input dataframe is non-numeric
    """
    test_data_val = np.random.randint(low=1, high=90, size=(5, 7))
    test_data = pd.DataFrame(index=range(5), columns=range(7), data=test_data_val)

    with pytest.raises(SystemExit):
        cd = CaterpillarDiagram(
            data=test_data.astype(str), relative=True, output_path=None,
        )


def test_input_dataseries_numeric():
    """
    This test will pass if it catches the exception when input data series is non-numeric
    """
    test_data_val = np.random.randint(low=1, high=90, size=70)
    test_data = pd.Series(index=range(70), data=test_data_val)

    with pytest.raises(SystemExit):
        cd = CaterpillarDiagram(
            data=test_data.astype(str), relative=False, output_path=None,
        )

