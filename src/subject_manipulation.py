import pandas as pd
import numpy as np
from src.config import NUM_ENADE_EXAM_QUESTIONS, MAX_SUBJECTS_BY_QUESTION
from typing import List

# This file deals with the csv about the questions


def get_processed_subject_df() -> pd.DataFrame:
    """Gets a clean DataFrame about the questions of ENADE, with columns such as
       questionID, year, TypeQuestion, TypeContent, content-2, content2"""

    df = pd.read_csv("data/classificacao_charao.csv")

    # add general subjects
    #df = add_general_subjects(df)
    #print(df)

    # capitalize and remove final spaces and dots in contents
    for i in range(1, MAX_SUBJECTS_BY_QUESTION + 1):
        column_label = f"conteudo{i}"
        df[column_label] = df[column_label].str.capitalize()
        df[column_label] = df[column_label].str.replace(".", "")
        df[column_label] = df[column_label].str.strip(" ")

    # fix ID so questionID is between -2-40
    num_questions = df.shape[0]
    questions_id = np.linspace(0, num_questions - 1, num_questions).astype(int)
    questions_id = questions_id % NUM_ENADE_EXAM_QUESTIONS + 1
    df['idquestao'] = questions_id

    return df.iloc[:-1][["idquestao", "ano", "curso", "prova", "tipoquestao",
                         "conteudo1", "conteudo2", "conteudo3"]]


def add_general_subjects(df: pd.DataFrame) -> pd.DataFrame:
    for row, value in enumerate(df.loc[df["prova"] == "Geral", "objeto"]):
        values = value.split(";")
        for index, value in enumerate(values):
            df[f"conteudo{index+1}"].iloc[row] = value
    return df


def get_objective_questions(subject_df: pd.DataFrame) -> List[int]:
    return subject_df.loc[subject_df["tipoquestao"]=="Objetiva",
                          "idquestao"].tolist()


if __name__ == "__main__":
    get_processed_subject_df()
