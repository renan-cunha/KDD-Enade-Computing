import pytest
import pandas as pd
from io import StringIO
from src.subject_manipulation import split_general_subjects, \
    get_objective_questions, get_processed_subject_df
from src.config import DIR_PATH
import os


columns = "prova,objeto,conteudo1,conteudo2,conteudo3"

data = [(f"{columns}\nGeral,Ola;meu;amigo,,,",
         f"{columns}\nGeral,Ola;meu;amigo,Ola,meu,amigo"),
        (f"{columns}\nGeral,Ola;meu,,,",
         f"{columns}\nGeral,Ola;meu,Ola,meu,"),
        (f"{columns}\nGeral,Ola,,,",
         f"{columns}\nGeral,Ola,Ola,,"),
        (f"{columns}\nGeral,Ola;meu;amigo,,,\nEspecífica,oi;eai;fala,,,",
         f"{columns}\nGeral,Ola;meu;amigo,Ola,meu,amigo\n"
         f"Específica,oi;eai;fala,,,")
        ]


@pytest.mark.parametrize("input, expected", data)
def test_split_general_subjects(input: str, expected: str) -> None:
    input_df = pd.read_csv(StringIO(input))
    split_general_subjects(input_df)
    expected_df = pd.read_csv(StringIO(expected))
    assert input_df.equals(expected_df)


raise_data = [f"{columns}\nGeral,,,,",
        f"{columns}\nGeral,Ola;meu;amigo;feliz,,,",
        ]


@pytest.mark.parametrize("input", raise_data)
def test_expect_raise_split_general_subjects(input: str) -> None:
    input_df = pd.read_csv(StringIO(input))
    with pytest.raises(ValueError):
        split_general_subjects(input_df)


def test_get_objective_questions() -> None:

    csv_str = "tipoquestao,idquestao\n" \
              "Objetiva,0\n" \
              "Discursiva,1\n" \
              "Objetiva,2"
    df = pd.read_csv(StringIO(csv_str))
    output = get_objective_questions(df)
    expected = [0, 2]
    assert expected == output


get_processed_subject_df_data = [(1, True), (2, False)]


@pytest.mark.parametrize("id, key", get_processed_subject_df_data)
def test_get_processed_subject_df(id: int, key: bool) -> None:
    df = get_processed_subject_df(os.path.join(DIR_PATH, "test",
                                          f"input_processed_subject_df_{id}.csv"), key)

    expected_df = pd.read_csv(os.path.join(DIR_PATH, "test",
                                           f"output_processed_subject_df_{id}.csv"),
                              dtype={
                                       "ano": int})


    print(df[["conteudo1", "conteudo2", "conteudo3"]].dtypes)
    print(expected_df[["conteudo1", "conteudo2", "conteudo3"]].dtypes)
    assert df.equals(expected_df)


def test_get_processed_subject_df_error() -> None:

    with pytest.raises(ValueError):
        df = get_processed_subject_df(os.path.join(DIR_PATH, "test",
                                                   f"input_processed_subject_df_raise.csv"))
