from unittest.mock import Mock
import pytest
from src.data.download_raw_data import DownloadData
import os




def test_download_data(tmpdir: str) -> None:
    
    def t_write_a_file(url: str, file_path: str) -> None:
        file = open(file_path, "w")
        file.close()

    mock = Mock(side_effect=t_write_a_file)
    
    download_data = DownloadData(tmpdir, mock)
    download_data.run()
    for year in [2017, 2014, 2011, 2008, 2005]:
        file_path = os.path.join(tmpdir, f"microdados_enade_{year}.zip")
        with open(file_path) as file:
            assert file.read() == ''

def test_download_data_with_exception(tmpdir: str) -> None:
    
    def t_write_a_file_failed(url: str, file_path: str) -> None:
        if url.startswith("http://download.inep.gov.br"):
            raise ConnectionResetError
        file = open(file_path, "w")
        file.close()

    mock = Mock(side_effect=t_write_a_file_failed)

    download_data = DownloadData(tmpdir, mock)
    download_data.run()
    mock.assert_any_call("https://github.com/renan-cunha/EnadeData/raw/main/microdados_enade_2005.zip", os.path.join(tmpdir, "microdados_enade_2005.zip"))
    for year in [2017, 2014, 2011, 2008, 2005]:
        file_path = os.path.join(tmpdir, f"microdados_enade_{year}.zip")
        with open(file_path) as file:
            assert file.read() == ''
    print(mock.mock_calls)

