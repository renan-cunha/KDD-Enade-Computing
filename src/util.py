import pandas as pd
from typing import Union
import numpy as np


def add_correct_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona uma nova coluna no DataFrame para cada questão objetiva.
    True indica que a questão foi acertada, False indica o contrário. 
    NaN indica que a questão foi anulada"""

    
    def return_var(df_true: pd.DataFrame, df_marked: pd.DataFrame,
                   index: int, offset: int) -> Union[str, bool]:
        df_true_question = df_true.str[i - offset]
        df_marked_question = df_marked.str[i - offset]
        if df_true_question.iloc[0] in ["Z", "X"]:
            return ["NaN"] * df_true.shape[0]
        else:
            return df_true_question == df_marked_question
    
    
    used_columns = ["DS_VT_GAB_OFG_FIN", "DS_VT_GAB_OCE_FIN",
                    "DS_VT_ESC_OFG", "DS_VT_ESC_OCE"]
    

    for column in used_columns:
        if column not in df.columns:
            raise ValueError(f"A {column} não está no DataFrame")

    general_answer_key = df[used_columns[0]]
    specific_answer_key = df[used_columns[1]]
    
    general_marked = df[used_columns[2]]
    specific_marked = df[used_columns[3]]
    
    for i in range(1, 35 + 1):
        if i < 9: # Indica que a questão é da formação geral
            var = return_var(general_answer_key, general_marked, i, 
                             offset = 1)
        else:
            var = return_var(specific_answer_key, specific_marked, i,
                             offset = 9)
        df.loc[:, f"QUESTAO_OBJ_{i}_ACERTO"] = var
    return df


def get_subjects(df: pd.DataFrame) -> np.ndarray:
    """Returns a ndarray with the unique set of subjects used in test"""
    subjects = np.zeros(0)
    for i in range(1, 3+1):
        column = f"conteudo{i}"
        column_subjects = df[column].dropna().unique()
        subjects = np.union1d(subjects, column_subjects)
    return subjects

