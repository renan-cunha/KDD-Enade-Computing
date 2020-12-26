import pytest
from src.transformation.transform_2014_2017 import Transform2014_2017
import pandas as pd
from pytest_mock import MockerFixture
from typing import List, Tuple

class TestGetQuestionsIdsAndsLabels:

    @pytest.mark.parametrize("input,expected",
                             [
                                 (["general", "objective"], ([3,4,5,6,7,8,9,10], [0,1,2,3,4,5,6,7])),
                                 (["general", "discursive"], ([1, 2], [1, 2])),
                                 (["specific", "objective"], ([list(range(14, 40 + 1)), list(range(27))])),
                                 (["specific", "discursive"], ([11, 12, 13], [1, 2, 3]))
                              ])
    def test_get_questions_ids_and_labels(self, input, expected):
        transform2014_2017 = Transform2014_2017()
        test_type, question_format = input
        output = transform2014_2017.get_questions_ids_and_labels(test_type,
                                                                  question_format)
        assert output[0] == expected[0]
        assert output[1] == expected[1]


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


class TestTransformObjectiveScore20142017:

    def test_transform_objective_scores_2014_2017_general(self,
                                                          mocker: MockerFixture) -> None:
        # arrange
        input_df = pd.DataFrame({"DS_VT_ACE_OFG": ["01"]})
        expected_df = pd.DataFrame({"DS_VT_ACE_OFG": ["01"],
                                 "QUESTAO_1_NOTA": [0.0],
                                 "QUESTAO_2_NOTA": [100.0]})

        def side_effect(test_type: str,
                        question_format:  str) -> Tuple[List[int], List[int]]:
            return [1, 2], [0, 1]

        mocker.patch("src.transformation.transform.Transform.get_questions_ids_and_labels",
                     side_effect=side_effect)

        # execute
        transform2014_2017 = Transform2014_2017()
        output_df = transform2014_2017.transform_objective_scores(input_df,
                                                                  "general")

        # assert
        assert output_df.equals(expected_df)
        transform2014_2017.get_questions_ids_and_labels.assert_called_once_with("general", "objective")




