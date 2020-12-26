import pytest
from src.transformation.transform_2014_2017 import Transform2014_2017
import pandas as pd
from pytest_mock import MockerFixture
from typing import List, Tuple
import numpy as np


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
        output_df = transform2014_2017.transform_discursive_questions(input_df,
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
        output_df = transform2014_2017.transform_discursive_questions(input_df,
                                                                   "specific")

        # assert
        assert output_df.equals(expected_df)


class TestTransformObjectiveQuestions:

    @pytest.mark.parametrize("input", [("specific", "CE"),
                                       ("general", "FG")])
    def test_transform_objective_questions(self, input,
                                           mocker: MockerFixture) -> None:
        test_type, label = input
        # arrange
        input_df = pd.DataFrame({f"DS_VT_ACE_O{label}": ["01.*89"]})
        expected_df = pd.DataFrame({f"DS_VT_ACE_O{label}": ["01.*89"],
                                    "QUESTAO_1_NOTA": [0.0],
                                    "QUESTAO_1_SITUACAO": ["ok"],
                                    "QUESTAO_2_NOTA": [100.0],
                                    "QUESTAO_2_SITUACAO": ["ok"],
                                    "QUESTAO_3_NOTA": [0.0],
                                    "QUESTAO_3_SITUACAO": ["branco"],
                                    "QUESTAO_4_NOTA": [0.0],
                                    "QUESTAO_4_SITUACAO": ["rasura"],
                                    "QUESTAO_5_NOTA": [np.nan],
                                    "QUESTAO_5_SITUACAO": [np.nan],
                                    "QUESTAO_6_NOTA": [np.nan],
                                    "QUESTAO_6_SITUACAO": [np.nan],
                                    })

        def side_effect(test_type: str,
                        question_format:  str) -> Tuple[List[int], List[int]]:
            return [1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4, 5]

        mocker.patch("src.transformation.transform.Transform.get_questions_ids_and_labels",
                     side_effect=side_effect)

        # execute
        transform2014_2017 = Transform2014_2017()
        output_df = transform2014_2017.transform_objective_questions(input_df,
                                                                     test_type)

        # assert
        assert output_df.equals(expected_df)
        transform2014_2017.get_questions_ids_and_labels.assert_called_once_with(test_type,
                                                                                "objective")
