from typing import List
import os
import sys
parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')) #this should give you absolute location of my_project folder.
sys.path.append(parent)
from src.transformation.transform_abstract import Transform


class Transform2014_2017(Transform):

    @property
    def general_discursive_questions_ids(self) -> List[int]:
        return [1, 2]

    @property
    def general_discursive_questions_labels(self) -> List[int]:
        return self.general_discursive_questions_ids

    @property
    def general_objective_questions_ids(self) -> List[int]:
        return list(range(3, 10 + 1))

    @property
    def general_objective_questions_labels(self) -> List[int]:
        return list(range(len(self.general_objective_questions_ids)))

    @property
    def specific_discursive_questions_ids(self) -> List[int]:
        return [11, 12, 13]

    @property
    def specific_discursive_questions_labels(self) -> List[int]:
        return [1, 2, 3]

    @property
    def specific_objective_questions_ids(self) -> List[int]:
        return list(range(14, 40 + 1))

    @property
    def specific_objective_questions_labels(self):
        return list(range(len(self.specific_objective_questions_ids)))

