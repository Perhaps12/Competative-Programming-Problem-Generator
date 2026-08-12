import os
from typing import Optional

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

PISTON_URL = os.environ.get("PISTON_URL", "http://localhost:2000")


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
async def execute_code(req: ExecuteRequest):
    """Run submitted code against Piston and return simplified results."""
    payload = {
        "language": req.language,
        "version": req.version,
        "files": [{"content": req.code}],
        "stdin": req.stdin or "",
    }

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                f"{PISTON_URL}/api/v2/execute", json=payload, timeout=30
            )
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Could not reach Piston: {e}")

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    data = resp.json()
    run = data.get("run", {})

    return ExecuteResult(
        stdout=run.get("stdout"),
        stderr=run.get("stderr"),
        exit_code=run.get("code"),
        output=run.get("output"),
    )