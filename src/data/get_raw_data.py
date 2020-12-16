import sys
import os
parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')) #this should give you absolute location of my_project folder.
sys.path.append(parent)
from urllib.request import urlretrieve
from src.config import years
from typing import Callable
from tqdm import tqdm
import click
import zipfile
import errno


DATA_DIR_NAMES = ["2.DADOS", "3.DADOS"]
README_DIR_NAMES = ['1.DOCUMENTAÇ╟O', "1.LEIA-ME"]
DATA_DIR = os.path.join("data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw_data")
RAW_ENADE_DATA_DIR = os.path.join(RAW_DATA_DIR, "enade_data")
MANUALS_DIR = os.path.join("references")


def get_raw_enade_csv_file_path(year: int,
                                raw_enade_data_dir: str = RAW_ENADE_DATA_DIR) -> str:
    return os.path.join(raw_enade_data_dir, f"enade_{year}",
                        f"microdados_enade_{year}.csv")


class GetData:

    def __init__(self, raw_data_path: str = RAW_ENADE_DATA_DIR,
                 manuals_path: str = MANUALS_DIR) -> None:
        self.start_url = "http://download.inep.gov.br/microdados/Enade_Microdados/"

        end_url_2017 = "microdados_Enade_2017_portal_2018.10.09.zip"
        end_url_2014 = "microdados_enade_2014.zip"
        end_url_2011 = "microdados_enade_2011.zip"
        end_url_2008 = "microdados_enade_2008.zip"
        end_url_2005 = "microdados_enade_2005.zip"

        self.urls = [end_url_2017, end_url_2014, end_url_2011, end_url_2008,
                     end_url_2005]
        self.raw_data_path = raw_data_path
        self.manuals_path = manuals_path
        self.file_start_path = "microdados_enade"
        self.years = years

    def __get_zip_file_name(self, year: int) -> str:
        return f"{self.file_start_path}_{year}.zip"

    def __get_zip_file_path(self, year: int) -> str:
        file_name = self.__get_zip_file_name(year)
        return os.path.join(self.raw_data_path,
                            f'enade_{year}',
                            file_name)

    def write_directories(self) -> None:
        for year in self.years:
            file_path = self.__get_zip_file_path(year)
            dirname = os.path.dirname(file_path)
            if not os.path.exists(dirname):
                try:
                    os.makedirs(dirname)
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise OSError

    def download_data(self, download_function: Callable = urlretrieve) -> None:
        try:
            for url_year, year in zip(tqdm(self.urls), self.years):
                url = f"{self.start_url}{url_year}"
                file_path = self.__get_zip_file_path(year)
                download_function(url, file_path)
        except ConnectionResetError:
            # In case original source is not working, download from github backup
            self.start_url = "https://github.com/renan-cunha/EnadeData/raw/main/"
            self.urls[0] = "microdados_enade_2017.zip"
            self.download_data(download_function)

    def __extract_and_rename(self, zip: zipfile.ZipFile, file_path: str,
                             new_path: str) -> None:
        with open(new_path, "wb") as new_file:
            with zip.open(file_path) as zip_file:
                content = zip_file.read()
                new_file.write(content)

    def __get_data_file_name(self, year: int) -> str:
        return f"{self.file_start_path}_{year}.csv"

    def __get_zip_file_member(self, zip_file: zipfile.ZipFile) -> str:
        """Returns the path of the data file inside the zip file"""
        file_names = zip_file.namelist()
        for file_name in file_names:
            for data_dir_name in DATA_DIR_NAMES:
                ends_with_txt = file_name.endswith(".txt")
                ends_with_csv = file_name.endswith(".csv")
                starts_with_dir_name = file_name.startswith(data_dir_name)
                if starts_with_dir_name and (ends_with_csv or ends_with_txt):
                    return file_name

        raise ValueError(f"No member was found in the zipfile that starts with"
                         f" {DATA_DIR_NAMES}")

    def extract_data(self) -> None:
        for year in tqdm(self.years):
            zip_file_path = self.__get_zip_file_path(year)
            with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
                self.__extract_csv(year, zip_file)
                self.__extract_manual(year, zip_file)

    def __extract_csv(self, year: int, zip_file: zipfile.ZipFile) -> None:
            member_name = self.__get_zip_file_member(zip_file)
            file_path = get_raw_enade_csv_file_path(year, self.raw_data_path)
            self.__extract_and_rename(zip_file,
                                      member_name,
                                      file_path)

    def __extract_manual(self, year: int,
                        zip_file: zipfile.ZipFile) -> None:
        dir = os.path.join(self.manuals_path, f"enade_{year}")
        for file in zip_file.namelist():
            for readme_dir_name in README_DIR_NAMES:
                if file.startswith(readme_dir_name):
                    zip_file.extract(file, dir)


def main(data_path: str, manuals_path: str, download: bool, extract: bool,
         download_function: Callable = urlretrieve) -> None:
    get_data = GetData(data_path, manuals_path)
    get_data.write_directories()
    if download:
        print("Downloading Data...")
        get_data.download_data(download_function=download_function)
        print("Download Complete")
    if extract:
        print("Extracting data")
        get_data.extract_data()
        print("Extraction completed")


@click.command()
@click.option('--data_path', help='Path to save downloaded files;')
@click.option('--manuals_path', default="", help='Path to save downloaded files;')
@click.option('--download/--no-download', default=False,
              help='Download data;')
@click.option('--extract/--no-extract', default=False,
              help='Extract data;')
def click_main(data_path, manuals_path, download, extract):
    main(data_path, manuals_path, download, extract)


if "__main__" == __name__:
    click_main()
