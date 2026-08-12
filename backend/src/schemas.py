from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class TestCaseSchema(BaseModel):
    id: Optional[int] = None
    input: str
    output: str

    class Config:
        from_attributes = True  # lets this read directly from SQLAlchemy objects


class ProblemOut(BaseModel):
    id: int
    title: str
    difficulty: str
    statement: str
    solution_code: str
    created_at: Optional[datetime]
    test_cases: List[TestCaseSchema] = []

    class Config:
        from_attributes = True


class ProblemCreateRequest(BaseModel):
    """What the client sends to request a new problem be generated."""

    difficulty: str  # "easy" | "medium" | "hard"


class SubmissionRequest(BaseModel):
    """What the client sends when submitting code against a problem's test cases."""

    language: str
    version: str = "*"
    code: str


class TestCaseResult(BaseModel):
    input: str
    expected_output: str
    actual_output: Optional[str]
    passed: bool
    stderr: Optional[str] = None


class SubmissionResult(BaseModel):
    problem_id: int
    all_passed: bool
    results: List[TestCaseResult]