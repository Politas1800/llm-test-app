from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="Viewer")
    tests = relationship("Test", back_populates="creator")

class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    user_message = Column(String)
    review_message = Column(String)
    num_requests = Column(Integer)
    selected_llms = Column(String)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    published = Column(Boolean, default=False)
    creator_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="tests")
    results = relationship("TestResult", back_populates="test", cascade="all, delete-orphan")

class TestResult(Base):
    __tablename__ = "test_results"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("tests.id"))
    llm_provider = Column(String)
    llm_model = Column(String)
    response = Column(String)
    is_correct = Column(Boolean)
    test = relationship("Test", back_populates="results")
