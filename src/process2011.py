import pandas as pd
from src.process_enade import filter_enade_df_by_ufpa_course, ProcessEnade, \
    get_recent_enade_dir, filter_enade_df_by_course_new
import numpy as np


class ProcessEnade2011(ProcessEnade):

    GEN_DIS_QUESTIONS_ID = [9, 10]
    GEN_DIS_QUESTIONS_LABEL = [1, 2]

    SPE_DIS_QUESTIONS_ID = [11, 12, 13]
    SPE_DIS_QUESTIONS_LABEL = [1, 2, 3]

    GEN_OBJ_QUESTIONS_ID = list(range(1, 8 + 1))
    GEN_OBJ_QUESTIONS_LABEL = list(range(len(GEN_OBJ_QUESTIONS_ID)))

    SPE_OBJ_QUESTIONS_ID = list(range(14, 40 + 1))
    SPE_OBJ_QUESTIONS_LABEL = np.array(list(range(len(SPE_OBJ_QUESTIONS_ID))))
    SPE_OBJ_QUESTIONS_LABEL[-5:] += 5
    SPE_OBJ_QUESTIONS_LABEL = list(SPE_OBJ_QUESTIONS_LABEL)

    path_csv = get_recent_enade_dir(2011)

    def read_csv(self) -> pd.DataFrame:
        return pd.read_csv(self.path_csv, sep=";", decimal=",",
                 dtype={"DS_VT_ESC_OFG": str,
                        "DS_VT_ESC_OCE": str,
                        "DS_VT_ACE_OCE": str,
                        "DS_VT_ACE_OFG": str,
                        "NT_OBJ_CE": str})

    def pre_process(self, df: pd.DataFrame) -> pd.DataFrame:
        return df

    def filter_enade_df_by_course(self, df: pd.DataFrame) -> pd.DataFrame:
        return filter_enade_df_by_course_new(df)