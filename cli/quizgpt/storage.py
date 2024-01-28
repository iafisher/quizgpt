from .types import Question, Subject


def fetch_subject(name: str) -> Subject:
    return Subject(
        name="Post-war American history",
        questions=[
            Question("What was the significance of Brown v. Board of Education in 1954?", None),
            Question("What were the key events and consequences of the Watergate scandal?", None),
            Question("How did the end of the Cold War impact American foreign policy?", None),
            Question("Who was the Republican nominee for president in 1960?", None),
            Question("Summarize the 1956 Suez crisis.", None),
        ]
    )
