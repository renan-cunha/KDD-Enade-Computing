import os
import sys
parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')) #this should give you absolute location of my_project folder.
sys.path.append(parent)

import pandas as pd

from src.pre_processing import pre_process
from src import config

from src.transformation.transform_2005 import Transform2005
from src.transformation.transform_2008 import Transform2008
from src.transformation.transform_2011 import Transform2011
from src.transformation.transform_2014_2017 import Transform2014_2017


TRANSFORMED_DATA_DIR = os.path.join(config.DATA_DIR, 'transformed_data')


def get_transformed_enade_csv_file_path(year: int,
                                        path: str = TRANSFORMED_DATA_DIR) -> str:
    return os.path.join(path, f"microdados_transformados_{year}.csv")


transform2014_2017 = Transform2014_2017()
transform2011 = Transform2011()
transform2008 = Transform2008()
transform2005 = Transform2005()


def transform_enade_year(pre_processed_year_df: pd.DataFrame,
                         year: int) -> pd.DataFrame:
    if year in [2017, 2014]:
        transformed_df = transform2014_2017.transform(pre_processed_year_df)
    elif year == 2011:
        transformed_df = transform2011.transform(pre_processed_year_df)
    elif year == 2008:
        transformed_df = transform2008.transform(pre_processed_year_df)
    elif year == 2005:
        transformed_df = transform2005.transform(pre_processed_year_df)
    else:
        raise ValueError()
    return transformed_df


def main(pre_processed_data_path: str = pre_process.PROCESSED_DATA_DIR,
         transformed_data_path: str = TRANSFORMED_DATA_DIR) -> None:
    for year in config.YEARS:
        pre_processed_csv_file_path = pre_process.get_processed_csv_file_path(year,
                                                                              pre_processed_data_path)
        pre_processed_year_df = pd.read_csv(pre_processed_csv_file_path)
        transformed_df_year = transform_enade_year(pre_processed_year_df, year)
        transformed_csv_file_path = get_transformed_enade_csv_file_path(year,
                                                                        path=transformed_data_path)
        transformed_df_year.to_csv(transformed_csv_file_path, index=False)
