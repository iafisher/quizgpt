from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

import storage

app = FastAPI()


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


@app.post("/quizzes/generate")
def generate_quiz():
    raise NotImplementedError


@app.post("/quizzes/grade")
def grade_quiz():
    raise NotImplementedError


def subject_to_json(subject) -> dict:
    return dict(
        subjectId=subject.subject_id,
        name=subject.name,
        description=subject.description,
    )
