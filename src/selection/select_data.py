import pandas as pd

COMPUTER_SCIENCE_CODE_2017_2014_2011 = 4004
COMPUTER_SCIENCE_CODE_2008 = 4001
COMPUTER_SCIENCE_CODE_2005 = 40


def filter_computer_science_2017_2014_2011(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[df["CO_GRUPO"] == COMPUTER_SCIENCE_CODE_2017_2014_2011]


def filter_computer_science_2008(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[df["co_subarea"] == COMPUTER_SCIENCE_CODE_2008]

"""

def filter_computer_science_2005(df: pd.DataFrame) -> pd.Dataframe:

    def is_computer_science(score_questions: str) -> bool:
        "#Returns true if the right answers are the same as the one from
        computer science"
        start = "." * 28
        end = "." * 14
        if type(score_questions) == float:
            return False
        if score_questions.startswith(start) and score_questions.endswith(end):
            # if it has at least one answer different than blank
            return True
        else:
            return False

    df = df.loc[df["co_grupo"] == COMPUTER_SCIENCE_CODE_2005]
    boolean_index = df["vt_ace_oce"].apply(is_computer_science)
    return df.loc[boolean_index]

"""