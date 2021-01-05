import pytest
import os
from src.transformation import transform
from pytest_mock import MockerFixture
import pandas as pd
import subprocess
import numpy as np


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


@pytest.mark.make
class TestMake:

    score_columns = [f"QUESTAO_{x}_NOTA" for x in range(1, 40 + 1)]
    situation_columns = [f"QUESTAO_{x}_SITUACAO" for x in range(1, 40 + 1)]

    @pytest.mark.parametrize("year", [2017, 2014, 2011, 2008, 2005])
    def test_make_have_columns(self, year: int) -> None:
        df = transform.read_csv(year)
        columns = TestMake.score_columns + TestMake.situation_columns
        for column in columns:
            assert column in df.columns

    @pytest.mark.parametrize("year", [2017, 2014, 2011, 2008, 2005])
    def test_make_score_columns_format(self, year: int):
        df = transform.read_csv(year)
        for column in TestMake.score_columns:
            column_series = df[column]
            assert column_series.dtype == float
            column_series_dropped = df[column].dropna()
            if len(column_series_dropped > 0):
                assert column_series_dropped.min() >= 0
                assert column_series.max() <= 100

    @pytest.mark.parametrize("year", [2017, 2014, 2011, 2008, 2005])
    def test_make_situation_columns_format(self, year: int):
        df = transform.read_csv(year)
        possible_values = {np.nan, "ok", "branco", "rasura"}
        for column in TestMake.situation_columns:
            column_series = df[column]
            if len(column_series.dropna()) > 0:
                assert column_series.dtype == object
                current_values = set(pd.unique(column_series))
                assert current_values.issubset(possible_values)


@pytest.mark.make()
class TestQuestions:

    cancelled_questions_2017 = [26, 30, 31]
    cancelled_questions_2014 = [16, 23, 26, 36, 38, 39]
    cancelled_questions_2011 = [18, 22, 28, 29, 38, 40]
    cancelled_questions_2005 = [11, 26, 27, 34, 36, 39, 40]

    situation_possible_values = {"ok", 'branco', 'rasura'}

    @pytest.mark.parametrize("year,questions_ids", [(2017, cancelled_questions_2017),
                                                (2014, cancelled_questions_2014),
                                                (2011, cancelled_questions_2011),
                                                (2005, cancelled_questions_2005)])
    def test(self, year, questions_ids):
        situation_columns = [f"QUESTAO_{x}_SITUACAO" for x in questions_ids]
        df = transform.read_csv(year)
        df_isna = df[situation_columns].isna()
        all_df_is_na = df_isna.all()
        assert all_df_is_na.all()


@pytest.mark.make()
class TestQuestionsMeanScore:

    expected_df = pd.read_csv("tests/test_mean_score_question_id.csv",
                              decimal=",")

    @pytest.mark.parametrize("year", [2017, 2014, 2011, 2008, 2005])
    def test_year(self, year: int) -> None:
        # arrange
        expected = TestQuestionsMeanScore.expected_df.copy()
        expected_year = expected.loc[expected["ano"] == year, ["acertosbrasil", "id"]]
        expected_year_mean_values = expected_year["acertosbrasil"].values.flatten()

        # execute
        df = transform.read_csv(year)
        present_df = df.loc[df['TP_PRES'].isin([555])]
        score_columns = [f"QUESTAO_{x}_NOTA" for x in expected_year['id']]
        present_df_mean_score = present_df[score_columns].mean()
        present_df_mean_score_values = present_df_mean_score.values.flatten()
        result = present_df_mean_score_values - expected_year_mean_values

        # assert
        assert max(abs(result)) == pytest.approx(0, abs=1.0)

