import pytest
from src.transformation.transform_2011 import Transform2011
import pandas as pd
from pytest_mock import MockerFixture
from typing import List, Tuple
import numpy as np


class TestGetQuestionsIdsAndsLabels:

    @pytest.mark.parametrize("input,expected",
                             [
                                 (["general", "objective"], ([1,2,3,4,5,6,7,8], [0,1,2,3,4,5,6,7])),
                                 (["general", "discursive"], ([9, 10], [1, 2])),
                                 (["specific", "objective"], (list(range(14, 40 + 1)), list(range(22)) + list(range(27, 32)))),
                                 (["specific", "discursive"], ([11, 12, 13], [1, 2, 3]))
                              ])
    def test_get_questions_ids_and_labels(self, input, expected):
        transform2011 = Transform2011()
        test_type, question_format = input
        output = transform2011.get_questions_ids_and_labels(test_type,
                                                                  question_format)
        assert output[0] == expected[0]
        assert output[1] == expected[1]


