from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.services.piston import execute_code, PistonError

router = APIRouter()


class ExecuteRequest(BaseModel):
    language: str
    version: str = "*"  # "*" tells Piston to use whatever version is installed
    code: str
    stdin: Optional[str] = ""


class ExecuteResult(BaseModel):
    stdout: Optional[str]
    stderr: Optional[str]
    exit_code: Optional[int]
    output: Optional[str]  # combined stdout+stderr, as Piston returns it


@router.post("/", response_model=ExecuteResult)
async def execute(req: ExecuteRequest):
    """Run submitted code against Piston and return simplified results."""
    try:
        result = await execute_code(
            language=req.language,
            code=req.code,
            stdin=req.stdin,
            version=req.version,
        )
    except PistonError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    return ExecuteResult(**result)