import pandas as pd
import numpy as np
from src.config import NUM_ENADE_EXAM_QUESTIONS, MAX_SUBJECTS_BY_QUESTION,\
    SUBJECT_DF_PATH, SUBJECT_CONTENT_COLUMNS
from typing import List

# This file deals with the csv about the questions


def split_general_subjects(df: pd.DataFrame) -> None:
    general_questions_index = df["prova"] == "Geral"

    if df.dtypes["objeto"] != object:
        raise ValueError("The column 'objeto' should have dtype "
                         "of 'objetct'")

    new_data = df.loc[general_questions_index, "objeto"].str.split(";",
                                                                   expand=True)
    num_columns = new_data.shape[1]
    if num_columns < 3:
        # add nan columns to match 3 columns in total
        new_data[[x for x in range(num_columns, 3)]] = np.nan

    if new_data.shape[1] != 3:
        raise ValueError(f"The 'objeto' column should have a maximum of 3 subjects "
                         f", instead it has {new_data.shape[1]}")

    df.loc[general_questions_index,
           SUBJECT_CONTENT_COLUMNS] = new_data.values


def get_processed_subject_df(include_general_subjects: bool = False) -> pd.DataFrame:
    """Gets a clean DataFrame about the questions of ENADE, with columns such as
       questionID, year, TypeQuestion, TypeContent, content1, content2, content3"""

    df = pd.read_csv(SUBJECT_DF_PATH)

    if include_general_subjects:
        split_general_subjects(df)

    # capitalize and remove final spaces and dots in contents
    for column_label in SUBJECT_CONTENT_COLUMNS:
        df[column_label] = df[column_label].str.capitalize()
        df[column_label] = df[column_label].str.replace(".", "")
        df[column_label] = df[column_label].str.strip(" ")

    # fix ID so questionID is between 1-40
    num_questions = df.shape[0]

    if num_questions % NUM_ENADE_EXAM_QUESTIONS != 0:
        raise ValueError(f"The number of questions should be divisible by "
                         f"{NUM_ENADE_EXAM_QUESTIONS}. Instead, the number of "
                         f"questions is {num_questions}")

    questions_id = np.linspace(0, num_questions - 1, num_questions).astype(int)
    questions_id = questions_id % NUM_ENADE_EXAM_QUESTIONS + 1
    df['idquestao'] = questions_id

    # remove last line of csv because is has some typos
    return df.iloc[:-1][["idquestao", "ano", "curso", "prova", "tipoquestao",
                         "conteudo1", "conteudo2", "conteudo3"]]


def get_objective_questions(subject_df: pd.DataFrame) -> List[int]:
    return subject_df.loc[subject_df["tipoquestao"]=="Objetiva",
                          "idquestao"].tolist()
