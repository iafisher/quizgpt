from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column, relationship, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.sqlite3"

# check_same_thread=False to allow FastAPI concurrency.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=dict(check_same_thread=False)
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Subject(Base):
    __tablename__ = "subjects"

    subject_id = mapped_column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    questions = relationship("Question", back_populates="subject")


class Question(Base):
    __tablename__ = "questions"

    question_id = Column(Integer, primary_key=True)
    subject_id = mapped_column(Integer, ForeignKey("subjects.subject_id"))
    text = Column(String)
    rephrase = Column(Boolean)

    subject = relationship("Subject", back_populates="questions")
