import os

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.database import crud
from src import schemas
from src.agents.problem import generate_problem
from src.agents.solution import generate_solution
from src.agents.testcase import generate_testcase_inputs
from src.services.piston import execute_code, PistonError

router = APIRouter()

PISTON_URL = os.environ.get("PISTON_URL", "http://localhost:2000")

# Default language/version the generated solution is executed with.
# Matches what the solution agent is prompted to write (see solution.py).
DEFAULT_LANGUAGE = "python"
DEFAULT_VERSION = "3.10.0"


# ---------------------------------------------------------------------------
# CREATE — generate a new problem end-to-end
# ---------------------------------------------------------------------------
@router.post("/", response_model=schemas.ProblemOut)
async def create_problem(req: schemas.ProblemCreateRequest, db: Session = Depends(get_db)):
    """
    Full problem-generation pipeline:

    1. problem.py generates the problem statement + title
    2. solution.py generates a reference solution for it
    3. The problem is saved to the database
    4. testcase.py generates 7 test case inputs
    5. Each input is run against the reference solution via Piston to get
       the OBJECTIVE expected output (not model-guessed)
    6. Each {input, output} pair is saved to the database, linked to the
       problem's id
    """
    import time
    t0 = time.time()

    # --- 1. Generate the problem ---
    problem_data = generate_problem(req.difficulty)
    print(f"[create_problem] generate_problem: {time.time() - t0:.2f}s")

    # --- 2. Generate the reference solution ---
    t1 = time.time()
    solution_data = generate_solution(
        problem_data["statement"], language=DEFAULT_LANGUAGE
    )
    print(f"[create_problem] generate_solution: {time.time() - t1:.2f}s")

    # --- 3. Save the problem to the database (no test cases yet) ---
    t2 = time.time()
    db_problem = crud.create_problem(
        db=db,
        title=problem_data["title"],
        difficulty=req.difficulty,
        statement=problem_data["statement"],
        solution_code=solution_data["solution_code"],
        test_cases=[],  # filled in below, once we have objective outputs
    )
    print(f"[create_problem] save problem to db: {time.time() - t2:.2f}s")

    # --- 4. Generate test case inputs ---
    t3 = time.time()
    testcase_data = generate_testcase_inputs(
        problem_data["statement"], solution_data["solution_code"]
    )
    print(f"[create_problem] generate_testcase_inputs: {time.time() - t3:.2f}s")

    # --- 5 & 6. Run each input through Piston, save the real output ---
    t4 = time.time()
    for i, test_input in enumerate(testcase_data["inputs"], start=1):
        t_case = time.time()
        try:
            result = await execute_code(
                language=DEFAULT_LANGUAGE,
                version=DEFAULT_VERSION,
                code=solution_data["solution_code"],
                stdin=test_input,
            )
        except PistonError as e:
            print(f"[create_problem] test case {i} FAILED after {time.time() - t_case:.2f}s: {e}")
            continue

        print(f"[create_problem] test case {i} piston call: {time.time() - t_case:.2f}s")

        if result["stderr"]:
            print(f"[create_problem] test case {i} skipped (stderr): {result['stderr']}")
            continue

        crud.add_test_case(
            db=db,
            problem_id=db_problem.id,
            input=test_input,
            output=(result["stdout"] or "").strip(),
        )
    print(f"[create_problem] full piston loop: {time.time() - t4:.2f}s")

    db.refresh(db_problem)
    print(f"[create_problem] TOTAL: {time.time() - t0:.2f}s")
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
    for tc in test_cases:
        try:
            result = await execute_code(
                language=submission.language,
                version=submission.version,
                code=submission.code,
                stdin=tc.input,
            )
        except PistonError as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

        actual_output = (result["stdout"] or "").strip()
        expected_output = tc.output.strip()

        results.append(
            schemas.TestCaseResult(
                input=tc.input,
                expected_output=tc.output,
                actual_output=result["stdout"],
                passed=actual_output == expected_output,
                stderr=result["stderr"],
            )
        )

    return schemas.SubmissionResult(
        problem_id=problem_id,
        all_passed=all(r.passed for r in results),
        results=results,
    )