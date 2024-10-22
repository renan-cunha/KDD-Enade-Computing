import pytest
from src.transformation.transform_2005 import Transform2005
import pandas as pd
from pytest_mock import MockerFixture
from typing import List, Tuple
import numpy as np


class TestGetQuestionsIdsAndsLabels:

    @pytest.mark.parametrize("input,expected",
                             [
                                 (["general", "objective"], ([1,2,3,4,5,6,7], [0,1,2,3,4,5,6])),
                                 (["general", "discursive"], ([8, 9, 10], [1, 2, 3])),
                                 (["specific", "objective"], (list(range(11, 24 + 1)) + list(range(26, 39 + 1)), list(range(28, 28 + 28)))),
                                 (["specific", "discursive"], ([25, 40], [3, 4]))
                              ])
    def test_get_questions_ids_and_labels(self, input, expected):
        transform = Transform2005()
        test_type, question_format = input
        output = transform.get_questions_ids_and_labels(test_type,
                                                                  question_format)
        assert output[0] == expected[0]
        assert output[1] == expected[1]


class TestTransformDiscursiveQuestions2005:

    @pytest.mark.parametrize("input", [("specific", "CE"),
                                       ("general", "FG")])
    def test_transform_discursive_scores(self, input,
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
                                    "QUESTAO_1_SITUACAO_DA_RESPOSTA": ["branco", "ok"],
                                    "QUESTAO_1_NOTA": [0.0, 50.0],
                                    "QUESTAO_1_SITUACAO_DA_QUESTAO": [0, 0],
                                    "QUESTAO_2_SITUACAO_DA_RESPOSTA": [np.nan, np.nan],
                                    "QUESTAO_2_NOTA": [np.nan, np.nan],
                                    "QUESTAO_2_SITUACAO_DA_QUESTAO": [1.0, 1.0]}
        )

        def side_effect(test_type: str,
                        question_format:  str) -> Tuple[List[int], List[int]]:
            return [1, 2], [1, 2]

        mocker.patch("src.transformation.transform_abstract.Transform.get_questions_ids_and_labels",
                     side_effect=side_effect)

        # execute
        transform = Transform2005()
        output_df = transform.transform_questions(input_df, test_type,
                                                           "discursive")

        # assert

        assert output_df.fillna("").equals(expected_df.fillna(""))


class TestTransformObjectiveQuestions:

    @pytest.mark.parametrize("input", [("specific", "CE"),
                                       ("general", "FG")])
    def test_transform_objective_questions(self, input,
                                           mocker: MockerFixture) -> None:
        test_type, label = input
        # arrange
        input_df = pd.DataFrame({f"DS_VT_ACE_O{label}": ["010089"],
                                 f"DS_VT_ESC_O{label}": ["AB.*CD"]})
        expected_df = pd.DataFrame({f"DS_VT_ACE_O{label}": ["010089"],
                                    f"DS_VT_ESC_O{label}": ["AB.*CD"],
                                    "QUESTAO_1_SITUACAO_DA_RESPOSTA": ["ok"],
                                    "QUESTAO_1_NOTA": [0.0],
                                    "QUESTAO_1_SITUACAO_DA_QUESTAO": [0],
                                    "QUESTAO_2_SITUACAO_DA_RESPOSTA": ["ok"],
                                    "QUESTAO_2_NOTA": [100.0],
                                    "QUESTAO_2_SITUACAO_DA_QUESTAO": [0],
                                    "QUESTAO_3_SITUACAO_DA_RESPOSTA": ["branco"],
                                    "QUESTAO_3_NOTA": [0.0],
                                    "QUESTAO_3_SITUACAO_DA_QUESTAO": [0],
                                    "QUESTAO_4_SITUACAO_DA_RESPOSTA": ["rasura"],
                                    "QUESTAO_4_NOTA": [0.0],
                                    "QUESTAO_4_SITUACAO_DA_QUESTAO": [0],
                                    "QUESTAO_5_SITUACAO_DA_RESPOSTA": ["ok"],
                                    "QUESTAO_5_NOTA": [np.nan],
                                    "QUESTAO_5_SITUACAO_DA_QUESTAO": [1],
                                    "QUESTAO_6_SITUACAO_DA_RESPOSTA": ["ok"],
                                    "QUESTAO_6_NOTA": [np.nan],
                                    "QUESTAO_6_SITUACAO_DA_QUESTAO": [1],
                                    })

        def side_effect(test_type: str,
                        question_format:  str) -> Tuple[List[int], List[int]]:
            return [1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4, 5]

        mocker.patch("src.transformation.transform_abstract.Transform.get_questions_ids_and_labels",
                     side_effect=side_effect)

        # execute
        transform = Transform2005()
        output_df = transform.transform_questions(input_df,
                                                           test_type, "objective")

        # assert
        assert output_df.equals(expected_df)
        transform.get_questions_ids_and_labels.assert_called_once_with(test_type,
                                                                                "objective")

class TestTransformationTransform:

    def test_transformation_transform(self, mocker: MockerFixture) -> None:
        # arange
        def side_effect(df: pd.DataFrame, test_type: str,
                        question_format: str) -> pd.DataFrame:
            return df.append({"test_type": test_type,
                              "question_format": question_format},
                             ignore_index=True)

        input_df = pd.DataFrame(columns=["test_type", "question_format"])
        expected_df = pd.DataFrame({"test_type": ["general",
                                                  'general',
                                                  "specific",
                                                  'specific'],
                                    "question_format": ["objective",
                                                        "discursive",
                                                        "objective",
                                                        "discursive"]})

        mocker.patch("src.transformation.transform_abstract.Transform.transform_questions",
                     side_effect=side_effect)

        # execute
        transform = Transform2005()
        output_df = transform.transform(input_df)

        # assert
        assert output_df.equals(expected_df)
