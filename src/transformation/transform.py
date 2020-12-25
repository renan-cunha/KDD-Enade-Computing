from abc import ABC, abstractmethod
import itertools
import pandas as pd
from typing import List


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

    def transform_discursive_scores(self, df: pd.DataFrame,
                                    test_type: str) -> pd.DataFrame:
        """Creates columns 'QUESTAO_{id}_nota' for scores in the discursive
        part of the test.

            test_type is "general" or "specific"
        """
        Transform.__verify_test_type(test_type)

        discursive_questions = self.questions_series.xs("discursive",
                                                        level="format")
        discursive_questions_type_test = discursive_questions.xs(
            test_type, level="test_type")

        questions_ids = discursive_questions_type_test["id"]
        questions_labels = discursive_questions_type_test["label"]

        test_label = Transform.type_test_label[test_type]

        score_labels = [f"NT_{test_label}_D{x}" for x in questions_labels]
        new_columns_labels = [f"QUESTAO_{x}_NOTA" for x in questions_ids]

        df[new_columns_labels] = df[score_labels]
        return df

    @staticmethod
    def __verify_test_type(test_type: str) -> None:
        test_type_options = ['general', 'specific']
        if test_type not in test_type_options:
            raise ValueError(f"test_type param should be one of "
                             f"{test_type_options}, not {test_type}")

    def get_objective_scores(self, df: pd.DataFrame, mode: bool) -> pd.DataFrame:
        """Creates columns for the objective part of the exam. Each column 'QUESTAO_{id}_NOTA'
        can have the values 0 (wrong alternative), 100 (correct).
        Columns such as 'QUESTAO_{id}_STATUS' can have values such as OK and RASURA"""

        test_label = "FG" if general else "CE"
        questions_id = self.GEN_OBJ_QUESTIONS_ID if general else self.SPE_OBJ_QUESTIONS_ID
        questions_label = self.GEN_OBJ_QUESTIONS_LABEL if general else self.SPE_OBJ_QUESTIONS_LABEL
        for id, question_label in zip(questions_id, questions_label):

            new_column_label = f"QUESTAO_{id}_NOTA"
            df.loc[:, new_column_label] = df.loc[:, f"DS_VT_ACE_O{test_label}"].str[question_label]
            digit_index = df.loc[:, new_column_label] == "1"
            if digit_index.any():
                df.loc[digit_index, new_column_label] = df.loc[digit_index,
                                                               new_column_label].astype(int)*100

            first_code, second_code = CODE_CANCELLED_OBJ_QUESTION
            arg1 = df.loc[:, f"DS_VT_ACE_O{test_label}"].str[question_label] == first_code
            arg2 = df.loc[:, f"DS_VT_ACE_O{test_label}"].str[question_label] == second_code
            cancelled_index = arg1 | arg2
            df.loc[cancelled_index, f"QUESTAO_{id}_STATUS"] = CANCELLED_LABEL
            df.loc[~cancelled_index, f"QUESTAO_{id}_STATUS"] = "OK"
            df.loc[cancelled_index, new_column_label] = CANCELLED_LABEL

            blank_index = df.loc[:, f"DS_VT_ESC_O{test_label}"].str[question_label] == "."
            df.loc[blank_index, new_column_label] = BLANK_LABEL

            deletion_index = df.loc[:, f"DS_VT_ESC_O{test_label}"].str[question_label] == "*"
            df.loc[deletion_index, new_column_label] = DELETION_LABEL

        return df