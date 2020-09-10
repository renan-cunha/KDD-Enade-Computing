import pandas as pd
from src.config import CODE_BLANK_DIS_ANSWER, CODE_CANCELLED_DIS_QUESTION
from src.config import BLANK_LABEL, CANCELLED_LABEL, DELETION_LABEL
from src.config import CODE_CANCELLED_OBJ_QUESTION, CODE_COURSE, \
    NUM_ENADE_EXAM_QUESTIONS, PRESENCE_COLUMN


NUM_DIS_GEN_QUESTIONS = 2
NUM_OBJ_GEN_QUESTIONS = 8
NUM_DIS_SPE_QUESTIONS = 3
NUM_OBJ_SPE_QUESTIONS = 27


def filter_enade_df_by_course(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[df["CO_CURSO"] == CODE_COURSE]


def get_processed_enade_2014_2017(path_csv: str) -> pd.DataFrame:
    df = pd.read_csv(path_csv, sep=";", decimal=",",
                              dtype={"DS_VT_ESC_OFG": str, 
                                     "DS_VT_ESC_OCE": str,
                                     "DS_VT_ACE_OCE": str,
                                     "DS_VT_ACE_OFG": str})
    df = filter_enade_df_by_course(df)
    # get discursive general scores
    df = get_discursive_scores(df, general=True)
    
    # get objective general scores
    df = get_objective_scores(df, general=True)

    # get discursive specific questions
    df = get_discursive_scores(df, general=False)

    # get objective specific questions
    df = get_objective_scores(df, general=False)

    question_columns = [f"QUESTAO_{i}_NOTA" for i in range(1,
                                                           NUM_ENADE_EXAM_QUESTIONS+1)]
    status_columns = [f"QUESTAO_{i}_STATUS" for i in range(1,
                                                           NUM_ENADE_EXAM_QUESTIONS+1)]
    columns = question_columns + [PRESENCE_COLUMN] + status_columns

    return df[columns]

    
def get_discursive_scores(df: pd.DataFrame, general: bool) -> pd.DataFrame:
    """Creates columns for the discursive part of the test"""
    
    start_id = 1 if general else 11
    num_questions = NUM_DIS_GEN_QUESTIONS if general else NUM_DIS_SPE_QUESTIONS
    label = "FG" if general else "CE"

    for i in range(start_id, num_questions + start_id):
        new_column_label = f"QUESTAO_{i}_NOTA"
        
        discursive_question_index = i - start_id + 1
        df[new_column_label] = df[f"NT_{label}_D{discursive_question_index}"]

        question_situation_label = f"TP_S{label}_D{discursive_question_index}"
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
    start_id = 3 if general else 14
    num_questions = NUM_OBJ_GEN_QUESTIONS if general else NUM_OBJ_SPE_QUESTIONS
    label = "FG" if general else "CE"
    for i in range(start_id, num_questions + start_id):

        new_column_label = f"QUESTAO_{i}_NOTA"
        question_index = i - start_id
        df.loc[:, new_column_label] = df.loc[:, f"DS_VT_ACE_O{label}"].str[question_index]
        df.loc[:, new_column_label] = df.loc[:, new_column_label].astype(float) * 100

        blank_index = df.loc[:, f"DS_VT_ESC_O{label}"].str[question_index] == "."
        df.loc[blank_index, new_column_label] = BLANK_LABEL

        deletion_index = df.loc[:, f"DS_VT_ESC_O{label}"].str[question_index] == "*"
        df.loc[deletion_index, new_column_label] = DELETION_LABEL

        first_code, second_code, third_code = CODE_CANCELLED_OBJ_QUESTION
        arg1 = df.loc[:, f"DS_VT_GAB_O{label}_FIN"].str[question_index] == first_code
        arg2 = df.loc[:, f"DS_VT_GAB_O{label}_FIN"].str[question_index] == second_code
        arg3 = df.loc[:, f"DS_VT_GAB_O{label}_FIN"].str[question_index] == third_code
        cancelled_index = arg1 | arg2 | arg3
        df.loc[cancelled_index, f"QUESTAO_{i}_STATUS"] = CANCELLED_LABEL
        df.loc[~cancelled_index, f"QUESTAO_{i}_STATUS"] = "OK"

    return df

