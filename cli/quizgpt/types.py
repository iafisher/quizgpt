from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Question:
    subject_name: str
    question_id: int
    text: str


@dataclass
class Subject:
    subject_id: int
    name: str
    questions: List[Question]


class QuizGptException(Exception):
    pass
