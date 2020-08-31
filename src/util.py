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

def is_question_cancelled(id_question: str, df_enade: pd.DataFrame) -> bool:
    """Returns True if the question is cancelled and False otherwise.
    id_question is in the format:
        
        [D1, D5] for discursive questions
        [1, 35] for objective questions"""

    if "D" in id_question:
        if int(id_question[-1]) < 4:
            column_label = f"TP_SFG_{id_question}"
        else:
            column_label = f"TP_SCE_D{int(id_question[-1])-2}"
        var = df_enade[column_label].iloc[0]
        if var == 666:
            result = True
        else:
            result = False

    else:
        if int(id_question) < 9:
            column_label = "DS_VT_GAB_OFG_FIN"
            var = df_enade[column_label].str[int(id_question)-1]
        else:
            column_label = "DS_VT_GAB_OCE_FIN"
            var = df_enade[column_label].str[int(id_question)-9]

        if var.iloc[0] in ["Z", "X"]:
            result = True
        else:
            result = False
    return result
    


def get_subjects(df: pd.DataFrame) -> np.ndarray:
    """Returns a ndarray with the unique set of subjects used in test"""
    subjects = np.zeros(0)
    for i in range(1, 3+1):
        column = f"conteudo{i}"
        column_subjects = df[column].dropna().unique()
        subjects = np.union1d(subjects, column_subjects)
    return subjects

def is_question_of_subject(subject: str, row: pd.Series) -> bool:
    """Returns True if a row/question is of subject and 
    False otherwise"""
    boolean_array = row[["conteudo1", "conteudo2", "conteudo3"]] == subject
    return boolean_array.any()


#def get_questions(subject: str, df: pd.DataFrame) -> List[str]:
#    """Returns a list with ids of the questions that have 
#    the subject"""
#    result = []
#    for index, row in df.iterrows():
#        if is_question_subject(subject, row):
#            result.append(row["idquestao"])
#    return result

