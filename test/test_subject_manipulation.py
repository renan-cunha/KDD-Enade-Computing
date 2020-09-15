import pytest
import pandas as pd
from io import StringIO
from src.subject_manipulation import split_general_subjects


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
