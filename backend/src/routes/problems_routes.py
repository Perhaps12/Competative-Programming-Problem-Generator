import os

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.database import crud
from src import schemas

router = APIRouter()

PISTON_URL = os.environ.get("PISTON_URL", "http://localhost:2000")


# ---------------------------------------------------------------------------
# CREATE — generate a new problem
# ---------------------------------------------------------------------------
@router.post("/", response_model=schemas.ProblemOut)
async def create_problem(req: schemas.ProblemCreateRequest, db: Session = Depends(get_db)):
    """
    Generate a new problem at the requested difficulty and save it to the DB.

    ------------------------------------------------------------------
    TODO: plug in AI model here.
    ------------------------------------------------------------------
    This is a placeholder. Replace the block below with a real call to
    whichever model you choose (e.g. Gemini 2.5 Flash via Google AI Studio).
    The call should return, at minimum:
        - title            (str)
        - statement         (str, markdown/html)
        - solution_code     (str)
        - test_cases         (list of {"input": str, "output": str})
    based on req.difficulty ("easy" | "medium" | "hard").

    Suggested approach: prompt the model to return a single JSON object
    matching this shape, so you can json.loads() it directly instead of
    parsing free-form text.
    ------------------------------------------------------------------
    """
    # --- START placeholder / stub data (delete once AI call is wired in) ---
    generated = {
        "title": f"Placeholder {req.difficulty.capitalize()} Problem",
        "statement": "This is a placeholder problem statement. Replace with AI output.",
        "solution_code": "def solution():\n    pass",
        "test_cases": [
            {"input": "1", "output": "1"},
        ],
    }
    # --- END placeholder ---

    db_problem = crud.create_problem(
        db=db,
        title=generated["title"],
        difficulty=req.difficulty,
        statement=generated["statement"],
        solution_code=generated["solution_code"],
        test_cases=generated["test_cases"],
    )
    return db_problem


# ---------------------------------------------------------------------------
# READ — fetch a saved problem
# ---------------------------------------------------------------------------
@router.get("/{problem_id}", response_model=schemas.ProblemOut)
def get_problem(problem_id: int, db: Session = Depends(get_db)):
    db_problem = crud.get_problem(db, problem_id)
    if not db_problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return db_problem


# ---------------------------------------------------------------------------
# SUBMIT — run submitted code against a problem's test cases via Piston
# ---------------------------------------------------------------------------
@router.post("/{problem_id}/submit", response_model=schemas.SubmissionResult)
async def submit_solution(
    problem_id: int, submission: schemas.SubmissionRequest, db: Session = Depends(get_db)
):
    db_problem = crud.get_problem(db, problem_id)
    if not db_problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    test_cases = crud.get_test_cases_for_problem(db, problem_id)
    if not test_cases:
        raise HTTPException(status_code=400, detail="Problem has no test cases")

    results = []
    async with httpx.AsyncClient() as client:
        for tc in test_cases:
            payload = {
                "language": submission.language,
                "version": submission.version,
                "files": [{"content": submission.code}],
                "stdin": tc.input,
            }
            try:
                resp = await client.post(
                    f"{PISTON_URL}/api/v2/execute", json=payload, timeout=30
                )
                resp.raise_for_status()
            except httpx.HTTPStatusError as e:
                raise HTTPException(
                    status_code=502, detail=f"Piston returned {e.response.status_code}: {e.response.text}"
                )
            except httpx.HTTPError as e:
                raise HTTPException(
                    status_code=502, detail=f"Could not reach Piston: {e}"
                )

            run = resp.json().get("run", {})
            actual_output = (run.get("stdout") or "").strip()
            expected_output = tc.output.strip()

            results.append(
                schemas.TestCaseResult(
                    input=tc.input,
                    expected_output=tc.output,
                    actual_output=run.get("stdout"),
                    passed=actual_output == expected_output,
                    stderr=run.get("stderr"),
                )
            )

    return schemas.SubmissionResult(
        problem_id=problem_id,
        all_passed=all(r.passed for r in results),
        results=results,
    )