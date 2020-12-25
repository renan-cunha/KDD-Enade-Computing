import os

import pandas as pd
import pytest
from pytest_mock import MockerFixture

from src import config
from src.selection import select_data


class TestFilter2017and2014and2011:

    def test_data_frame(self):
        code = select_data.COMPUTER_SCIENCE_CODE_2017_2014_2011

        input_df = pd.DataFrame(columns=["dados", "CO_GRUPO"],
                                data=[["1", code],
                                      ["2", code+1],
                                      ["3", code -1]])

        expected_df = pd.DataFrame(columns=["dados", "CO_GRUPO"],
                                   data=[["1", code]])

        output_df = select_data.filter_computer_science_2017_2014_2011(input_df)

        assert output_df.equals(expected_df)


class TestFilter2008:

    def test_data_frame(self):
        code = select_data.COMPUTER_SCIENCE_CODE_2008

        input_df = pd.DataFrame(columns=["dados", "co_subarea"],
                                data=[["1", code],
                                      ["2", code+1],
                                      ["3", code-1]])

        expected_df = pd.DataFrame(columns=["dados", "co_subarea"],
                                   data=[["1", code]])

        output_df = select_data.filter_computer_science_2008(input_df)

        assert output_df.equals(expected_df)


class TestGetComputerScienceAnswerKey2005:

    def test_raise_value_error(selfs) -> None:

        input_series = pd.Series(["...", ".."])
        with pytest.raises(ValueError):
            select_data.get_computer_science_answer_key_2005(input_series)

    def test_example(self) -> None:
        input_series = pd.Series([".ad..", "..d.."])

        expected_output = (".", "..")

        output = select_data.get_computer_science_answer_key_2005(input_series)

        assert output == expected_output


class TestFilter2005:

    def test_example(self) -> None:

        input_dataframe = pd.DataFrame({"co_curso": [config.CODE_UFPA_COURSE,
                                                     config.CODE_UFPA_COURSE,
                                                     1245, 1256, 1257],
                                        "vt_ace_oce": [".abc..", ".ab...",
                                                       ".acc..",
                                                       ".adec.",
                                                       ".abc.."],
                                        "co_grupo": [40, 40, 40, 40, 12]})

        expected_df = pd.DataFrame({"co_curso": [config.CODE_UFPA_COURSE,
                                                 config.CODE_UFPA_COURSE,
                                                 1245],
                                    "vt_ace_oce": [".abc..", ".ab...",
                                                  ".acc.."],
                                    "co_grupo": [40, 40, 40]})

        output_df = select_data.filter_computer_science_2005(input_dataframe)
        assert output_df.equals(expected_df)


class TestGetSelectedEnadeCsvFilePath:

    def test_example(self, tmpdir) -> None:
        year = 2005

        expected_output = os.path.join(tmpdir, "microdados_ciencia_computacao_2005.csv")

        output = select_data.get_selected_enade_csv_file_path(year,
                                                              path=tmpdir)
        assert  output == expected_output


class TestFilterComputerScience:

    def return_input_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame({"in_grad": [0, 1], "column2": [2, 3]})

    def return_output_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame({"in_grad": [0], "column2": [2]})

    def test_2017(self, mocker: MockerFixture) -> None:
        year = 2017
        mocker.patch("src.selection.select_data.filter_computer_science_2017_2014_2011",
                     side = self.return_input_dataframe)

        input_df = self.return_input_dataframe()
        output_df = select_data.filter_computer_science(input_df, year)

        assert output_df.equals(input_df)

    def test_2008(self, mocker: MockerFixture) -> None:
        year = 2008
        mocker.patch("src.selection.select_data.filter_2008",
                     side = self.return_output_dataframe)

        input_df = self.return_output_dataframe()
        output_df = select_data.filter_computer_science(input_df, year)

        assert output_df.equals(input_df)
        select_data.filter_2008.called_once()

    def test_2005(self, mocker: MockerFixture) -> None:
        year = 2005
        mocker.patch("src.selection.select_data.filter_2005",
                     side = self.return_output_dataframe)

        input_df = self.return_output_dataframe()
        output_df = select_data.filter_computer_science(input_df, year)

        assert output_df.equals(input_df)
        select_data.filter_2005.called_once()


class TestFilterSeniorStudents:

    def test_filter_senior_students(self) -> None:
        input_df = pd.DataFrame({"in_grad": [0, 1]})
        expected_df = pd.DataFrame({"in_grad": [0]})

        output_df = select_data.filter_senior_students(input_df)
        assert output_df.equals(expected_df)


class TestFilterEnade2008:

    def test_filter_2008(self) -> None:
        input_df = pd.DataFrame({"in_grad": [0, 1, 0, 1],
                                 "co_subarea": [4001, 4001, 4000, 4000]})
        expected_df = pd.DataFrame({"in_grad": [0], "co_subarea": [4001]})

        output_df = select_data.filter_2008(input_df)
        assert output_df.equals(expected_df)


class TestFilterEnade2005:

    def side_effect(self, df: pd.DataFrame) -> pd.DataFrame:
        return df

    def test_filter_2005(self, mocker: MockerFixture) -> None:

        input_df = pd.DataFrame({"in_grad": [0, 1],
                                 "co_subarea": [4001, 4001]})
        expected_df = pd.DataFrame({"in_grad": [0], "co_subarea": [4001]})
        mocker.patch("src.selection.select_data.filter_computer_science_2005",
                     side_effect=self.side_effect)

        output_df = select_data.filter_2008(input_df)
        assert output_df.equals(expected_df)

        output_df = select_data.filter_2008(input_df)
        assert output_df.equals(expected_df)


class TestMain:

    expected_df = pd.DataFrame({"column1": [1],
                             "column2": [2]})

    def read_csv(self, year: int) -> pd.DataFrame:
        return pd.DataFrame()

    def filter_computer_science(self, df: pd.DataFrame,
                                year: int) -> pd.DataFrame:
        return self.expected_df

    def test_example(self, tmpdir, mocker) -> None:

        mocker.patch("src.get_data.get_raw_data.GetData.read_csv",
                     side_effect=self.read_csv)
        mocker.patch("src.selection.select_data.filter_computer_science",
                     side_effect=self.filter_computer_science)
        select_data.main(tmpdir, tmpdir)

        for year in config.YEARS:
            file_path = os.path.join(tmpdir,
                                     f"microdados_ciencia_computacao_{year}.csv")
            df = pd.read_csv(file_path)
            assert df.equals(self.expected_df)


class TestReadCsv:

    def test_read_csv(self, tmpdir) -> None:
        year = 2005
        # setup
        file_path = os.path.join(tmpdir, f"microdados_ciencia_computacao_{year}.csv")
        with open(file_path, "w") as f:
            f.write("a,b\n1,2")
        expected_df = pd.DataFrame({"a":[1], "b": [2]})

        # execute
        output_df = select_data.read_csv(year, tmpdir)

        # assert
        assert output_df.equals(expected_df)
