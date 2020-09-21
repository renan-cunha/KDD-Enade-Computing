import pytest
from io import StringIO
import pandas as pd
from src import util

get_subjects_columns = "conteudo1,conteudo2,conteudo3"

get_subjects_data = [(f"{get_subjects_columns}\nTeoria dos Grafos,,",
                     ["Teoria dos Grafos"]),
                     (f"{get_subjects_columns}\nTeoria dos Grafos,,\nCompiladores,,",
                     ["Teoria dos Grafos", "Compiladores"]),
                     (f"{get_subjects_columns}\nTeoria dos Grafos,,\nTeoria dos Grafos,,",
                     ["Teoria dos Grafos"]),
                     (f"{get_subjects_columns}\nCompiladores,Grafos,\nGrafos,,",
                     ["Compiladores", "Grafos"]),
                     (f"{get_subjects_columns}\nCompiladores,Grafos,",
                     ["Compiladores", "Grafos"]),
                     ]


@pytest.mark.parametrize("input, expected", get_subjects_data)
def test_get_subjects(input: str, expected: list) -> None:
    df = pd.read_csv(StringIO(input))
    subjects = util.get_subjects(df)
    assert sorted(subjects.tolist()) == sorted(expected)