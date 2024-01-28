import random
from typing import List

from .types import Question


def select_questions(questions: List[Question], n: int) -> List[Question]:
    # TODO: actual spaced-repetition algorithm
    shuffled = questions.copy()
    random.shuffle(shuffled)
    return shuffled[:n]
