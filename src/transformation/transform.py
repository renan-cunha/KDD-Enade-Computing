import os
import sys
import subprocess

import pandas as pd
from tqdm import tqdm

parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(parent)
from src.pre_processing import pre_process
from src import config
from src.transformation.transform_2005 import Transform2005
from src.transformation.transform_2008 import Transform2008
from src.transformation.transform_2011 import Transform2011
from src.transformation.transform_2014_2017 import Transform2014_2017


TRANSFORMED_DATA_DIR = os.path.join(config.DATA_DIR, 'transformed_data')


def read_csv(year: int, path: str = TRANSFORMED_DATA_DIR) -> pd.DataFrame:
    return pd.read_csv(get_transformed_enade_csv_file_path(year, path),
                       dtype=config.DTYPES)


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
    subprocess.run(["mkdir", "-p", transformed_data_path])
    for year in tqdm(config.YEARS):
        pre_processed_year_df = pre_process.read_csv(year,
                                                     path=pre_processed_data_path)
        transformed_df_year = transform_enade_year(pre_processed_year_df, year)
        transformed_csv_file_path = get_transformed_enade_csv_file_path(year,
                                                                        path=transformed_data_path)
        transformed_df_year.to_csv(transformed_csv_file_path, index=False)


if __name__ == "__main__":
    main()
