from typing import List

from openai import OpenAI


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
            }
        ],
    )
    return response.choices[0].message.content.splitlines()
