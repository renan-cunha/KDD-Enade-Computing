import pandas as pd
from src.process_enade import filter_enade_df_by_course, filter_senior_students, \
    ProcessEnade, get_old_enade_dir, pre_process_old


class ProcessEnade2008(ProcessEnade):

    GEN_DIS_QUESTIONS_ID = [9, 10]
    GEN_DIS_QUESTIONS_LABEL = [1, 2]

    SPE_DIS_QUESTIONS_ID = [20, 39, 40]
    SPE_DIS_QUESTIONS_LABEL = [1, 2, 3]

    GEN_OBJ_QUESTIONS_ID = list(range(1, 8 + 1))
    GEN_OBJ_QUESTIONS_LABEL = list(range(len(GEN_OBJ_QUESTIONS_ID)))

    SPE_OBJ_QUESTIONS_ID = list(range(11, 20)) + list(range(21, 38 + 1))
    SPE_OBJ_QUESTIONS_LABEL = list(range(len(SPE_OBJ_QUESTIONS_ID)))

    path_csv = get_old_enade_dir(2008)

    def read_csv(self) -> pd.DataFrame:
        return pd.read_csv(self.path_csv, sep=";", decimal=",",
                         dtype={"vt_esc_ofg": str,
                                "vt_esc_oce": str,
                                "vt_ace_oce": str,
                                "vt_ace_ofg": str,
                                "nt_obj_ce": str})

    def pre_process(self, df: pd.DataFrame) -> pd.DataFrame:
        df = pre_process_old(df)
        df = filter_enade_df_by_course(df)
        return filter_senior_students(df)


