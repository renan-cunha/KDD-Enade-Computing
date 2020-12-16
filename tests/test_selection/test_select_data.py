import pytest
from src.selection import select_data
import pandas as pd
from src import config


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