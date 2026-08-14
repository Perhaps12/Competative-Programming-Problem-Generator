"""
Agent responsible for generating the problem statement itself
(title + description), given a difficulty level.

Deliberately does NOT generate the solution or test cases -- those are
handled by solution.py and testcase.py so each agent has one job and can
be prompt-tuned independently.
"""

import json
import os

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ["API_KEY"])

MODEL_NAME = "gemini-3.5-flash-lite"

# JSON schema the model must follow. Using response_schema (rather than just
# asking nicely in the prompt) is what makes this reliably parseable.
PROBLEM_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "statement": {
            "type": "string",
            "description": "Full problem statement in markdown, including examples and constraints.",
        },
    },
    "required": ["title", "statement"],
}


def generate_problem(difficulty: str) -> dict:
    """
    Generate a problem title + statement for the given difficulty.

    Returns: {"title": str, "statement": str}
    """
    prompt = f"""
    You are generating a LeetCode-style coding problem at "{difficulty}" difficulty.

    Write an original problem (do not copy a well-known existing LeetCode problem
    verbatim). Include:
    - A clear title
    - A markdown-formatted statement with a description, 1-2 examples (input/output),
      and any constraints (e.g. array size, value ranges).

    Do not include a solution or test cases -- only the problem itself.
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=PROBLEM_SCHEMA,
        ),
    )
    return json.loads(response.text)


if __name__ == "__main__":
    # Quick manual test: python -m src.agents.problem
    import time
 
    start = time.time()
    result = generate_problem("easy")
    elapsed = time.time() - start
 
    print(f"Title: {result['title']}\n")
    print(result["statement"])
    print(f"\n[generate_problem took {elapsed:.2f}s]")