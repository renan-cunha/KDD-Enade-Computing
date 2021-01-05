import pytest
from src.transformation.transform_2008 import Transform2008
import pandas as pd
from pytest_mock import MockerFixture
from typing import List, Tuple
import numpy as np
import subprocess
import os


class TestGetQuestionsIdsAndsLabels:

    @pytest.mark.parametrize("input,expected",
                             [
                                 (["general", "objective"], ([1,2,3,4,5,6,7,8], [0,1,2,3,4,5,6,7])),
                                 (["general", "discursive"], ([9, 10], [1, 2])),
                                 (["specific", "objective"], (list(range(11, 20)) + list(range(21, 38 + 1)), list(range(27)))),
                                 (["specific", "discursive"], ([20, 39, 40], [1, 2, 3]))
                              ])
    def test_get_questions_ids_and_labels(self, input, expected):
        transform2008 = Transform2008()
        test_type, question_format = input
        output = transform2008.get_questions_ids_and_labels(test_type,
                                                                  question_format)
        assert output[0] == expected[0]
        assert output[1] == expected[1]


