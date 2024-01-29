#!/usr/bin/env python
import json
from typing import Optional

import click
from sqlalchemy.orm import Session

from quizgpt import cli, gpt, repetition, storage
from quizgpt.cli import pluralize
from quizgpt.types import QuizGptException, Subject


@click.group()
def group():
    pass


@group.command("add")
@click.argument("subject", required=False)
def add_question(subject: Optional[str]):
    with storage.new_session() as session:
        subject_obj = get_subject(session, subject)

        text = input("Enter the question text: ").strip()
        storage.create_question(session, subject_obj.subject_id, text)


@group.command("create")
def create_subject():
    subject_name = input("Enter the name of the subject: ").strip()
    with storage.new_session() as session:
        storage.create_subject(session, subject_name)


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


@group.command
def recreate_db():
    if not cli.confirm("Re-create the database and delete all existing data? "):
        print("Aborted.")
        return

    storage.recreate_db()


@group.command("search")
@click.argument("term")
def search_questions(term: str):
    with storage.new_session() as session:
        search_results = storage.search_questions(session, term)
        if search_results:
            for question in search_results:
                print(f"{question.question_id:>6}  {question.text}  (subject: {question.subject_name})")
        else:
            print("No results found.")


@group.command("take")
@click.argument("subject", required=False)
@click.option("-n", type=int, default=5)
def take_quiz(subject: Optional[str], n: int):
    gpt.precheck()

    with storage.new_session() as session:
        subject_obj = get_subject(session, subject)

        questions = repetition.select_questions(subject_obj.questions, n)
        answers = []

        for index, question in enumerate(questions, start=1):
            answer = cli.ask_question(index, question)
            answers.append(answer)

        # TODO: display timing data
        grades = gpt.grade(subject_obj.name, questions, answers)
        storage.save_quiz_result(
            session, subject_obj.subject_id, questions, answers, grades
        )

        for question, answer, grade in zip(questions, answers, grades):
            print()
            print()
            cli.print_grade(question, answer, grade)


def get_subject(session: Session, subject_name: Optional[str]) -> Subject:
    if subject_name is None:
        subject_list = storage.fetch_all_subjects(session)
        r = cli.select(subject_list, key=lambda x: x.name)
        print()
        print()
        return r
    else:
        return storage.fetch_subject(session, subject_name)


if __name__ == "__main__":
    try:
        group()
    except QuizGptException as e:
        print(f"Error: {e}")
