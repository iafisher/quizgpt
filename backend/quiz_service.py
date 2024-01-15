from typing import List

from openai import OpenAI

# TODO: validate OpenAI key is set on server start-up


def generate(instructions: str) -> List[str]:
    client = OpenAI()
    # TODO: have GPT generate JSON instead of unstructured text
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """
                You are a quiz-master AI who creates quizzes on topics that the user supplies.
                You can vary between questions that require a single term, name, or date as an
                answer, and questions that require a paragraph of text. It's okay to ask
                questions with subjective answers, but don't ask questions that are purely about
                personal preferences or taste. The questions should cover general knowledge, for
                example what you might read in Wikipedia. You will be prompted with the topics to
                cover in the quiz and you will respond with 5 questions, each on their own line.
                """,
            },
            {
                "role": "user",
                "content": "The geography of the United States, emphasizing human geography (e.g., capitals, states, etc.)",
            },
            {
                "role": "assistant",
                "content": "What is the capital of Michigan?\nWhich two states are not contiguous with the rest of the country?\nDescribe the physical geography of the American West.\nWhat long river ends at the Gulf of Mexico and drains most of the Great Plains?\nWhat is the largest city in Nebraska?\n",
            },
            {
                "role": "user",
                "content": instructions,
            },
        ],
    )
    return response.choices[0].message.content.splitlines()


def grade(subject: str, questions: List[str], answers: List[str]) -> List[str]:
    prompt_builder = [subject]
    for i in range(len(questions)):
        # TODO: do more validation on user input
        prompt_builder.append(questions[i].strip() + "\n" + answers[i].replace("\n", "").strip() + "\n")
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
