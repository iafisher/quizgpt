#!/usr/bin/env python
import json
from typing import Optional

import click

from quizgpt import cli, gpt, repetition, storage
from quizgpt.cli import pluralize
from quizgpt.types import QuizGptException


@click.group()
def group():
    pass


@group.command("create")
@click.argument("subject")
def create_subject(subject: str):
    raise NotImplementedError


@group.command("edit")
@click.argument("subject")
def edit_subject(subject: str):
    raise NotImplementedError


@group.command("import")
@click.argument("input", type=click.File("r"))
def import_subject(input: click.File):
    data = json.load(input)

    with storage.new_session() as session:
        storage.import_json(session, data)


@group.command("list")
def list_subjects():
    with storage.new_session() as session:
        subject_list = storage.fetch_all_subjects(session)

        if not subject_list:
            print("No subjects found in database.")
            return

        for subject in subject_list:
            print(f"{subject.name} ({pluralize(len(subject.questions), 'question')})")

        print()
        print(f"{pluralize(len(subject_list), 'subject')} in database.")


@group.command("take")
@click.argument("subject", required=False)
@click.option("-n", type=int, default=5)
def take_quiz(subject: Optional[str], n: int):
    gpt.precheck()

    with storage.new_session() as session:
        if subject is None:
            subject_list = storage.fetch_all_subjects(session)
            subject_obj = cli.select(subject_list, key=lambda x: x.name)
            print()
            print()
        else:
            subject_obj = storage.fetch_subject(session, subject)

        questions = repetition.select_questions(subject_obj.questions, n)
        answers = []

        for index, question in enumerate(questions, start=1):
            answer = cli.ask_question(index, question)
            answers.append(answer)

        # TODO: display timing data
        grades = gpt.grade(subject_obj.name, questions, answers)
        for question, answer, grade in zip(questions, answers, grades):
            print()
            print()
            cli.print_grade(question, answer, grade)


if __name__ == "__main__":
    try:
        group()
    except QuizGptException as e:
        print(f"Error: {e}")
