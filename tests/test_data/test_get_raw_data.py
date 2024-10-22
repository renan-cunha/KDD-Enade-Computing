from unittest.mock import Mock
import pytest
from src.get_data.get_raw_data import GetData, main
import os
import zipfile
import pandas as pd
import subprocess
from typing import Callable

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

        def t_write_a_file(url: str, file_path: str) -> None:
            with zipfile.ZipFile(file_path, "w") as zip_file:
                file_name = os.path.basename(file_path)
                new_file_name = file_name[:file_name.index(".zip")] + ".csv"
                new_file_path = os.path.join(DATA_DIR_NAME, new_file_name)
                zip_file.writestr(f"2.DADOS/", '')
                zip_file.writestr(new_file_path, "z")

        mock = Mock(side_effect=t_write_a_file)
        main(tmpdir,tmpdir,  True, True, mock)
        assert_created_zip_files(tmpdir, "csv", 'z')


class TestReadCsv:

    def get_df_2017(self) -> pd.DataFrame:
        return pd.DataFrame({"DS_VT_ESC_OFG": ["efe", "1"],
                                  "DS_VT_ESC_OCE": ["r3r", "1"],
                                  "DS_VT_ACE_OCE": ["r3", "1"],
                                  "DS_VT_ACE_OFG": ["efe", "1"],
                                  "NT_OBJ_CE": ["ege", "1"],
                                  "CO_IES": ["1", "3frg"]})

    def get_df_2008(self) -> pd.DataFrame:
        return pd.DataFrame({"vt_esc_ofg": ["ef", '1'],
                                "vt_esc_oce": ['1', '133'],
                                "vt_ace_oce": ['erg', '2'],
                                "vt_ace_ofg": ['r3r3', '2'],
                                "nt_obj_ce": ['13', '13'],
                                "co_grupo": [1, 2]})

    def get_df_2005(self) -> pd.DataFrame:
        return pd.DataFrame({"vt_esc_ofg": ['13', '1'],
                                  "vt_esc_oce": ['12', '1243'],
                                  "vt_ace_oce": ['124', '134'],
                                  "vt_ace_ofg": ['1243', 'ete'],
                                  "nt_obj_ce": ['143', '15425']})

    def set_up(self, tmpdir: str, year: int, function: Callable) -> pd.DataFrame:
        csv_file_name = f"microdados_enade_{year}.csv"
        dir_name = os.path.join(tmpdir, f"enade_{year}")
        subprocess.run(["mkdir", dir_name])
        csv_file_path = os.path.join(dir_name, csv_file_name)
        input_df = function()
        input_df.to_csv(csv_file_path, sep=";", index=False)
        return input_df

    def test_read_csv_2017(self, tmpdir) -> None:
        year = 2017
        input_df = self.set_up(tmpdir, year, self.get_df_2017)

        data = GetData(tmpdir)
        output_df = data.read_csv(year)

        assert output_df.equals(input_df)

    def test_read_csv_2008(self, tmpdir) -> None:
        year = 2008
        input_df = self.set_up(tmpdir, year, self.get_df_2008)

        data = GetData(tmpdir)
        output_df = data.read_csv(year)

        assert output_df.equals(input_df)

    def test_read_csv_2005(self, tmpdir) -> None:
        year = 2005
        input_df = self.set_up(tmpdir, year, self.get_df_2005)

        data = GetData(tmpdir)
        output_df = data.read_csv(year)

        assert output_df.equals(input_df)


ENADE_DATA_PATH = os.path.join('data', 'raw_data', 'enade_data')


class TestMakeDownloadData:
    @pytest.mark.parametrize("input,expected", [(2005, 27682769),
                                                (2008, 37755081),
                                                (2011, 24917485),
                                                (2014, 40651249),
                                                (2017, 45740121)])
    @pytest.mark.make()
    def test_make_download_data(self, input, expected) -> None:
        path_year = os.path.join(ENADE_DATA_PATH, f'enade_{input}',
                                 f"microdados_enade_{input}.zip")
        assert os.path.getsize(path_year) == expected


class TestMakeExtractData:
    @pytest.mark.parametrize("input,expected", [(2005, (323338, 210)),
                                                (2008, (461776, 198)),
                                                (2011, (376180, 115)),
                                                (2014, (481720, 154)),
                                                (2017, (537436, 150))])
    @pytest.mark.make()
    def test_make_extract_data(self, input, expected) -> None:
        get_data = GetData()
        assert get_data.read_csv(input).shape == expected
