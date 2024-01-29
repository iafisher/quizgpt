import shutil
import textwrap
from typing import Any, List, Optional

from .types import Question, Subject


def ask_question(index: int, question: Question) -> str:
    _print_wrapped(f"{index:>3}. {question.text}")
    print()
    response = input("   > ")
    print()
    return response.strip()


def print_grade(question: Question, answer: str, grade: str) -> None:
    _print_wrapped(f"Question: {question.text}")
    print()
    _print_wrapped(f"Your answer: {answer}")
    print()
    _print_wrapped(f"QuizGPT: {grade}")


def _print_wrapped(s: str) -> None:
    columns, _ = shutil.get_terminal_size()
    print(textwrap.fill(s, width=columns))


def select(options: List[Any], *, key: Optional[callable] = None) -> Any:
    if key is None:
        key = lambda x: x

    for i, option in enumerate(options, start=1):
        print(f"({i}) {key(option)}")

    print()
    while True:
        response = input("Choose: ")
        try:
            index = int(response)
        except ValueError:
            continue

        index = index - 1
        if index < 0 or index >= len(options):
            continue

        return options[index]


def print_question(question: Question) -> None:
    print(
        f"{question.question_id:>6}  {question.text}  (subject: {question.subject_name})"
    )


def print_subject(subject: Subject) -> None:
    print(
        f"{subject.subject_id:>6}  {subject.name:<50}  ({pluralize(len(subject.questions), 'question')})"
    )


def pluralize(n: int, word: str, plural: Optional[str] = None) -> str:
    if n == 1:
        return f"{n} {word}"
    else:
        return f"{n} {plural or (word + 's')}"
