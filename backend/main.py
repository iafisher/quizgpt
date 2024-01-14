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
    subject = db.query(storage.Subject).filter(storage.Subject.subject_id == subject_id).first()
    return subject_to_json(subject)


class SubjectCreate(BaseModel):
    name: str
    description: str
    instructions: str


@app.post("/subjects/create")
def create_subject(subject: SubjectCreate, db: Session = Depends(get_db)):
    db_subject = storage.Subject(name=subject.name, description=subject.description, instructions=subject.instructions)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return dict(created=subject_to_json(db_subject))


class QuizGenerate(BaseModel):
    subject_id: int


@app.post("/quizzes/generate")
def generate_quiz(request: QuizGenerate, db: Session = Depends(get_db)):
    # TODO: handle missing subject
    db_subject = db.query(storage.Subject).filter(storage.Subject.subject_id == request.subject_id).first()
    questions = quiz_service.generate(db_subject.instructions)
    return dict(questions=[dict(text=text) for text in questions])


@app.post("/quizzes/grade")
def grade_quiz():
    raise NotImplementedError


def subject_to_json(subject) -> dict:
    return dict(
        subjectId=subject.subject_id,
        name=subject.name,
        description=subject.description,
        instructions=subject.instructions,
    )
