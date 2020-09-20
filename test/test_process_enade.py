import pytest
from src.process_enade import pre_process_old
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
    print(output_df)
    print(expected_df)
    assert output_df.equals(expected_df)
