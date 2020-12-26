from abc import ABC
import itertools
import pandas as pd
from typing import List, Tuple
import numpy as np
from src import config

BLANK_DISCURSIVE_ANSWER_CODE = 333
CANCELLED_DISCURSIVE_ANSWER_CODE = 335
VALID_DISCURSIVE_ANSWER_CODE = 555

BLANK_OBJECTIVE_ANSWER_CODE = "."
DELETED_OBJECTIVE_ANSWER_CODE = "*"
CANCELLED_OBJECTIVE_ANSWER_CODE = ["8", "9"]
VALID_OBJECTIVE_ANSWER_CODE = ["1", "0"]


class Transform(ABC):

    type_test_questions = ["general", "specific"]
    type_format_questions = ["objective", "discursive"]
    type_data_questions = ["id", "label"]
    type_test_label = {"general": "FG",
                       "specific": "CE"}

    tuples = itertools.product(type_test_questions,
                               type_format_questions,
                               type_data_questions)

    index = pd.MultiIndex.from_tuples(tuples, names=["test_type",
                                                     "format",
                                                     "data_type"])

    def __init__(self):
        self.questions_series = pd.Series(index=Transform.index,
                                          dtype=object)
        self.questions_series['general', 'objective', 'id'] = self.general_objective_questions_ids
        self.questions_series['general', 'objective', 'label'] = self.general_objective_questions_labels
        self.questions_series['general', 'discursive', 'id'] = self.general_discursive_questions_ids
        self.questions_series['general', 'discursive', 'label'] = self.general_discursive_questions_labels

        self.questions_series['specific', 'objective', 'id'] = self.specific_objective_questions_ids
        self.questions_series['specific', 'objective', 'label'] = self.specific_objective_questions_labels
        self.questions_series['specific', 'discursive', 'id'] = self.specific_discursive_questions_ids
        self.questions_series['specific', 'discursive', 'label'] = self.specific_discursive_questions_labels

    @property
    def general_discursive_questions_ids(self) -> List[int]:
        raise NotImplementedError

    @property
    def general_discursive_questions_labels(self) -> List[int]:
        raise NotImplementedError

    @property
    def general_objective_questions_ids(self) -> List[int]:
        raise NotImplementedError

    @property
    def general_objective_questions_labels(self) -> List[int]:
        raise NotImplementedError

    @property
    def specific_discursive_questions_ids(self) -> List[int]:
        raise NotImplementedError

    @property
    def specific_discursive_questions_labels(self) -> List[int]:
        raise NotImplementedError

    @property
    def specific_objective_questions_ids(self) -> List[int]:
        raise NotImplementedError

    @property
    def specific_objective_questions_labels(self) -> List[int]:
        raise NotImplementedError

    def transform_discursive_questions(self, df: pd.DataFrame,
                                       test_type: str) -> pd.DataFrame:
        """Creates columns 'QUESTAO_{id}_nota' for scores in the discursive
        part of the test.

        Also Creates columns 'QUESTAO_{id}_SITUATION' for discursive questions,
        they can have the values "ok" and "branco"

        test_type is "general" or "specific"
        """
        Transform.__verify_test_type(test_type)
        test_label = Transform.type_test_label[test_type]
        questions_ids, questions_labels = self.get_questions_ids_and_labels(
            test_type, "discursive")

        # score columns
        score_columns= [f"NT_{test_label}_D{x}" for x in questions_labels]
        new_score_columns = [f"QUESTAO_{x}_NOTA" for x in questions_ids]
        df[new_score_columns] = df[score_columns]

        # situation columns
        situation_columns = [f"TP_S{test_label}_D{x}" for x in questions_labels]
        new_situation_columns = [f"QUESTAO_{x}_SITUACAO" for x in questions_ids]
        df[new_situation_columns] = df[situation_columns]
        df[new_situation_columns] = df[situation_columns].replace({BLANK_DISCURSIVE_ANSWER_CODE: config.BLANK_ANSWER_LABEL,
                                                                   CANCELLED_DISCURSIVE_ANSWER_CODE: np.nan,
                                                                   VALID_DISCURSIVE_ANSWER_CODE: config.VAlID_ANSWER_LABEL})

        for score_column, situation_column in zip(new_score_columns,
                                                  new_situation_columns):
            index = (df[situation_column].isna())
            df.loc[index, score_column] = np.nan

        return df

    def get_questions_ids_and_labels(self, test_type: str,
                                     question_format: str) -> Tuple[List[int],
                                                                      List[int]]:
        questions = self.questions_series.xs(question_format, level="format")
        questions_type_test = questions.xs(test_type, level="test_type")
        questions_ids = questions_type_test["id"]
        questions_labels = questions_type_test["label"]
        return questions_ids, questions_labels

    @staticmethod
    def __verify_test_type(test_type: str) -> None:
        test_type_options = ['general', 'specific']
        if test_type not in test_type_options:
            raise ValueError(f"test_type param should be one of "
                             f"{test_type_options}, not {test_type}")

    def transform_objective_questions(self, df:pd.DataFrame,
                                     test_type: str) -> pd.DataFrame:
        """Creates columns 'QUESTAO_{id}_NOTA' for objective questions, they
        can have the values 0 (wrong alternative), 100 (correct).

        Also Creates columns 'QUESTAO_{id}_SITUATION' for objective questions,
        they can have the values "ok", "branco" and "rasura"

        test_type param can be "general" or "specific"
         """

        Transform.__verify_test_type(test_type)
        test_label = Transform.type_test_label[test_type]
        questions_ids, questions_labels = self.get_questions_ids_and_labels(
            test_type, "objective")

        for id, question_label in zip(questions_ids, questions_labels):
            Transform.__add_column_score_objective_question(df, id, question_label, test_label)
            Transform.__add_column_situation_objective_question(df, id, question_label, test_label)

        return df

    @staticmethod
    def __add_column_score_objective_question(df: pd.DataFrame,
                                              id: int,
                                              question_label: int,
                                              test_label: str) -> pd.DataFrame:
        new_column_label = f"QUESTAO_{id}_NOTA"
        df[new_column_label] = df[f"DS_VT_ACE_O{test_label}"].str[
            question_label]
        df[new_column_label] = df[new_column_label].replace([BLANK_OBJECTIVE_ANSWER_CODE,
                                                             DELETED_OBJECTIVE_ANSWER_CODE], "0")
        df[new_column_label] = df[new_column_label].replace(CANCELLED_OBJECTIVE_ANSWER_CODE,
                                                            np.nan)
        df[new_column_label] = df[new_column_label].astype(float)
        df[new_column_label] *= 100
        return df

    @staticmethod
    def __add_column_situation_objective_question(df: pd.DataFrame,
                                                  id: int,
                                                  question_label: int,
                                                  test_label: str) -> pd.DataFrame:
        new_column_label = f"QUESTAO_{id}_SITUACAO"
        df[new_column_label] = df[f"DS_VT_ACE_O{test_label}"].str[
            question_label]
        df[new_column_label] = df[new_column_label].replace(VALID_OBJECTIVE_ANSWER_CODE,
                                                            config.VAlID_ANSWER_LABEL)
        df[new_column_label] = df[new_column_label].replace(DELETED_OBJECTIVE_ANSWER_CODE,
                                                            config.DELETION_ANSWER_LABEL)
        df[new_column_label] = df[new_column_label].replace(CANCELLED_OBJECTIVE_ANSWER_CODE,
                                                            np.nan)
        df[new_column_label] = df[new_column_label].replace(BLANK_OBJECTIVE_ANSWER_CODE,
                                                            config.BLANK_ANSWER_LABEL)
        return df

