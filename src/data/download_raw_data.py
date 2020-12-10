import sys
import os
parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')) #this should give you absolute location of my_project folder.
sys.path.append(parent)
from urllib.request import urlretrieve
from src.config import years
from typing import Callable
from tqdm import tqdm
import click


class DownloadData:

    def __init__(self, raw_data_path: str,
                 download_function: Callable = urlretrieve) -> None:
        self.start_url = "http://download.inep.gov.br/microdados/Enade_Microdados/"

        end_url_2017 = "microdados_Enade_2017_portal_2018.10.09.zip"
        end_url_2014 = "microdados_enade_2014.zip"
        end_url_2011 = "microdados_enade_2011.zip"
        end_url_2008 = "microdados_enade_2008.zip"
        end_url_2005 = "microdados_enade_2005.zip"

        self.urls = [end_url_2017, end_url_2014, end_url_2011, end_url_2008,
                     end_url_2005]
        self.raw_data_path = raw_data_path
        self.file_start_path = "microdados_enade"
        self.download_function = download_function
        self.years = years

    def run(self) -> None:
        try:
            for url_year, year in zip(tqdm(self.urls), self.years):
                url = f"{self.start_url}{url_year}"
                file_name = f"{self.file_start_path}_{year}.zip"
                file_path = os.path.join(self.raw_data_path, file_name)
                print(url, file_path)
                self.download_function(url, file_path)
        except ConnectionResetError:
            # In case original source is not working, download from github backup
            self.start_url = "https://github.com/renan-cunha/EnadeData/raw/main/"
            self.urls[0] = "microdados_enade_2017.zip"
            self.run()
            

@click.command()
@click.option('--path', help='Path to save downloaded files;')
def main(path):
    download_data = DownloadData(path)
    print("Downloading Data...")
    download_data.run()
    print("Download complete")


if "__main__" == __name__:
    main()
