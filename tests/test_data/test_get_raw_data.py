from unittest.mock import Mock
import pytest
from src.data.get_raw_data import GetData, main
import os
import zipfile
from typing import Tuple

years = [2017, 2014, 2011, 2008, 2005]


@pytest.fixture()
def setUp(tmpdir):
    download_data = GetData(tmpdir, tmpdir)
    download_data.write_directories()
    yield download_data


def assert_created_zip_files(tmpdir: str, extension: str,
                             content: str = "") -> None:
    for year in years:
        file_path = os.path.join(tmpdir, f"enade_{year}",
                                 f"microdados_enade_{year}.{extension}")
        with open(file_path) as file:
            assert file.read() == content


class TestDownloadData:

    def test_download_data(self, tmpdir: str, setUp: GetData) -> None:

        def t_write_a_file(data: Tuple[str, str]) -> None:
            url, file_path = data
            file = open(file_path, "w")
            file.close()

        download_data = setUp
        mock = Mock(side_effect=t_write_a_file)
        download_data.download_data(mock)
        assert_created_zip_files(tmpdir, "zip")

    def test_download_data_with_exception(self, tmpdir: str, setUp: GetData) -> None:

        # setup
        def t_write_a_file_failed(data: Tuple[str, str]) -> str:
            url, file_path = data
            if url.startswith("http://download.inep.gov.br"):
                raise ConnectionResetError
            file = open(file_path, "w")
            file.close()
            return url

        get_data = setUp
        mock = Mock(side_effect=t_write_a_file_failed)
        # test
        get_data.download_data(mock)
        data = ("https://github.com/renan-cunha/EnadeData/raw/main/microdados_enade_2005.zip",
                os.path.join(tmpdir, "enade_2005", "microdados_enade_2005.zip"))
        print(mock.mock_calls)
        mock.assert_any_call(data)
        assert_created_zip_files(tmpdir, "zip")


DATA_DIR_NAME = "2.DADOS"


class TestExtractData:

    def create_zip_files(self, path) -> None:
        start_file_name = "microdados_enade"
        file_names = [f'{start_file_name}_{year}' for year in years]
        dir_names = [f"enade_{year}" for year in years]
        file_paths = [os.path.join(path,
                                   dir_name,
                                   f"{file_name}.zip") for file_name,
                                                  dir_name in zip(file_names,
                                                                  dir_names)]
        for file_path, year in zip(file_paths, years):
            with zipfile.ZipFile(file_path, 'w') as myzip:

                myzip.writestr(f"1.LEIA-me/manual.txt", '')
                myzip.writestr(f"2.DADOS/", '')
                myzip.writestr(f"2.DADOS/microdados_enade_{year}.txt", 'z')
                myzip.writestr(f"INPUTS/scrip.sh", "")

    def test_extract_data(self, tmpdir: str, setUp) -> None:
        """Should create text files from zip files"""
        # setup
        get_data = setUp
        self.create_zip_files(tmpdir)

        #test
        get_data.extract_data()
        assert_created_zip_files(tmpdir, "csv", 'z')

    def test_manuals(self, tmpdir: str, setUp) -> None:
        """Should create manual files from zip files"""
        # setup
        get_data = setUp

        for year in years:
            file_path = os.path.join(tmpdir, f'enade_{year}',
                                     f"microdados_enade_{year}.zip")
            with zipfile.ZipFile(file_path, 'w') as myzip:
                if year % 2 == 0:
                    myzip.writestr(f"1.LEIA-ME/manual.txt", 'leia')
                else:
                    myzip.writestr(f"1.DOCUMENTAÇ╟O/manual.txt", 'manual')
                myzip.writestr(f"2.DADOS/dados.csv", "")
        # run
        get_data.extract_data()

        # assert

        with open(os.path.join(tmpdir, "enade_2017", "1.DOCUMENTAÇ╟O/manual.txt")) as file:
            assert file.read() == "manual"
        with open(os.path.join(tmpdir, "enade_2014", "1.LEIA-ME/manual.txt")) as file:
            assert file.read() == "leia"
        with open(os.path.join(tmpdir, "enade_2011", "1.DOCUMENTAÇ╟O/manual.txt")) as file:
            assert file.read() == "manual"
        with open(os.path.join(tmpdir, "enade_2008", "1.LEIA-ME/manual.txt")) as file:
            assert file.read() == "leia"
        with open(os.path.join(tmpdir, "enade_2005", "1.DOCUMENTAÇ╟O/manual.txt")) as file:
            assert file.read() == "manual"


class TestMainData:

    def test_main_data(self, tmpdir):

        def t_write_a_file(data: Tuple[str, str]) -> None:
            url, file_path = data
            with zipfile.ZipFile(file_path, "w") as zip_file:
                file_name = os.path.basename(file_path)
                new_file_name = file_name[:file_name.index(".zip")] + ".csv"
                new_file_path = os.path.join(DATA_DIR_NAME, new_file_name)
                zip_file.writestr(f"2.DADOS/", '')
                zip_file.writestr(new_file_path, "z")

        mock = Mock(side_effect=t_write_a_file)
        main(tmpdir,tmpdir,  True, True, mock)
        assert_created_zip_files(tmpdir, "csv", 'z')