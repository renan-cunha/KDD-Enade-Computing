import pytest
import os
from src.transformation import transform
from pytest_mock import MockerFixture
import pandas as pd
import subprocess

def test_get_transformed_enade_csv_file_path():
    path = "tmp"
    year = 2017
    expected = os.path.join(path, "microdados_transformados_2017.csv")
    output = transform.get_transformed_enade_csv_file_path(year, path)
    assert output == expected


class TestTransformEnadeYear:

    def test_transform_2017(self, mocker: MockerFixture):
        # arrange
        year = 2017

        def side_effect(df: pd.DataFrame) -> pd.DataFrame:
            return df.append({"year": f"{year}"}, ignore_index=True)

        mocker.patch("src.transformation.transform_2014_2017.Transform2014_2017.transform",
                     side_effect=side_effect)
        input_df = pd.DataFrame(columns=["year"])
        expected_df = pd.DataFrame({"year": [f"{year}"]})

        output = transform.transform_enade_year(input_df, year)

        assert output.equals(expected_df)


    def test_transform_2014(self, mocker: MockerFixture):
        # arrange
        year = 2014

        def side_effect(df: pd.DataFrame) -> pd.DataFrame:
            return df.append({"year": f"{year}"}, ignore_index=True)

        mocker.patch("src.transformation.transform_2014_2017.Transform2014_2017.transform",
                     side_effect=side_effect)
        input_df = pd.DataFrame(columns=["year"])
        expected_df = pd.DataFrame({"year": [f"{year}"]})

        output = transform.transform_enade_year(input_df, year)

        assert output.equals(expected_df)

    def test_transform_2011(self, mocker: MockerFixture):
        # arrange
        year = 2011

        def side_effect(df: pd.DataFrame) -> pd.DataFrame:
            return df.append({"year": f"{year}"}, ignore_index=True)

        mocker.patch("src.transformation.transform_2011.Transform2011.transform",
                     side_effect=side_effect)
        input_df = pd.DataFrame(columns=["year"])
        expected_df = pd.DataFrame({"year": [f"{year}"]})

        output = transform.transform_enade_year(input_df, year)

        assert output.equals(expected_df)

    def test_transform_2008(self, mocker: MockerFixture):
        # arrange
        year = 2008

        def side_effect(df: pd.DataFrame) -> pd.DataFrame:
            return df.append({"year": f"{year}"}, ignore_index=True)

        mocker.patch("src.transformation.transform_2008.Transform2008.transform",
                     side_effect=side_effect)
        input_df = pd.DataFrame(columns=["year"])
        expected_df = pd.DataFrame({"year": [f"{year}"]})

        output = transform.transform_enade_year(input_df, year)

        assert output.equals(expected_df)

    def test_transform_2005(self, mocker: MockerFixture):
        # arrange
        year = 2005

        def side_effect(df: pd.DataFrame) -> pd.DataFrame:
            return df.append({"year": f"{year}"}, ignore_index=True)

        mocker.patch("src.transformation.transform_2005.Transform2005.transform",
                     side_effect=side_effect)
        input_df = pd.DataFrame(columns=["year"])
        expected_df = pd.DataFrame({"year": [f"{year}"]})

        output = transform.transform_enade_year(input_df, year)

        assert output.equals(expected_df)

    def test_transform_value_error(self):
        # arrange
        year = 2004

        input_df = pd.DataFrame(columns=["year"])

        with pytest.raises(ValueError):
            transform.transform_enade_year(input_df, year)


def test_main(tmpdir, mocker: MockerFixture):
    # arrange
    processed_path = os.path.join(tmpdir, "processed")
    transformed_path = os.path.join(tmpdir, "transformed")
    subprocess.run(["mkdir", processed_path])

    def side_effect(df: pd.DataFrame, year: int) -> pd.DataFrame:
        return df.append({"year": f"{year}"}, ignore_index=True)

    mocker.patch("src.transformation.transform.transform_enade_year",
                 side_effect=side_effect)

    for year in [2017, 2014, 2011, 2008, 2005]:
        file_path = os.path.join(processed_path,
                                 f"microdados_processado_{year}.csv")
        with open(file_path, "w") as f:
            f.write("year\n0\n")

    # execute

    transform.main(processed_path, transformed_path)

    # assert
    for year in [2017, 2014, 2011, 2008, 2005]:
        file_path = os.path.join(transformed_path,
                                 f"microdados_transformados_{year}.csv")
        with open(file_path, "r") as f:
            data = f.read()
            assert data == f"year\n0\n{year}\n"


