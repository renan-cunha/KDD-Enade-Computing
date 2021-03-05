import os
from abc import ABC
import itertools
import pandas as pd
from typing import List, Tuple
import numpy as np
import sys
parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')) #this should give you absolute location of my_project folder.
sys.path.append(parent)
from src import config


BLANK_DISCURSIVE_ANSWER_CODE = 333
VALID_DISCURSIVE_ANSWER_CODE = [555, 336]

BLANK_OBJECTIVE_ANSWER_CODE = "."
DELETED_OBJECTIVE_ANSWER_CODE = "*"
CANCELLED_OBJECTIVE_ANSWER_CODE = ["8", "9"]
VALID_OBJECTIVE_ANSWER_CODE = ["A", "B", "C", "D", "E"]



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

    @staticmethod
    def get_score_column(id: int) -> str:
        return f"QUESTAO_{id}_NOTA"

    @staticmethod
    def get_answer_situation_column(id: int) -> str:
        return f"QUESTAO_{id}_SITUACAO_DA_RESPOSTA"

    @staticmethod
    def get_question_situation_column(id: int) -> str:
        return f"QUESTAO_{id}_SITUACAO_DA_QUESTAO"

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

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.transform_questions(df, "general", "objective")
        df = self.transform_questions(df, "general", "discursive")
        df = self.transform_questions(df, "specific", "objective")
        df = self.transform_questions(df, "specific", "discursive")
        return df

    def transform_questions(self, df: pd.DataFrame, test_type: str,
                            question_format: str) -> pd.DataFrame:
        """Creates columns 'QUESTAO_{id}_NOTA' for scores.

        Also Creates columns 'QUESTAO_{id}_SITUACAO'
        they can have the values "ok", "branco" and "rasura"

        And Creates columns 'QUESTAO_{id}_CANCELLED'
        that can have values of 1 or 0

        test_type is "general" or "specific"
        question_format is "discursive" or "objective"
        """
        if question_format not in Transform.type_format_questions:
            raise ValueError(f"question_format should be one of"
                             f" {Transform.type_format_questions}, not "
                             f"{question_format}")

        Transform.__verify_test_type(test_type)
        test_label = Transform.type_test_label[test_type]
        questions_ids, questions_labels = self.get_questions_ids_and_labels(
            test_type, question_format)

        for id, question_label in zip(questions_ids, questions_labels):
            if question_format == "discursive":
                df = Transform.__add_column_discursive_question(df,
                                                           id,
                                                           question_label,
                                                           test_label)
            else:
                df = Transform.__add_column_objective_question(df,
                                                          id,
                                                          question_label,
                                                          test_label)

        return df

    @staticmethod
    def __add_column_objective_question(df: pd.DataFrame, id: int,
                                        question_label: int,
                                        test_label: str) -> pd.DataFrame:
        df = Transform.__add_column_answer_situation_objective_question(df, id,
                                                                        question_label,
                                                                        test_label)
        df = Transform.__add_column_score_objective_question(df, id,
                                                        question_label,
                                                        test_label)
        df = Transform.__add_column_question_situation_objective_question(df, id,
                                                                          question_label,
                                                                          test_label)
        return df



    @staticmethod
    def __add_column_discursive_question(df: pd.DataFrame, id: int,
                                         question_label: int,
                                         test_label: str) -> pd.DataFrame:
        df = Transform.__add_column_answer_situation_discursive_question(
            df, id, question_label, test_label)
        df = Transform.__add_column_score_discursive_question(df, id,
                                                         question_label,
                                                         test_label)
        df = Transform.__add_column_question_situation_discursive_question(df, id)
        return df

    @staticmethod
    def __add_column_question_situation_discursive_question(df: pd.DataFrame,
                                                            id: int) -> pd.DataFrame:
        new_column_label = Transform.get_question_situation_column(id)
        answer_situation_column = Transform.get_answer_situation_column(id)
        df[new_column_label] = df[answer_situation_column]
        df.loc[~df[new_column_label].isna(), new_column_label] = 0
        df.loc[df[new_column_label].isna(), new_column_label] = 1
        return df

    @staticmethod
    def __add_column_question_situation_objective_question(df: pd.DataFrame, id: int,
                                                           question_label: int,
                                                           test_label: str) -> pd.DataFrame:
        new_column_label = Transform.get_question_situation_column(id)
        df[new_column_label] = df[f"DS_VT_ACE_O{test_label}"].str[
            question_label]
        if (df[new_column_label].isin(CANCELLED_OBJECTIVE_ANSWER_CODE)).any():
            df[new_column_label] = 1
        else:
            df[new_column_label] = 0
        return df


    @staticmethod
    def __add_column_score_discursive_question(df: pd.DataFrame, id: int,
                                               question_label: int,
                                               test_label: str) -> pd.DataFrame:
        score_column = f"NT_{test_label}_D{question_label}"
        new_score_column = Transform.get_score_column(id)
        df[new_score_column] = df[score_column]
        answer_situation_column = Transform.get_answer_situation_column(id)
        index = (df[answer_situation_column].isna())
        df.loc[index, new_score_column] = np.nan
        return df

    @staticmethod
    def __add_column_answer_situation_discursive_question(df: pd.DataFrame, id: int,
                                                          question_label: int,
                                                          test_label: str) -> pd.DataFrame:
        situation_column = f"TP_S{test_label}_D{question_label}"
        new_situation_column = Transform.get_answer_situation_column(id)
        df[new_situation_column] = df[situation_column]
        df[new_situation_column] = df[new_situation_column].replace(BLANK_DISCURSIVE_ANSWER_CODE,
                                                                config.BLANK_ANSWER_LABEL)
        df[new_situation_column] = df[new_situation_column].replace(VALID_DISCURSIVE_ANSWER_CODE,
                                                                    config.VAlID_ANSWER_LABEL)

        def num_to_nan(x: object) -> object:
            if type(x) == int or type(x) == float:
                return np.nan
            else:
                return x

        df[new_situation_column] = df[new_situation_column].apply(num_to_nan)
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

    @staticmethod
    def __add_column_score_objective_question(df: pd.DataFrame,
                                              id: int,
                                              question_label: int,
                                              test_label: str) -> pd.DataFrame:
        new_column_label = Transform.get_score_column(id)
        df[new_column_label] = df[f"DS_VT_ACE_O{test_label}"].str[
            question_label]
        df[new_column_label] = df[new_column_label].replace(BLANK_OBJECTIVE_ANSWER_CODE, "0")
        df[new_column_label] = df[new_column_label].replace(CANCELLED_OBJECTIVE_ANSWER_CODE, np.nan)
        df[new_column_label] = df[new_column_label].astype(float)
        df[new_column_label] *= 100
        return df

    @staticmethod
    def __add_column_answer_situation_objective_question(df: pd.DataFrame,
                                                         id: int,
                                                         question_label: int,
                                                         test_label: str) -> pd.DataFrame:
        new_column_label = Transform.get_answer_situation_column(id)
        df[new_column_label] = df[f"DS_VT_ESC_O{test_label}"].str[question_label]
        df[new_column_label] = df[new_column_label].replace(BLANK_OBJECTIVE_ANSWER_CODE,
                                                        config.BLANK_ANSWER_LABEL)
        df[new_column_label] = df[new_column_label].replace(VALID_OBJECTIVE_ANSWER_CODE,
                                                        config.VAlID_ANSWER_LABEL)
        df[new_column_label] = df[new_column_label].replace(DELETED_OBJECTIVE_ANSWER_CODE,
                                                            config.DELETION_ANSWER_LABEL)
        return df


