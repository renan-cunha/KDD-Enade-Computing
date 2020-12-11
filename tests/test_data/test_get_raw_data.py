from unittest.mock import Mock
import pytest
from src.data.get_raw_data import GetData, main
import os
from zipfile import ZipFile

years = [2017, 2014, 2011, 2008, 2005]


@pytest.fixture()
def setUp(tmpdir):
    download_data = GetData(tmpdir)
    download_data.write_directories()
    yield download_data


def assert_created_zip_files(tmpdir: str, extension: str) -> None:
    for year in years:
        file_path = os.path.join(tmpdir, f"enade_{year}",
                                 f"microdados_enade_{year}.{extension}")
        with open(file_path) as file:
            assert file.read() == ''


class TestDownloadData:

    def test_download_data(self, tmpdir: str, setUp: GetData) -> None:

        def t_write_a_file(url: str, file_path: str) -> None:
            file = open(file_path, "w")
            file.close()

        download_data = setUp
        mock = Mock(side_effect=t_write_a_file)
        download_data.download_data(mock)
        assert_created_zip_files(tmpdir, "zip")

    def test_download_data_with_exception(self, tmpdir: str, setUp: GetData) -> None:

        # setup
        def t_write_a_file_failed(url: str, file_path: str) -> None:

            if url.startswith("http://download.inep.gov.br"):
                raise ConnectionResetError
            file = open(file_path, "w")
            file.close()

        get_data = setUp
        mock = Mock(side_effect=t_write_a_file_failed)
        # test
        get_data.download_data(mock)
        mock.assert_any_call("https://github.com/renan-cunha/EnadeData/raw/main/microdados_enade_2005.zip", os.path.join(tmpdir, f"enade_2005", "microdados_enade_2005.zip"))
        assert_created_zip_files(tmpdir, "zip")


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
        for file_path, file_name in zip(file_paths, file_names):
            with ZipFile(file_path, 'w') as myzip:
                myzip.writestr(f'{file_name}.txt', '')

    def test_extract_data(self, tmpdir: str, setUp) -> None:
        """Should create text files from zip files"""
        # setup
        get_data = setUp
        self.create_zip_files(tmpdir)

        #test
        get_data.extract_data()
        assert_created_zip_files(tmpdir, "txt")


class TestMainData:

    def test_main_data(self, tmpdir):

        def t_write_a_file(url: str, file_path: str) -> None:
            with ZipFile(file_path, "w") as zip_file:
                file_name = os.path.basename(file_path)
                new_file_name = file_name[:file_name.index(".zip")] + ".txt"
                zip_file.writestr(new_file_name, "")

        mock = Mock(side_effect=t_write_a_file)
        main(tmpdir, mock)
        assert_created_zip_files(tmpdir, "txt")