import os
from typing import List

from openai import OpenAI

from .types import Question, QuizGptException


def precheck() -> None:
    if "OPENAI_API_KEY" not in os.environ:
        raise QuizGptException("OPENAI_API_KEY environment variable must be set.")


def grade(subject: str, questions: List[Question], answers: List[str]) -> List[str]:
    prompt_builder = [subject]
    for question, answer in zip(questions, answers):
        # TODO: do more validation on user input
        prompt_builder.append(
            question.text.strip() + "\n" + answer.replace("\n", "").strip() + "\n"
        )
    prompt = "\n\n".join(prompt_builder)

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """
                    You are a quiz-master AI who grades user responses to questions. The first line of
                    your input is the topic of the quiz. Each subsequent paragraph consists of three
                    lines: the original question, the suggested answer, and the user's answer. The
                    suggested answer may be blank. Your output should have one line per question. Each
                    line must begin with either 'Correct', 'Partially correct', or 'Incorrect'. If
                    'Partially correct' or 'Incorrect', it should be followed with a brief explanation
                    of why the answer is not completely correct.
                    """,
            },
            {
                "role": "user",
                "content": "Geography of the United States\n\nWhat is the capital of Michigan?\n\nAnn Arbor\n\nName the longest river in the United States.\nMississippi or Missouri\nMississippi\n\nWhat is the largest city in California?\nLos Angeles\nLos Angeles\n",
            },
            {
                "role": "assistant",
                "content": "Incorrect. The capital of Michigan is Lansing.\nPartially correct. The Mississippi River is the primary river of the longest river system in the US, but the longest single river is its tributary, the Missouri River.\nCorrect.\n",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    lines = response.choices[0].message.content.splitlines()
    return [line for line in lines if line]


def create_variants(text: str) -> List[str]:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """
                    You are a quiz-master AI who helps users create their own quizzes and study guides. You
                    will be given the text of a question, and you should output 2 variants of the same
                    question with different wording, each on their own line. Make them different enough to
                    be distinctive, but don't change the meaning of the question.
                    """,
            },
            {
                "role": "user",
                "content": "What American investor is known for managing Fidelity's Magellan Fund",
            },
            {
                "role": "assistant",
                "content": "Name the US investor who managed the Fidelty fund for Magellan.\nFidelity's Magellan Fund was managed by what investor?",
            },
            {
                "role": "user",
                "content": text,
            },
        ],
    )
    lines = response.choices[0].message.content.splitlines()
    return [line for line in lines if line]
