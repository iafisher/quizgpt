import math
import time
from typing import List

import pydantic
import sqlalchemy.exc
from sqlalchemy import ForeignKey, Integer, String, create_engine, select
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
            questions=[question.to_dataclass() for question in self.questions],
        )


class StoredQuestion(Base):
    __tablename__ = "question"

    question_id: Mapped[int] = mapped_column(primary_key=True)
    # TODO: specify on_delete behavior of foreign-key fields
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.subject_id"))
    text: Mapped[str] = mapped_column(String)

    subject: Mapped["StoredSubject"] = relationship(back_populates="questions")

    def to_dataclass(self) -> Question:
        return Question(
            subject_name=self.subject.name, question_id=self.question_id, text=self.text
        )


class StoredQuizResult(Base):
    __tablename__ = "quiz_result"

    quiz_result_id: Mapped[int] = mapped_column(primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.subject_id"))
    time_finished_secs: Mapped[int] = mapped_column(Integer)

    question_results: Mapped[List["StoredQuestionResult"]] = relationship()


class StoredQuestionResult(Base):
    __tablename__ = "question_result"

    question_result_id: Mapped[int] = mapped_column(primary_key=True)
    quiz_result: Mapped[int] = mapped_column(ForeignKey("quiz_result.quiz_result_id"))
    question: Mapped[str] = mapped_column(String)
    answer: Mapped[str] = mapped_column(String)
    grade: Mapped[str] = mapped_column(String)


# TODO: make configurable
DB_PATH = "sqlite:///quizgpt.sqlite3"


def new_session():
    engine = create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    return Session(engine)


def recreate_db():
    engine = create_engine(DB_PATH)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def fetch_subject_by_name(session: Session, name: str) -> Subject:
    stmt = select(StoredSubject).where(StoredSubject.name == name)
    try:
        subject = session.scalars(stmt).one()
    except sqlalchemy.exc.NoResultFound:
        raise QuizGptException(f"No subject named {name!r} found.")

    return subject.to_dataclass()


def fetch_subject_by_id(session: Session, subject_id: int) -> Subject:
    stmt = select(StoredSubject).where(StoredSubject.subject_id == subject_id)
    try:
        subject = session.scalars(stmt).one()
    except sqlalchemy.exc.NoResultFound:
        raise QuizGptException(f"No subject {subject_id} not found.")

    return subject.to_dataclass()


def fetch_all_subjects(session: Session) -> List[Subject]:
    subject_list = session.scalars(select(StoredSubject).order_by(StoredSubject.name))
    return [subject.to_dataclass() for subject in subject_list]


def save_quiz_result(
    session: Session,
    subject_id: int,
    questions: List[Question],
    answers: List[str],
    grades: List[str],
) -> None:
    time_finished_secs = math.floor(time.time())

    question_results_to_add = []
    for question, answer, grade in zip(questions, answers, grades):
        question_results_to_add.append(
            StoredQuestionResult(question=question.text, answer=answer, grade=grade)
        )

    # TODO: do I need to call session.begin() to open a transaction?
    quiz_result = StoredQuizResult(
        subject_id=subject_id,
        question_results=question_results_to_add,
        time_finished_secs=time_finished_secs,
    )
    session.add(quiz_result)
    session.commit()


def create_question(session: Session, subject_id: int, text: str) -> None:
    question = StoredQuestion(subject_id=subject_id, text=text)
    session.add(question)
    session.commit()


def create_subject(session: Session, subject_name: str) -> None:
    subject = StoredSubject(name=subject_name)
    session.add(subject)
    session.commit()


def search_questions(session: Session, term: str) -> List[Question]:
    stored_questions = session.scalars(select(StoredQuestion).where(StoredQuestion.text.ilike(f"%{term}%")))
    return [q.to_dataclass() for q in stored_questions]


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
