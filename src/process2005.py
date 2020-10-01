import pandas as pd
from src.process_enade import filter_enade_df_by_course_old, \
    filter_senior_students, ProcessEnade, get_old_enade_dir, pre_process_old


class ProcessEnade2005(ProcessEnade):

    GEN_DIS_QUESTIONS_ID = [8, 9, 10]
    GEN_DIS_QUESTIONS_LABEL = [1, 2, 3]

    SPE_DIS_QUESTIONS_ID = [25, 40]
    SPE_DIS_QUESTIONS_LABEL = [3, 4]

    GEN_OBJ_QUESTIONS_ID = list(range(1, 7 + 1))
    GEN_OBJ_QUESTIONS_LABEL = list(range(len(GEN_OBJ_QUESTIONS_ID)))

    SPE_OBJ_QUESTIONS_ID = list(range(11, 24 + 1)) + list(range(26, 39 + 1))
    SPE_OBJ_QUESTIONS_LABEL = list(range(28, len(SPE_OBJ_QUESTIONS_ID) + 28))


    path_csv = get_old_enade_dir(2005)

    def read_csv(self) -> pd.DataFrame:
        return pd.read_csv(self.path_csv, sep=";", decimal=",",
                           dtype={"vt_esc_ofg": str,
                                  "vt_esc_oce": str,
                                  "vt_ace_oce": str,
                                  "vt_ace_ofg": str,
                                  "nt_obj_ce": str},
                           encoding="latin")

    def pre_process(self, df: pd.DataFrame) -> pd.DataFrame:
        df = pre_process_old(df)
        return filter_senior_students(df)

    def filter_enade_df_by_course(self, df: pd.DataFrame) -> pd.DataFrame:
        return filter_enade_df_by_course_old(df)
