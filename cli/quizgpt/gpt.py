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
                    your input is the topic of the quiz. Each subsequent paragraph consists of two lines:
                    the original question, and the user's answer. Your output should have one line per
                    question. Each line must begin with either 'Correct', 'Partially correct', or 'Incorrect'.
                    If 'Partially correct' or 'Incorrect', it should be followed with a brief explanation
                    of why the answer is not completely correct.
                    """,
            },
            {
                "role": "user",
                "content": "Geography of the United States\n\nWhat is the capital of Michigan?\nAnn Arbor\n\nName the longest river in the United States.\nMississippi\n\nWhat is the largest city in California?\nLos Angeles\n",
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
