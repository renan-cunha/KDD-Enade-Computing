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
                                    general: bool) -> pd.DataFrame:
        """Creates columns 'QUESTAO_{id}_nota' for scores in the discursive
        part of the test."""
        type_test_question = "general" if general else "specific"

        discursive_questions = self.questions_series.xs("discursive",
                                                        level="format")
        discursive_questions_type_test = discursive_questions.xs(
            type_test_question, level="test_type")

        questions_ids = discursive_questions_type_test["id"]
        questions_labels = discursive_questions_type_test["label"]

        test_label = Transform.type_test_label[type_test_question]

        score_labels = [f"NT_{test_label}_D{x}" for x in questions_labels]
        new_columns_labels = [f"QUESTAO_{x}_NOTA" for x in questions_ids]

        df[new_columns_labels] = df[score_labels]
        return df
    """

    def get_objective_scores(self, df: pd.DataFrame, general: bool) -> pd.DataFrame:
        "Creates columns for the objective part of the exam. Each column 'QUESTAO_{id}_NOTA'
        can have the values 0 (wrong alternative), 100 (correct).
        Columns such as 'QUESTAO_{id}_STATUS' can have values such as OK and RASURA"

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

    @abstractmethod
    def filter_enade_df_by_course(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    def filter_anomalies(self, df: pd.DataFrame) -> pd.DataFrame:
        "This function filters the students that were present but have
        missing values"
        arg1 = df["DS_VT_ESC_OCE"].isna()
        arg2 = df["TP_PRES"] == 555
        boolean_index = ~(arg1 & arg2)
        return df.loc[boolean_index]

    def get_data(self, filter_by_ufpa: bool = True) -> pd.DataFrame:

        df = self.read_csv()
        df = self.pre_process(df)
        if filter_by_ufpa:
            df = filter_enade_df_by_ufpa_course(df)
        else:
            df = self.filter_enade_df_by_course(df)
            df = self.filter_anomalies(df)

        df = self.get_objective_scores(df, general=True)
        df = self.preprocess_discursive_scores(df, general=True)
        df = self.preprocess_discursive_scores(df, general=False)
        df = self.get_objective_scores(df, general=False)

        return self.filter_columns_enade(df)
    """
