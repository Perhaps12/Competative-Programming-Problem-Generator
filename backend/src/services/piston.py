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

# Piston determines the compiler from the file extension. Java requires
# the filename to match the public class name (Main.java <-> "public class
# Main"). C/C++ removed from this project -- see lib/languages.ts on the
# frontend for why.
_DEFAULT_FILENAMES = {
    "python": "main.py",
    "java": "Main.java",
}


class PistonError(Exception):
    """Raised when Piston can't be reached, or rejects/fails a request."""

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


async def execute_code(
    language: str,
    code: str,
    stdin: str = "",
    version: str = "*",
    file_name: Optional[str] = None,
) -> dict:
    """
    Run code against Piston and return a simplified result dict:
    {"stdout": str, "stderr": str, "exit_code": int, "output": str}

    file_name: explicit filename to send to Piston. If omitted, falls back
    to _DEFAULT_FILENAMES based on `language` -- this matters most for C++
    (must end in .cpp, not .c) and Java (must match the public class name).

    Raises PistonError if Piston is unreachable or rejects the request.
    """
    resolved_name = file_name or _DEFAULT_FILENAMES.get(language, "main")

    payload = {
        "language": language,
        "version": version,
        "files": [{"name": resolved_name, "content": code}],
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


if __name__ == "__main__":
    # Quick manual test: python -m src.services.piston
    import asyncio
    import json

    result = asyncio.run(
        execute_code(
            language="python",
            version="3.10.0",
            code="print(input())",
            stdin="hello world",
        )
    )
    print(json.dumps(result, indent=2))