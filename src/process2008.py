import pandas as pd
from src.config import CODE_BLANK_DIS_ANSWER, CODE_CANCELLED_DIS_QUESTION
from src.config import BLANK_LABEL, CANCELLED_LABEL, DELETION_LABEL
from src.config import CODE_CANCELLED_OBJ_QUESTION, CODE_COURSE, \
    NUM_ENADE_EXAM_QUESTIONS, PRESENCE_COLUMN
from typing import Tuple


NUM_DIS_GEN_QUESTIONS = 2
NUM_OBJ_GEN_QUESTIONS = 8
NUM_DIS_SPE_QUESTIONS = 3
NUM_OBJ_SPE_QUESTIONS = 27


def filter_enade_df_by_course(df: pd.DataFrame) -> pd.DataFrame:
    df = df.loc[df["co_curso"] == CODE_COURSE]
    df = df.loc[df["in_grad"] == 0]
    print(df.shape)
    return df


def get_processed_enade_2008(path_csv: str) -> Tuple[pd.DataFrame,
                                                     pd.DataFrame]:
    df = pd.read_csv(path_csv, sep=";", decimal=",",
                              dtype={"vt_esc_ofg": str,
                                     "vt_esc_oce": str,
                                     "vt_ace_oce": str,
                                     "vt_ace_ofg": str,
                                     "nt_obj_ce": str})
    df = filter_enade_df_by_course(df)



    df = get_objective_scores(df, general=True)
    df = get_discursive_scores(df, general=True)
    df = get_discursive_scores(df, general=False)
    df = get_objective_scores(df, general=False)

    question_columns = [f"QUESTAO_{i}_NOTA" for i in range(1,
                                                           NUM_ENADE_EXAM_QUESTIONS+1)]
    status_columns = [f"QUESTAO_{i}_STATUS" for i in range(1,
                                                           NUM_ENADE_EXAM_QUESTIONS+1)]
    columns = question_columns + ["tp_pres"] + status_columns
    return df[columns].copy(), df

    
def get_discursive_scores(df: pd.DataFrame, general: bool) -> pd.DataFrame:
    """Creates columns for the discursive part of the test"""
    
    general_indexes = [9, 10]
    specific_indexes = [20, 39, 40]
    label = "fg" if general else "ce"
    indexes = general_indexes if general else specific_indexes

    for discursive_question_index, i in enumerate(indexes):
        new_column_label = f"QUESTAO_{i}_NOTA"
        
        discursive_question_index += 1
        df[new_column_label] = df[f"nt_{label}_d{discursive_question_index}"].copy()

        question_situation_label = f"tp_s{label}_d{discursive_question_index}"
        blank_indices = df[question_situation_label] == CODE_BLANK_DIS_ANSWER
        cancelled_indices = df[question_situation_label] == CODE_CANCELLED_DIS_QUESTION

        df.loc[blank_indices, new_column_label] = BLANK_LABEL
        df.loc[cancelled_indices, f"QUESTAO_{i}_STATUS"] = CANCELLED_LABEL
        df.loc[~cancelled_indices, f"QUESTAO_{i}_STATUS"] = "OK"

    return df


def get_objective_scores(df: pd.DataFrame, general: bool) -> pd.DataFrame:
    """Creates columns for the objective part of the exam. Each column
    can have the values 0 (wrong alternative), 100 (correct), BRANCO, RASURA and 
    NULA"""

    general_indexes = list(range(1, 8 + 1))
    specific_indexes = list(range(11, 20)) + list(range(21, 38 + 1))
    label = "fg" if general else "ce"
    indexes = general_indexes if general else specific_indexes
    for question_index, i in enumerate(indexes):
        
        new_column_label = f"QUESTAO_{i}_NOTA"
        df.loc[:, new_column_label] = df.loc[:, f"vt_ace_o{label}"].str[question_index].copy()
        df.loc[:, new_column_label] = df.loc[:, new_column_label].astype(float) * 100

        blank_index = df.loc[:, f"vt_esc_o{label}"].str[question_index] == "."
        df.loc[blank_index, new_column_label] = BLANK_LABEL

        deletion_index = df.loc[:, f"vt_esc_o{label}"].str[question_index] == "*"
        df.loc[deletion_index, new_column_label] = DELETION_LABEL

        arg1 = df.loc[:, f"vt_ace_o{label}"].str[question_index] == 8
        arg2 = df.loc[:, f"vt_ace_o{label}"].str[question_index] == 9
        cancelled_index = arg1 | arg2
        df.loc[cancelled_index, f"QUESTAO_{i}_STATUS"] = CANCELLED_LABEL
        df.loc[~cancelled_index, f"QUESTAO_{i}_STATUS"] = "OK"

    return df

