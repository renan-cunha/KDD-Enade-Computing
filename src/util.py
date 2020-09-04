import pandas as pd
from typing import Union, List
import numpy as np
from src.config import NUM_ENADE_EXAM_QUESTIONS, MAX_SUBJECTS_BY_QUESTION



def get_processed_subject_df() -> pd.DataFrame:
    """Gets a clean DataFrame about the questions of ENADE, with columns such as
       questionID, year, TypeQuestion, TypeContent, content1, content2"""

    df = pd.read_csv("data/classificacao_charao.csv")

    # remove spaces in contents
    for i in range(1, MAX_SUBJECTS_BY_QUESTION + 1):
        column_label = f'conteudo{i}'
        df[column_label] = df[column_label].str.replace(" ", "")

    # fix ID so questionID is between 1-40
    num_questions = df.shape[0]
    questions_id = np.linspace(0, num_questions-1, num_questions).astype(int) 
    questions_id = questions_id % NUM_ENADE_EXAM_QUESTIONS + 1
    df['idquestao'] = questions_id

    return df.iloc[:-1][["idquestao", "ano", "curso", "prova", "tipoquestao", 
                        "conteudo1", "conteudo2", "conteudo3"]]



def add_columns_objective_score(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona uma nova coluna no DataFrame para cada questão objetiva.
    True indica que a questão foi acertada, False indica o contrário. 
    NaN indica que a questão foi anulada"""

    
    def return_var(df_true: pd.DataFrame, df_marked: pd.DataFrame,
                   index: int, offset: int) -> pd.Series:
        df_true_question = df_true.str[i - offset]
        df_marked_question = df_marked.str[i - offset]

        result = pd.Series([0]*df_true.shape[0], dtype=object)

        result = df_true_question == df_marked_question
        
        arg1 = df_true_question == "Z"
        arg2 = df_true_question == "X"
        cancelled_index = arg1 | arg2
        result[cancelled_index] = "NaN"

        return result
    
    
    used_columns = ["DS_VT_GAB_OFG_FIN", "DS_VT_GAB_OCE_FIN",
                    "DS_VT_ESC_OFG", "DS_VT_ESC_OCE"]
    

    for column in used_columns:
        if column not in df.columns:
            raise ValueError(f"A coluna {column} não está no DataFrame")

    general_answer_key = df[used_columns[0]]
    specific_answer_key = df[used_columns[1]]
    
    general_marked = df[used_columns[2]]
    specific_marked = df[used_columns[3]]
    
    for i in range(1, 35 + 1): # loop pelas questoes objetivas
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
        if int(id_question[-1]) < 3:
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
    for i in range(1, 3+1): #  df_subject has 3 subjects
        column = f"conteudo{i}"
        column_subjects = df[column].dropna().unique()
        subjects = np.union1d(subjects, column_subjects)
    return subjects

def is_question_of_subject(subject: str, row: pd.Series) -> bool:
    """Returns True if a row/question is of subject and 
    False otherwise"""
    boolean_array = row[["conteudo1", "conteudo2", "conteudo3"]] == subject
    return boolean_array.any()


def get_subject_valid_questions(subject: str, df_subject: pd.DataFrame,
                                df_enade: pd.DataFrame) -> List[str]:
    """Returns a list with ids of the questions that have 
    the subject and that are valid"""
    result = []
    for index, row in df_subject.iterrows():
        arg1 = is_question_of_subject(subject, row)
        arg2 = not is_question_cancelled(row["idquestao"], df_enade)
        if arg1 and arg2:
            result.append(row["idquestao"])
    return result

def add_column_score_subject(subject: str, df_enade: pd.DataFrame, 
                             df_temas: pd.DataFrame) -> pd.DataFrame:
    questions = get_subject_valid_questions(subject, df_temas, df_enade)
    sum_score = np.array([0.0] * df_enade.shape[0])  # number of participants
    for question in questions:
        if 'D' in question: # discursive question
            numeric_id = int(question[-1])
            if numeric_id < 3:
                sum_score += df_enade[f"NT_FG_D{numeric_id}"]
            else:
                numeric_id -= 2
                sum_score += df_enade[f"NT_CE_D{numeric_id}"]
        else:
            sum_score += pd.to_numeric(df_enade[f"QUESTAO_OBJ_{question}_ACERTO"]) * 100
    sum_score /= len(questions)
    df_enade.loc[:, f"SCORE_{subject}"] = sum_score
    return df_enade


def add_column_objective_score_subject(subject: str, df_enade: pd.DataFrame, 
                                       df_temas: pd.DataFrame) -> pd.DataFrame:
    questions = get_subject_valid_questions(subject, df_temas, df_enade)
    # get only objective questions
    questions = [x for x in questions if "D" not in x]
    sum_score = np.array([0.0] * df_enade.shape[0])  # number of participants
    for question in questions:
        sum_score += pd.to_numeric(df_enade[f"QUESTAO_OBJ_{question}_ACERTO"]) * 100
    mean_score = sum_score / len(questions)
    df_enade.loc[:, f"SCORE_OBJ_{subject}"] = mean_score
    df_enade.loc[:, f"ACERTOS_OBJ_{subject}"] = sum_score / 100
    return df_enade


def add_all_score_subjects(df_enade: pd.DataFrame,
        df_temas: pd.DataFrame, objective: bool) -> pd.DataFrame:
    subjects = get_subjects(df_temas)
    for subject in subjects:
        if objective:
            df_enade = add_column_objective_score_subject(subject, df_enade,
                                                          df_temas)
        else:
            df_enade = add_column_score_subject(subject, df_enade, df_temas)
    return df_enade

