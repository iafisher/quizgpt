from typing import List

import pydantic
import sqlalchemy.exc
from sqlalchemy import ForeignKey, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

from .types import Question, QuizGptException, Subject


class Base(DeclarativeBase):
    pass


class StoredSubject(Base):
    __tablename__ = "subject"

    subject_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)

    questions: Mapped[List["StoredQuestion"]] = relationship(back_populates="subject")

    def to_dataclass(self) -> Subject:
        return Subject(
            subject_id=self.subject_id,
            name=self.name,
            questions=[
                Question(question_id=question.question_id, text=question.text)
                for question in self.questions
            ],
        )


class StoredQuestion(Base):
    __tablename__ = "question"

    question_id: Mapped[int] = mapped_column(primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.subject_id"))
    text: Mapped[str] = mapped_column(String)

    subject: Mapped["StoredSubject"] = relationship(back_populates="questions")


def new_session():
    engine = create_engine("sqlite:///quizgpt.sqlite3")
    Base.metadata.create_all(engine)
    return Session(engine)


def fetch_subject(session: Session, name: str) -> Subject:
    stmt = select(StoredSubject).where(StoredSubject.name == name)
    try:
        subject = session.scalars(stmt).one()
    except sqlalchemy.exc.NoResultFound:
        raise QuizGptException(f"No subject named {name!r} found.")

    return subject.to_dataclass()


def fetch_all_subjects(session: Session) -> List[Subject]:
    subject_list = session.scalars(select(StoredSubject).order_by(StoredSubject.name))
    return [subject.to_dataclass() for subject in subject_list]


class ImportQuestion(pydantic.BaseModel):
    text: str


class Import(pydantic.BaseModel):
    name: str
    questions: List[ImportQuestion]


def import_json(session: Session, data: dict) -> None:
    try:
        validated_data = Import(**data)
    except pydantic.ValidationError:
        # TODO: surface detailed pydantic errors
        raise QuizGptException("The import file did not match the expected schema.")

    questions_to_add = [
        StoredQuestion(text=import_question.text)
        for import_question in validated_data.questions
    ]
    subject = StoredSubject(name=validated_data.name, questions=questions_to_add)
    session.add(subject)

    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise QuizGptException(
            "Unable to import the data into the database. Does a subject of the same name already exist?"
        )
