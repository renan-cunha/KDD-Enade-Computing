from typing import List
from src.transformation.transform import Transform
import numpy as np


class Transform2008(Transform):

    @property
    def general_discursive_questions_ids(self) -> List[int]:
        return [9, 10]

    @property
    def general_discursive_questions_labels(self) -> List[int]:
        return [1, 2]

    @property
    def general_objective_questions_ids(self) -> List[int]:
        return list(range(1, 8 + 1))

    @property
    def general_objective_questions_labels(self) -> List[int]:
        return list(range(len(self.general_objective_questions_ids)))

    @property
    def specific_discursive_questions_ids(self) -> List[int]:
        return [20, 39, 40]

    @property
    def specific_discursive_questions_labels(self) -> List[int]:
        return [1, 2, 3]

    @property
    def specific_objective_questions_ids(self) -> List[int]:
        return list(range(11, 20)) + list(range(21, 38 + 1))

    @property
    def specific_objective_questions_labels(self):
        return list(range(len(self.specific_objective_questions_ids)))
