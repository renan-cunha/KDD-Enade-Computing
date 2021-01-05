import pytest
from src.transformation.transform_2014_2017 import Transform2014_2017
import pandas as pd
from pytest_mock import MockerFixture
from typing import List, Tuple
import numpy as np


class TestGetQuestionsIdsAndsLabels:

    @pytest.mark.parametrize("input,expected",
                             [
                                 (["general", "objective"], ([3,4,5,6,7,8,9,10], [0,1,2,3,4,5,6,7])),
                                 (["general", "discursive"], ([1, 2], [1, 2])),
                                 (["specific", "objective"], ([list(range(14, 40 + 1)), list(range(27))])),
                                 (["specific", "discursive"], ([11, 12, 13], [1, 2, 3]))
                              ])
    def test_get_questions_ids_and_labels(self, input, expected):
        transform2014_2017 = Transform2014_2017()
        test_type, question_format = input
        output = transform2014_2017.get_questions_ids_and_labels(test_type,
                                                                  question_format)
        assert output[0] == expected[0]
        assert output[1] == expected[1]


