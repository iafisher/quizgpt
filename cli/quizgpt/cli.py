import shutil
import textwrap

from .types import Question


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
