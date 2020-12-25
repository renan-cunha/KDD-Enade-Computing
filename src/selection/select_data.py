import pandas as pd
from typing import Tuple
import os
import sys

import src.config

parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')) #this should give you absolute location of my_project folder.
sys.path.append(parent)
from src.get_data import get_raw_data
from src import config
from tqdm import tqdm
import subprocess


SELECTED_DATA_DIR = os.path.join(src.config.DATA_DIR, "selected_data")
COMPUTER_SCIENCE_CODE_2017_2014_2011 = 4004
COMPUTER_SCIENCE_CODE_2008 = 4001
COMPUTER_CODE_2005 = 40


def read_csv(year: int, path: str = SELECTED_DATA_DIR) -> pd.DataFrame:
    return pd.read_csv(get_selected_enade_csv_file_path(year, path))


def get_selected_enade_csv_file_path(year: int,
                                     path: str = SELECTED_DATA_DIR) -> str:
    return os.path.join(path, f"microdados_ciencia_computacao_{year}.csv")


def filter_computer_science(df: pd.DataFrame, year: int) -> pd.DataFrame:
    if year in [2017, 2014, 2011]:
        return filter_computer_science_2017_2014_2011(df)
    elif year == 2008:
        return filter_computer_science_2008(df)
    elif year == 2005:
        return filter_computer_science_2005(df)
    else:
        raise ValueError(f"Use a year of {config.YEARS}, not {year}")


def filter_computer_science_2017_2014_2011(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[df["CO_GRUPO"] == COMPUTER_SCIENCE_CODE_2017_2014_2011]


def filter_computer_science_2008(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[df["co_subarea"] == COMPUTER_SCIENCE_CODE_2008]


def has_same_value(series: pd.Series) -> bool:
    """Returns true if the series has the same value in each row,
    returns false otherwise."""
    series_unique = series.unique()
    length_series = len(series_unique)
    if length_series > 1:
        return False
    elif length_series == 0:
        raise ValueError("The series is empty")
    else:
        return True


def get_computer_science_answer_key_2005(ufpa_cc_score_specific: pd.Series) -> Tuple[str, str]:
    """Returns the regex used to match the 'vt_ace_oce' with computer science
    courses. It gets that by using the 'vt_ace_oce' of the known UFPA computer
    science course"""

    length_scores = ufpa_cc_score_specific.str.len()
    if not has_same_value(length_scores):
        raise ValueError("The series should have values with the same length")

    def get_num_starting_dots(series: pd.Series, mode: str) -> int:
        length_value = len(series.iloc[0])
        num_dots_result = 0
        for num_dots in range(1, length_value):
            dot_string = "." * num_dots
            if mode == "start":
                equal_to_dot = series.str.startswith(dot_string)
            elif mode == "end":
                equal_to_dot = series.str.endswith(dot_string)
            else:
                raise ValueError(f"Use 'start' or 'end' as mode not {mode}")
            if equal_to_dot.all():
                num_dots_result = num_dots
            else:
                break
        return num_dots_result

    num_starting_dots = get_num_starting_dots(ufpa_cc_score_specific, 'start')
    num_ending_dots = get_num_starting_dots(ufpa_cc_score_specific, 'end')
    return '.' * num_starting_dots, '.' * num_ending_dots


def select_ufpa_computer_science_2005(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[df["co_curso"] == config.CODE_UFPA_COURSE]


def filter_specific_score_2005(df: pd.DataFrame) -> pd.DataFrame:
    return df["vt_ace_oce"]


def filter_computer_science_2005(df: pd.DataFrame) -> pd.DataFrame:

    """
    def is_computer_science(score_questions: str) -> bool:
        start = "." * 28
        end = "." * 14
        if type(score_questions) == float:
            return False
        if score_questions.startswith(start) and score_questions.endswith(end):
            # if it has at least one answer different than blank
            return True
        else:
            return False"""

    ufpa_comp_sci = select_ufpa_computer_science_2005(df)
    ufpa_comp_sci_specific_score = filter_specific_score_2005(ufpa_comp_sci)
    computer_science_dot_match = get_computer_science_answer_key_2005(ufpa_comp_sci_specific_score)

    starting_dots, ending_dots = computer_science_dot_match

    computer_df = df.loc[df["co_grupo"] == COMPUTER_CODE_2005]
    starting_dot_index = computer_df["vt_ace_oce"].str.startswith(starting_dots)
    ending_dot_index = computer_df["vt_ace_oce"].str.endswith(ending_dots)
    return computer_df.loc[starting_dot_index & ending_dot_index]


def main(raw_data_path: str = get_raw_data.RAW_ENADE_DATA_DIR,
         selected_data_path: str = SELECTED_DATA_DIR):
    subprocess.run(["mkdir", "-p", selected_data_path])
    get_data = get_raw_data.GetData(raw_data_path=raw_data_path)

    for year in tqdm(config.YEARS):
        df_year = get_data.read_csv(year)
        df_computer_science_year = filter_computer_science(df_year, year)
        file_path = get_selected_enade_csv_file_path(year, selected_data_path)
        df_computer_science_year.to_csv(file_path, index=False)


if __name__ == "__main__":
    print("Selecting Computer Science data")
    main()
    print("Selection completed")
