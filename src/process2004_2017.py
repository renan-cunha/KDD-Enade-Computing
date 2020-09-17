import pandas as pd
from src.process_enade import filter_enade_df_by_course, get_recent_enade_dir, \
    ProcessEnade


class ProcessEnade2014_2017(ProcessEnade):

    GEN_DIS_QUESTIONS_ID = [1, 2]
    GEN_DIS_QUESTIONS_LABEL = GEN_DIS_QUESTIONS_ID

    SPE_DIS_QUESTIONS_ID = [11, 12, 13]
    SPE_DIS_QUESTIONS_LABEL = [1, 2, 3]

    GEN_OBJ_QUESTIONS_ID = list(range(3, 10 + 1))
    GEN_OBJ_QUESTIONS_LABEL = list(range(len(GEN_OBJ_QUESTIONS_ID)))

    SPE_OBJ_QUESTIONS_ID = list(range(14, 40 + 1))
    SPE_OBJ_QUESTIONS_LABEL = list(range(len(SPE_OBJ_QUESTIONS_ID)))

    def __init__(self, year: int) -> None:
        self.path_csv = get_recent_enade_dir(year)

    def read_csv(self) -> pd.DataFrame:
        return pd.read_csv(self.path_csv, sep=";", decimal=",",
                           dtype={"DS_VT_ESC_OFG": str,
                                  "DS_VT_ESC_OCE": str,
                                  "DS_VT_ACE_OCE": str,
                                   "DS_VT_ACE_OFG": str})

    def pre_process(self, df: pd.DataFrame) -> pd.DataFrame:
        return filter_enade_df_by_course(df)

    def set_year(self, year: int) -> None:
        if year != 2014 or year != 2017:
            raise ValueError(f"Year should be 2014 or 2017, not {year}")
        self.path_csv = get_recent_enade_dir(year)
