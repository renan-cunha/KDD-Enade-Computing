import pytest
from src.transformation.transform_2011 import Transform2011
import pandas as pd
from pytest_mock import MockerFixture
from typing import List, Tuple
import numpy as np


class TestGetQuestionsIdsAndsLabels:

    @pytest.mark.parametrize("input,expected",
                             [
                                 (["general", "objective"], ([1,2,3,4,5,6,7,8], [0,1,2,3,4,5,6,7])),
                                 (["general", "discursive"], ([9, 10], [1, 2])),
                                 (["specific", "objective"], (list(range(14, 40 + 1)), list(range(22)) + list(range(27, 32)))),
                                 (["specific", "discursive"], ([11, 12, 13], [1, 2, 3]))
                              ])
    def test_get_questions_ids_and_labels(self, input, expected):
        transform2011 = Transform2011()
        test_type, question_format = input
        output = transform2011.get_questions_ids_and_labels(test_type,
                                                                  question_format)
        assert output[0] == expected[0]
        assert output[1] == expected[1]


class TestTransformDiscursiveQuestions2011:

    @pytest.mark.parametrize("input", [("specific", "CE"),
                                       ("general", "FG")])
    def test_transform_discursive_scores_2011_specific(self, input,
                                                            mocker: MockerFixture) -> None:
        # arrange
        test_type, label = input
        input_df = pd.DataFrame({f"NT_{label}_D1": [0, 50],
                                 f"NT_{label}_D2": [0, 0],
                                 f"TP_S{label}_D1": [333, 555],
                                 f"TP_S{label}_D2": [335, 335],
                                 })
        expected_df = pd.DataFrame({f"NT_{label}_D1": [0, 50],
                                    f"NT_{label}_D2": [0, 0],
                                    f"TP_S{label}_D1": [333, 555],
                                    f"TP_S{label}_D2": [335, 335],
                                    "QUESTAO_1_SITUACAO": ["branco", "ok"],
                                    "QUESTAO_1_NOTA": [0.0, 50.0],
                                    "QUESTAO_2_SITUACAO": [np.nan, np.nan],
                                    "QUESTAO_2_NOTA": [np.nan, np.nan]}
                                   )

        def side_effect(test_type: str,
                        question_format:  str) -> Tuple[List[int], List[int]]:
            return [1, 2], [1, 2]

        mocker.patch("src.transformation.transform.Transform.get_questions_ids_and_labels",
                     side_effect=side_effect)

        # execute
        transform2014_2017 = Transform2011()
        output_df = transform2014_2017.transform_questions(input_df, test_type,
                                                           "discursive")

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
                                    "QUESTAO_1_SITUACAO": ["ok"],
                                    "QUESTAO_1_NOTA": [0.0],
                                    "QUESTAO_2_SITUACAO": ["ok"],
                                    "QUESTAO_2_NOTA": [100.0],
                                    "QUESTAO_3_SITUACAO": ["branco"],
                                    "QUESTAO_3_NOTA": [0.0],
                                    "QUESTAO_4_SITUACAO": ["rasura"],
                                    "QUESTAO_4_NOTA": [0.0],
                                    "QUESTAO_5_SITUACAO": [np.nan],
                                    "QUESTAO_5_NOTA": [np.nan],
                                    "QUESTAO_6_SITUACAO": [np.nan],
                                    "QUESTAO_6_NOTA": [np.nan],
                                    })

        def side_effect(test_type: str,
                        question_format:  str) -> Tuple[List[int], List[int]]:
            return [1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4, 5]

        mocker.patch("src.transformation.transform.Transform.get_questions_ids_and_labels",
                     side_effect=side_effect)

        # execute
        transform2014_2017 = Transform2011()
        output_df = transform2014_2017.transform_questions(input_df,
                                                           test_type, "objective")

        # assert
        assert output_df.equals(expected_df)
        transform2014_2017.get_questions_ids_and_labels.assert_called_once_with(test_type,
                                                                                "objective")
