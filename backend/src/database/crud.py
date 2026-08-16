"""
All internal database commands live here. Routes should call these functions
instead of touching SQLAlchemy sessions/queries directly.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from src.database import models


def create_problem(
    db: Session,
    title: str,
    difficulty: str,
    statement: str,
    solution_code: str,
    test_cases: List[dict],  # each dict: {"input": str, "output": str}
) -> models.Problem:
    db_problem = models.Problem(
        title=title,
        difficulty=difficulty,
        statement=statement,
        solution_code=solution_code,
    )
    db_problem.test_cases = [
        models.TestCase(input=tc["input"], output=tc["output"]) for tc in test_cases
    ]

    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem


def get_problem(db: Session, problem_id: int) -> Optional[models.Problem]:
    return db.query(models.Problem).filter(models.Problem.id == problem_id).first()


def list_problems(db: Session) -> List[models.Problem]:
    return db.query(models.Problem).order_by(models.Problem.created_at.desc()).all()


def get_all_titles(db: Session) -> List[str]:
    """
    Return every existing problem title. Used to feed into the problem
    generation prompt so the AI avoids repeating the same concepts.
    """
    rows = db.query(models.Problem.title).all()
    return [row[0] for row in rows]


def delete_problem(db: Session, problem_id: int) -> bool:
    db_problem = get_problem(db, problem_id)
    if not db_problem:
        return False
    db.delete(db_problem)
    db.commit()
    return True


def get_test_cases_for_problem(db: Session, problem_id: int) -> List[models.TestCase]:
    return (
        db.query(models.TestCase)
        .filter(models.TestCase.problem_id == problem_id)
        .all()
    )


def add_test_case(db: Session, problem_id: int, input: str, output: str) -> models.TestCase:
    """Insert a single test case linked to an already-saved problem."""
    db_test_case = models.TestCase(problem_id=problem_id, input=input, output=output)
    db.add(db_test_case)
    db.commit()
    db.refresh(db_test_case)
    return db_test_case


def get_solution_code(db: Session, problem_id: int) -> Optional[str]:
    """
    Return just a problem's solution code, without loading the rest of the
    problem or its test cases. Used by the on-demand "reveal solution"
    endpoint, kept separate from get_problem() so the solution isn't
    fetched as part of the normal page load.
    """
    result = (
        db.query(models.Problem.solution_code)
        .filter(models.Problem.id == problem_id)
        .first()
    )
    return result[0] if result else None