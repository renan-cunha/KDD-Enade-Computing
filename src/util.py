import pandas as pd
from typing import Union, List, Callable
import numpy as np
from src.config import NUM_ENADE_EXAM_QUESTIONS, MAX_SUBJECTS_PER_QUESTION, \
    STUDENT_CODE_ABSENT, STUDENT_CODE_PRESENT, BLANK_LABEL, DELETION_LABEL, \
    DIFFICULTIES
from src.process2014_2017 import ProcessEnade2014_2017
from src.process2011 import ProcessEnade2011
from src.process2008 import ProcessEnade2008
from src.process2005 import ProcessEnade2005


def map_presence(df: pd.DataFrame) -> None:
    new_mapping = df["TP_PRES"].map({STUDENT_CODE_ABSENT: "Ausente",
                                     STUDENT_CODE_PRESENT: "Presente"}).values
    df.loc[:, "TP_PRES"] = new_mapping


def filter_present_students(df: pd.DataFrame) -> pd.DataFrame:
    df = df.loc[df["TP_PRES"] == "Presente"]
    return df


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
    """Returns True if the question is cancelled and False otherwise."""
    if df_enade[f"QUESTAO_{id_question}_STATUS"].iloc[0] == "NULA":
        result = True
    else:
        result = False
    return result
    

def get_subjects(df: pd.DataFrame) -> np.ndarray:
    """Returns a ndarray with the unique set of subjects used in test"""
    subjects = np.zeros(0)
    for i in range(1, MAX_SUBJECTS_PER_QUESTION+1): #  df_subject has 3 subjects
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
                                df_enade: pd.DataFrame,
                                just_objective: bool, 
                                type_questions: str = "valid") -> List[str]:
    """Returns a list with ids of the questions that have 
    the subject"""
    result = []
    for index, row in df_subject.iterrows():
        arg1 = is_question_of_subject(subject, row)
        arg2 = not is_question_cancelled(row["idquestao"], df_enade)

        if type_questions == "invalid":
            arg2 = not arg2
        elif type_questions != "valid":
            raise ValueError(f"The type_question argumento should be 'valid'"
                             f" or invalid")

        if just_objective:
            arg3 = row["tipoquestao"] == "Objetiva"
        else:
            arg3 = True
        if arg1 and arg2 and arg3:
            result.append(row["idquestao"])
    return result

def get_validity_questions_df_year(df_subject: pd.DataFrame, 
                               df_enade_year: pd.DataFrame, 
                               just_objective: bool) -> pd.DataFrame:
    """Return a df with index as subjects, and columns of valid and invalid"""
    subjects = get_subjects(df_subject)
    result = pd.DataFrame(index=subjects, columns = ["valid", "invalid"])
    for subject in subjects:

        valid_questions = get_subject_valid_questions(subject, df_subject,
                                                      df_enade_year,
                                                      just_objective, 'valid')
        invalid_questions = get_subject_valid_questions(subject, df_subject,
                                                        df_enade_year,
                                                        just_objective, 
                                                        'invalid')
        result.loc[subject, :] = [len(valid_questions), len(invalid_questions)]
    return result

def get_validity_questions_df_all_years(df_subject: pd.DataFrame,
                                        dfs_enade: pd.DataFrame,
                                        just_objective: bool=True) -> pd.DataFrame:
    subjects = get_subjects(df_subject)
    years = dfs_enade.keys()
    result = pd.DataFrame(0, index=subjects, columns=["valid", "invalid"])
    for year in years:
        df_subject_year = df_subject.loc[df_subject["ano"] == year]
        df_enade_year = dfs_enade[year]
        
        validity_questions_year = get_validity_questions_df_year(df_subject_year,
                                                      df_enade_year,
                                                      just_objective)
        index_year = validity_questions_year.index
        result.loc[index_year] += validity_questions_year
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


def add_column_objective_score_category(category: str, df_enade: pd.DataFrame,
                                        questions: List[str]) -> pd.DataFrame:
    """Assumes valid questions"""
    sum_score = np.array([0.0] * df_enade.shape[0])  # number of participants
    for question in questions:
        question_score = df_enade[f"QUESTAO_{question}_NOTA"].copy()
        blank_question_score_index = question_score == BLANK_LABEL
        deletion_question_score_index = question_score == DELETION_LABEL
        zero_score_index = blank_question_score_index | deletion_question_score_index
        question_score[zero_score_index] = 0
        sum_score += pd.to_numeric(question_score)
    if len(questions) > 0:
        mean_score = sum_score / len(questions)
    else:
        # in case the subject doesn't have questions
        mean_score = np.full_like(a=sum_score, fill_value=np.nan)
    df_enade.loc[:, f"SCORE_OBJ_{category}"] = mean_score
    df_enade.loc[:, f"ACERTOS_OBJ_{category}"] = sum_score / 100
    return df_enade


def add_all_score_categories(df_enade: pd.DataFrame,
                             df_categories: pd.DataFrame,
                             objective: bool,
                             categories: List[str],
                             get_questions_function: Callable) -> pd.DataFrame:
    for category in categories:
        if objective:
            questions = get_questions_function(category, df_categories,
                                               df_enade, just_objective=True)
            df_enade = add_column_objective_score_category(category, df_enade,
                                                           questions)
        else:
            raise NotImplemented
    return df_enade


def add_all_score_subjects(df_enade: pd.DataFrame, df_temas: pd.DataFrame,
                           objective: bool) -> pd.DataFrame:
    subjects = get_subjects(df_temas)
    for subject in subjects:
        if objective:
            questions = get_subject_valid_questions(subject, df_temas, df_enade,
                                                    just_objective=True)
            df_enade = add_column_objective_score_category(subject, df_enade,
                                                           questions)
        else:
            df_enade = add_column_score_subject(subject, df_enade, df_temas)
    return df_enade


def add_all_score_difficulties(df_enade: pd.DataFrame,
                               df_difficulty: pd.DataFrame) -> pd.DataFrame:
    for difficulty in DIFFICULTIES:
        questions = get_difficulty_valid_questions(difficulty, df_difficulty,
                                                   df_enade)
        df_enade = add_column_objective_score_category(difficulty, df_enade,
                                                       questions)
    return df_enade


def get_difficulty_valid_questions(diffculty: str, df_difficulty: pd.DataFrame,
                                   df_enade: pd.DataFrame,
                                   just_objective: bool = True) -> List[str]:
    """Returns a list with ids of the questions that are of the difficulty and
    that are valid"""
    if not just_objective:
        raise ValueError("Only objective questions have difficulty")
    result = []
    for index, row in df_difficulty.iterrows():
        arg1 = row["dificuldade"] == diffculty
        arg2 = not is_question_cancelled(row["idquestao"], df_enade)
        if arg1 and arg2:
            result.append(row["idquestao"])
    return result


def get_dict_all_years(filter_by_ufpa: bool) -> dict:
    """Return a dict with keys as year, and values as enade_df"""
    enade_2017 = ProcessEnade2014_2017(2017).get_data(filter_by_ufpa)
    enade_2014 = ProcessEnade2014_2017(2014).get_data(filter_by_ufpa)
    enade_2011 = ProcessEnade2011().get_data(filter_by_ufpa)
    enade_2008 = ProcessEnade2008().get_data(filter_by_ufpa)
    enade_2005 = ProcessEnade2005().get_data(filter_by_ufpa)
    return {2017: enade_2017, 
            2014: enade_2014, 
            2011: enade_2011,
            2008: enade_2008,
            2005: enade_2005}
