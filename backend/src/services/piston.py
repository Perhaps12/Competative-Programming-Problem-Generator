"""
Standalone service for executing code via Piston.

Framework-agnostic on purpose: no FastAPI imports here, no HTTPException.
This is called from execute_routes.py (for user-submitted code), and also
directly from the problem-generation flow (to run the AI-generated solution
against AI-generated inputs and record the real output).
"""

import os
from typing import Optional

import httpx

PISTON_URL = os.environ.get("PISTON_URL", "http://localhost:2000")


class PistonError(Exception):
    """Raised when Piston can't be reached, or rejects/fails a request."""

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


async def execute_code(
    language: str, code: str, stdin: str = "", version: str = "*"
) -> dict:
    """
    Run code against Piston and return a simplified result dict:
    {"stdout": str, "stderr": str, "exit_code": int, "output": str}

    Raises PistonError if Piston is unreachable or rejects the request.
    """
    payload = {
        "language": language,
        "version": version,
        "files": [{"content": code}],
        "stdin": stdin or "",
    }

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                f"{PISTON_URL}/api/v2/execute", json=payload, timeout=30
            )
        except httpx.HTTPError as e:
            raise PistonError(502, f"Could not reach Piston: {e}")

    if resp.status_code >= 400:
        raise PistonError(resp.status_code, resp.text)

    data = resp.json()
    run = data.get("run", {})

    return {
        "stdout": run.get("stdout"),
        "stderr": run.get("stderr"),
        "exit_code": run.get("code"),
        "output": run.get("output"),
    }