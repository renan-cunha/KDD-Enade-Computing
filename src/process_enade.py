from typing import List, Callable
import pandas as pd
from abc import ABC, abstractmethod
from src.config import NUM_ENADE_EXAM_QUESTIONS, PRESENCE_COLUMN, CODE_COURSE, \
    ENADE_DATA_DIR, CODE_BLANK_DIS_ANSWER, CODE_CANCELLED_DIS_QUESTION, \
    BLANK_LABEL, CANCELLED_LABEL, DELETION_LABEL, CODE_CANCELLED_OBJ_QUESTION, \
    SENIOR_STUDENT_CODE
import os


def filter_enade_df_by_course(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[df["CO_CURSO"] == CODE_COURSE]


def filter_senior_students(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[df["IN_GRAD"] == SENIOR_STUDENT_CODE]


def get_recent_enade_dir(year: int) -> str:
    """Used for enade 2017, 2014 and 2011"""
    return os.path.join(ENADE_DATA_DIR, f"enade{year}", "3.DADOS",
                        f"MICRODADOS_ENADE_{year}.txt")


def get_old_enade_dir(year: int) -> str:
    """Used for enade 2005 and 2008"""
    return os.path.join(ENADE_DATA_DIR, f"enade{year}", "2.DADOS",
                        f"microdados_enade_{year}.csv")


def pre_process_old(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [x.upper() for x in df.columns]
    columns_to_rename = ["VT_ESC_OFG", "VT_ESC_OCE", "VT_ACE_OCE",
                         "VT_ACE_OFG"]
    df[[f"DS_{x}" for x in columns_to_rename]] = df[columns_to_rename]
    return df


class ProcessEnade(ABC):

    GEN_DIS_QUESTIONS_ID = [0]
    GEN_DIS_QUESTIONS_LABEL = [0]

    SPE_DIS_QUESTIONS_ID = [0]
    SPE_DIS_QUESTIONS_LABEL = [0]

    GEN_OBJ_QUESTIONS_ID = [0]
    GEN_OBJ_QUESTIONS_LABEL = [0]

    SPE_OBJ_QUESTIONS_ID = [0]
    SPE_OBJ_QUESTIONS_LABEL = [0]
    path_csv = ""

    @abstractmethod
    def read_csv(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def pre_process(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    @staticmethod
    def filter_columns_enade(df: pd.DataFrame) -> pd.DataFrame:
        question_columns = [f"QUESTAO_{i}_NOTA" for i in range(1,
                                                               NUM_ENADE_EXAM_QUESTIONS + 1)]
        status_columns = [f"QUESTAO_{i}_STATUS" for i in range(1,
                                                               NUM_ENADE_EXAM_QUESTIONS + 1)]
        columns = question_columns + [PRESENCE_COLUMN] + status_columns
        return df[columns]

    def get_discursive_scores(self, df: pd.DataFrame, general: bool) -> pd.DataFrame:
        """Creates columns for the discursive part of the test. Columns such as
            'QUESTAO_{id}_NOTA' for the score and 'QUESTAO_{id}_STATUS' that states
            if the question was cancelled"""
        test_label = "FG" if general else "CE"
        questions_id = self.GEN_DIS_QUESTIONS_ID if general else self.SPE_DIS_QUESTIONS_ID
        questions_label = self.GEN_DIS_QUESTIONS_LABEL if general else self.SPE_DIS_QUESTIONS_LABEL

        for id, question_label in zip(questions_id, questions_label):
            new_column_label = f"QUESTAO_{id}_NOTA"

            df[new_column_label] = df[f"NT_{test_label}_D{question_label}"]

            situation_label = f"TP_S{test_label}_D{question_label}"
            blank_indices = df[situation_label] == CODE_BLANK_DIS_ANSWER
            cancelled_indices = df[situation_label] == CODE_CANCELLED_DIS_QUESTION

            df.loc[blank_indices, new_column_label] = BLANK_LABEL

            status_column = f"QUESTAO_{id}_STATUS"
            df.loc[cancelled_indices, status_column] = CANCELLED_LABEL

            df.loc[~cancelled_indices, status_column] = "OK"

        return df

    def get_objective_scores(self, df: pd.DataFrame, general: bool) -> pd.DataFrame:
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
                                                               new_column_label].astype(float)*100

            blank_index = df.loc[:, f"DS_VT_ESC_O{test_label}"].str[question_label] == "."
            df.loc[blank_index, new_column_label] = BLANK_LABEL

            deletion_index = df.loc[:, f"DS_VT_ESC_O{test_label}"].str[question_label] == "*"
            df.loc[deletion_index, new_column_label] = DELETION_LABEL

            first_code, second_code = CODE_CANCELLED_OBJ_QUESTION
            arg1 = df.loc[:, f"DS_VT_ACE_O{test_label}"].str[question_label] == first_code
            arg2 = df.loc[:, f"DS_VT_ACE_O{test_label}"].str[question_label] == second_code
            cancelled_index = arg1 | arg2
            df.loc[cancelled_index, f"QUESTAO_{id}_STATUS"] = CANCELLED_LABEL
            df.loc[~cancelled_index, f"QUESTAO_{id}_STATUS"] = "OK"

        return df

    def get_data(self) -> pd.DataFrame:

        df = self.read_csv()
        df = self.pre_process(df)

        df = self.get_objective_scores(df, general=True)
        df = self.get_discursive_scores(df, general=True)
        df = self.get_discursive_scores(df, general=False)
        df = self.get_objective_scores(df, general=False)

        return self.filter_columns_enade(df)
