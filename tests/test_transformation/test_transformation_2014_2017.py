import pytest
from src.transformation.transform_2014_2017 import Transform2014_2017
import pandas as pd


class TestTransformDiscursiveScore20142017:

    def test_transform_discursive_scores_2014_2017_general(self) -> None:
        # arrange

        input_df = pd.DataFrame({"NT_FG_D1": [0, 50],
                                 "NT_FG_D2": [0, 100],
                                 "NT_CE_D1": [0, 0]})
        expected_df = pd.DataFrame({"NT_FG_D1": [0, 50],
                                    "NT_FG_D2": [0, 100],
                                    "NT_CE_D1": [0, 0],
                                    "QUESTAO_1_NOTA": [0, 50],
                                    "QUESTAO_2_NOTA": [0, 100]})

        # execute
        transform2014_2017 = Transform2014_2017()
        output_df = transform2014_2017.transform_discursive_scores(input_df,
                                                                   "general")

        # assert
        assert output_df.equals(expected_df)

    def test_transform_discursive_scores_2014_2017_specific(self) -> None:
        # arrange

        input_df = pd.DataFrame({"NT_CE_D1": [0, 50],
                                 "NT_CE_D2": [0, 100],
                                 "NT_CE_D3": [0, 0],
                                 "NT_FG_D1": [0, 75],
                                 })
        expected_df = pd.DataFrame({"NT_CE_D1": [0, 50],
                                    "NT_CE_D2": [0, 100],
                                    "NT_CE_D3": [0, 0],
                                    "NT_FG_D1": [0, 75],
                                    "QUESTAO_11_NOTA": [0, 50],
                                    "QUESTAO_12_NOTA": [0, 100],
                                    "QUESTAO_13_NOTA": [0, 0]})

        # execute
        transform2014_2017 = Transform2014_2017()
        output_df = transform2014_2017.transform_discursive_scores(input_df,
                                                                   "specific")

        # assert
        assert output_df.equals(expected_df)






