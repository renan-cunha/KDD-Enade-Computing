import pytest
from src.selection import select_data
import pandas as pd


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
