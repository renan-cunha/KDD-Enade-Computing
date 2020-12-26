import pytest
from src.process_enade import pre_process_old
from src.process2014_2017 import ProcessEnade2014_2017
from io import StringIO
import pandas as pd


def test_pre_process_old() -> None:
    input_csv = "test,vt_esc_ofg,vt_esc_oce,vt_ace_oce,vt_ace_ofg,nt_obj_ce\n" \
                "a,b,c,d,e,f"
    output_csv = "TEST,VT_ESC_OFG,VT_ESC_OCE,VT_ACE_OCE,VT_ACE_OFG,NT_OBJ_CE," \
                 "DS_VT_ESC_OFG,DS_VT_ESC_OCE,DS_VT_ACE_OCE,DS_VT_ACE_OFG\n" \
                "a,b,c,d,e,f,b,c,d,e"
    input_df = pd.read_csv(StringIO(input_csv))
    output_df = pre_process_old(input_df)
    expected_df = pd.read_csv(StringIO(output_csv))
    assert output_df.equals(expected_df)


data = [
        ("NT_FG_D1,NT_FG_D2,NT_CE_D1,TP_SFG_D1,TP_SFG_D2,TP_SCE_D1\n"
         "65,0,30,555,333,555",
         "QUESTAO_1_NOTA,QUESTAO_1_STATUS,QUESTAO_2_NOTA,QUESTAO_2_STATUS\n"
         "65,OK,BRANCO,OK", True, [1, 2], [1, 2], [3], [1]),
    ("NT_FG_D1,NT_FG_D2,NT_CE_D1,TP_SFG_D1,TP_SFG_D2,TP_SCE_D1\n"
     "0,0,30,335,333,555",
     "QUESTAO_1_NOTA,QUESTAO_1_STATUS,QUESTAO_2_NOTA,QUESTAO_2_STATUS\n"
     "0,NULA,BRANCO,OK", True, [1, 2], [1, 2], [3], [1]),
    ("NT_FG_D1,NT_FG_D2,NT_CE_D1,TP_SFG_D1,TP_SFG_D2,TP_SCE_D1\n"
     "0,0,30,335,333,555",
     "QUESTAO_3_NOTA,QUESTAO_3_STATUS\n"
     "30,OK", False, [1, 2], [1, 2], [3], [1]),
]


def auxiliar_function_scores(input: str, expected: str) -> tuple:
    input_df = pd.read_csv(StringIO(input), dtype={"DS_VT_ACE_OCE": str})
    expected_df = pd.read_csv(StringIO(expected))
    expected_df = pd.concat([input_df.copy(), expected_df], axis=1)
    process_2017 = ProcessEnade2014_2017(2017)
    return process_2017, expected_df, input_df


@pytest.mark.parametrize("input, expected, key, gen_ids, gen_labels, "
                         "spe_ids, spe_labels", data)
def test_discursive_scores(input: str, expected: str, key: bool, gen_ids: list,
                           gen_labels: list, spe_ids: list,
                           spe_labels: list) -> None:
    process_2017, expected_df, input_df = auxiliar_function_scores(input, expected)
    process_2017.GEN_DIS_QUESTIONS_LABEL = gen_labels
    process_2017.GEN_DIS_QUESTIONS_ID = gen_ids
    process_2017.SPE_DIS_QUESTIONS_LABEL = spe_labels
    process_2017.SPE_DIS_QUESTIONS_ID = spe_ids
    output_df = process_2017.transform_discursive_scores(input_df, key)
    expected_df = expected_df.astype(output_df.dtypes)
    assert output_df.equals(expected_df)


input_csv_objective_columns = "DS_VT_ACE_OFG,DS_VT_ACE_OCE,DS_VT_ESC_OFG," \
                           "DS_VT_ESC_OCE\n" \

objective_data = [
    (input_csv_objective_columns + "900019,10009,A.*BC.,E.*AB",
     ",".join([f"QUESTAO_{x}_NOTA,QUESTAO_{x}_STATUS" for x in range(1, 7)]) + "\n"
     "NULA,NULA,BRANCO,OK,RASURA,OK,0,OK,100,OK,BRANCO,NULA",
     True, [1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4, 5], [7, 8, 9, 10, 11], [0, 1, 2, 3, 4]),
    (input_csv_objective_columns + "01,0001,AB,..AB",
     ",".join(
         [f"QUESTAO_{x}_NOTA,QUESTAO_{x}_STATUS" for x in [11, 13]]) + "\n"
        "0,OK,100,OK",
     False, [1, 2], [0, 1], [11, 13],
     [2, 3]),
]


@pytest.mark.parametrize("input, expected, key, gen_ids, gen_labels, "
                         "spe_ids, spe_labels", objective_data)
def test_objective_scores(input: str, expected: str, key: bool, gen_ids: list,
                           gen_labels: list, spe_ids: list,
                           spe_labels: list) -> None:
    process_2017, expected_df, input_df = auxiliar_function_scores(input, expected)
    process_2017.GEN_OBJ_QUESTIONS_LABEL = gen_labels
    process_2017.GEN_OBJ_QUESTIONS_ID = gen_ids
    process_2017.SPE_OBJ_QUESTIONS_LABEL = spe_labels
    process_2017.SPE_OBJ_QUESTIONS_ID = spe_ids
    expected_df = expected_df.astype(str)
    input_df = input_df.astype(str)
    output_df = process_2017.get_objective_scores(input_df, key)
    output_df = output_df.astype(str)
    assert output_df.equals(expected_df)


def test_set_year_raise():
    process2017 = ProcessEnade2014_2017(2017)
    with pytest.raises(ValueError):
        process2017.set_year(2015)


set_year_data = [2017, 2014]
@pytest.mark.parametrize("year", set_year_data)
def test_set_year(year: int) -> None:
    process2017 = ProcessEnade2014_2017(abs(year-3))
    process2017.set_year(year)


