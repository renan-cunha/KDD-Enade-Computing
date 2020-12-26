from typing import List
from src.transformation.transform import Transform
import numpy as np


class Transform2005(Transform):

    @property
    def general_discursive_questions_ids(self) -> List[int]:
        return [8, 9, 10]

    @property
    def general_discursive_questions_labels(self) -> List[int]:
        return [1, 2, 3]

    @property
    def general_objective_questions_ids(self) -> List[int]:
        return list(range(1, 7 + 1))

    @property
    def general_objective_questions_labels(self) -> List[int]:
        return list(range(len(self.general_objective_questions_ids)))

    @property
    def specific_discursive_questions_ids(self) -> List[int]:
        return [25, 40]

    @property
    def specific_discursive_questions_labels(self) -> List[int]:
        return [3, 4]

    @property
    def specific_objective_questions_ids(self) -> List[int]:
        return list(range(11, 24 + 1)) + list(range(26, 39 + 1))

    @property
    def specific_objective_questions_labels(self):
        return list(range(28, len(self.specific_objective_questions_ids) + 28))
