from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.sqlite3"

# check_same_thread=False to allow FastAPI concurrency.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=dict(check_same_thread=False)
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Subject(Base):
    __tablename__ = "subjects"

    subject_id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def to_json(self) -> dict:
        return dict(
            subjectId=self.subject_id,
            name=self.name,
            description=self.description,
        )
