import pytest
from src.pre_processing import pre_process
import pandas as pd
import os
from pytest_mock import MockerFixture
import subprocess


class TestRemoveMissingData:

    def test_remove_missing_data(self) -> None:
        input_df = pd.DataFrame({"DS_VT_ESC_OCE": ["1344", "3545", None, None],
                                 "TP_PRES": [555, 222, 555, 222]})
        expected_df = pd.DataFrame({"DS_VT_ESC_OCE": ["1344", "3545", None],
                                  "TP_PRES": [555, 222, 222]}, index=[0, 1, 3])

        output_df = pre_process.remove_missing_data(input_df)
        assert output_df.equals(expected_df)


class TestRenameColumns:

    def test_rename_columns(self) -> None:
        input_df = pd.DataFrame(columns = ["a",
                                       "vt_ace_oce",
                                       "vt_ace_ofg",
                                       "vt_esc_oce",
                                       "vt_esc_ofg"])
        expected_df = pd.DataFrame(columns=["A",
                                            "DS_VT_ACE_OCE",
                                            "DS_VT_ACE_OFG",
                                            "DS_VT_ESC_OCE",
                                            "DS_VT_ESC_OFG"])
        output_df = pre_process.rename_columns_2008_2005(input_df)

        assert output_df.equals(expected_df)


class TestGetFilePath:

    def test_get_file_path(self, tmpdir) -> None:

        expected = os.path.join(tmpdir, "microdados_processado_2005.csv")
        output = pre_process.get_processed_csv_file_path(2005, tmpdir)

        assert expected == output



class TestMain:

    def side_effect(self, input: pd.DataFrame) -> pd.DataFrame:
        return input

    def test_main(self, tmpdir) -> None:
        # arrange
        select_path = os.path.join(tmpdir, "select")
        processed_path = os.path.join(tmpdir, "processed")
        subprocess.run(["mkdir", select_path])

        data_2017 = "DS_VT_ESC_OCE,TP_PRES\n1,2\n"
        data_2014 = "DS_VT_ESC_OCE,TP_PRES\n2,3\n"
        data_2011 = "DS_VT_ESC_OCE,TP_PRES\n3,4\n"
        data_2008 = "vt_esc_oce,tp_pres\n4,5\n"
        data_2005 = "vt_esc_oce,tp_pres\n5,6\n"
        output_data_2008 = "DS_VT_ESC_OCE,TP_PRES\n4,5\n"
        output_data_2005 = "DS_VT_ESC_OCE,TP_PRES\n5,6\n"

        years = [2017, 2014, 2011, 2008, 2005]
        data = [data_2017, data_2014, data_2011, data_2008, data_2005]
        output_data = [data_2017, data_2014, data_2011, output_data_2008,
                       output_data_2005]

        for year, string in zip(years, data):
            file_name = os.path.join(select_path,
                                     f"microdados_ciencia_computacao_{year}.csv")
            with open(file_name, "w") as f:
                f.write(string)

        # execute
        pre_process.main(select_path=select_path,
                         processed_path=processed_path)

        # assert
        for year, string in zip(years, output_data):
            file_name = os.path.join(processed_path,
                                    f"microdados_processado_{year}.csv")
            with open(file_name, "r") as f:
                data = f.read()
                assert data == string


class TestReadCsv:

    def test_read_csv(self, tmpdir) -> None:
        year = 2005
        # setup
        file_path = os.path.join(tmpdir, f"microdados_processado_{year}.csv")
        with open(file_path, "w") as f:
            f.write("a,b\n1,2")
        expected_df = pd.DataFrame({"a":[1], "b": [2]})

        # execute
        output_df = pre_process.read_csv(year, tmpdir)

        # assert
        assert output_df.equals(expected_df)


@pytest.mark.parametrize("input", [2017, 2014, 2011, 2008, 2005])
@pytest.mark.make
def test_make_missing_values(input: int) -> None:
    df = pre_process.read_csv(input)
    is_present = df['TP_PRES'] == 555
    missing_answers = df["DS_VT_ESC_OCE"].isna()
    boolean_series = (is_present & missing_answers)
    assert boolean_series.any() == False


@pytest.mark.parametrize("input", [ 2008, 2005])
@pytest.mark.make
def test_make_new_columns(input: int) -> None:
    df = pre_process.read_csv(input)
    new_columns = ["DS_VT_ESC_OFG", "DS_VT_ESC_OCE", "DS_VT_ACE_OCE",
                   "DS_VT_ACE_OFG"]
    for column in new_columns:
        assert column in df.columns
