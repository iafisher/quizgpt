#!/usr/bin/env python
import click

from quizgpt import cli, gpt, repetition, storage


@click.group()
def group():
    pass


@group.command("create")
@click.argument("subject")
def create_quiz(subject: str):
    raise NotImplementedError


@group.command("edit")
@click.argument("subject")
def edit_quiz(subject: str):
    raise NotImplementedError


@group.command("take")
@click.argument("subject")
@click.option("-n", type=int, default=5)
def take_quiz(subject: str, n: int):
    gpt.precheck()

    subject_obj = storage.fetch_subject(subject)
    questions = repetition.select_questions(subject_obj.questions, n)
    answers = []

    for index, question in enumerate(questions, start=1):
        answer = cli.ask_question(index, question)
        answers.append(answer)

    grades = gpt.grade(subject_obj.name, questions, answers)
    for question, answer, grade in zip(questions, answers, grades):
        print()
        print()
        cli.print_grade(question, answer, grade)


if __name__ == "__main__":
    group()
