from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from src.database.connection import Base


class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)  # "easy" | "medium" | "hard"
    statement = Column(Text, nullable=False)      # markdown/html problem statement
    solution_code = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    test_cases = relationship(
        "TestCase",
        back_populates="problem",
        cascade="all, delete-orphan",  # deleting a Problem deletes its TestCases too
    )


class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(
        Integer,
        ForeignKey("problems.id", ondelete="CASCADE"),
        nullable=False,
    )
    input = Column(Text, nullable=False)   # can contain multiple lines
    output = Column(Text, nullable=False)  # can contain multiple lines

    problem = relationship("Problem", back_populates="test_cases")