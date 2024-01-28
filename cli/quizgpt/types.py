from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Question:
    text: str
    answer: Optional[str]


@dataclass
class Subject:
    name: str
    questions: List[Question]
