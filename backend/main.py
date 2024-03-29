from typing import List

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

import quiz_service
import storage

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = storage.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/subjects/list")
def get_subject_list(db: Session = Depends(get_db)):
    subject_list = db.query(storage.Subject).all()
    return dict(subjects=[subject_to_json(subject) for subject in subject_list])


@app.get("/subjects/get/{subject_id}")
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = (
        db.query(storage.Subject)
        .filter(storage.Subject.subject_id == subject_id)
        .first()
    )
    return subject_to_json(subject)


class SubjectCreate(BaseModel):
    name: str
    description: str
    instructions: str


@app.post("/subjects/create")
def create_subject(subject: SubjectCreate, db: Session = Depends(get_db)):
    db_subject = storage.Subject(
        name=subject.name,
        description=subject.description,
        instructions=subject.instructions,
    )
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return dict(created=subject_to_json(db_subject))


class QuizGenerate(BaseModel):
    subject_id: int


@app.post("/quizzes/generate")
def generate_quiz(request: QuizGenerate, db: Session = Depends(get_db)):
    # TODO: handle missing subject
    db_subject = (
        db.query(storage.Subject)
        .filter(storage.Subject.subject_id == request.subject_id)
        .first()
    )
    return dict(questions=[question_to_json(q) for q in db_subject.questions])


class QuizGrade(BaseModel):
    subject: str
    questions: List[str]
    answers: List[str]


@app.post("/quizzes/grade")
def grade_quiz(request: QuizGrade):
    responses = quiz_service.grade(request.subject, request.questions, request.answers)
    results = [
        dict(
            text=request.questions[i],
            answer=request.answers[i],
            comment=responses[i],
        )
        for i in range(len(responses))
    ]
    return dict(results=results)


def subject_to_json(subject) -> dict:
    return dict(
        subjectId=subject.subject_id,
        name=subject.name,
        description=subject.description,
        questions=[question_to_json(q) for q in subject.questions],
    )


def question_to_json(question) -> dict:
    return dict(
        questionId=question.question_id,
        text=question.text,
        rephrase=question.rephrase,
    )
