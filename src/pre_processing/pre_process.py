import os
import subprocess

import pandas as pd

import sys
parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')) #this should give you absolute location of my_project folder.
sys.path.append(parent)
from src import config
from src.selection import select_data
from src.config import DATA_DIR
from tqdm import tqdm

PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed_data")


def read_csv(year: int, path: str = PROCESSED_DATA_DIR) -> pd.DataFrame:
    return pd.read_csv(get_processed_csv_file_path(year, path),
                       dtype=config.DTYPES)


def get_processed_csv_file_path(year: int,
                                path: str = PROCESSED_DATA_DIR) -> str:
    return os.path.join(path, f"microdados_processado_{year}.csv")


def remove_missing_data(df: pd.DataFrame) -> pd.DataFrame:
    """Filters the students that were present but have missing values"""
    missing_values = df["DS_VT_ESC_OCE"].isna()
    present = df["TP_PRES"] == config.STUDENT_CODE_PRESENT
    boolean_index = ~(missing_values & present)
    return df.loc[boolean_index]


def rename_columns_2008_2005(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns of enade dataframes of years 2005 in 2008
    The new name is the same as the datasets from more recent years"""
    df.columns = [x.upper() for x in df.columns]
    columns_to_rename = ["VT_ESC_OFG", "VT_ESC_OCE", "VT_ACE_OCE", "VT_ACE_OFG"]
    new_columns = [f"DS_{x}" for x in columns_to_rename]

    df.rename(columns=dict(zip(columns_to_rename, new_columns)), inplace=True)
    return df


def main(select_path: str = select_data.SELECTED_DATA_DIR,
         processed_path: str = PROCESSED_DATA_DIR):

    subprocess.run(["mkdir", "-p", processed_path])
    for year in tqdm(config.YEARS):
        df_year = select_data.read_csv(year, select_path)
        if year in [2008, 2005]:
            df_year = rename_columns_2008_2005(df_year)
        df_year_cleaned = remove_missing_data(df_year)
        file_path = get_processed_csv_file_path(year, processed_path)
        df_year_cleaned.to_csv(file_path, index=False)


if __name__ == "__main__":
    main()
