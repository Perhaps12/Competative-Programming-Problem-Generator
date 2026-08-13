"""
Agent responsible for generating a reference solution, given an
already-generated problem statement.

Runs AFTER problem.py's output is available -- pass the generated
statement in as input here.
"""

import json
import os

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ["API_KEY"])

MODEL_NAME = "gemini-3.5-flash-lite"

SOLUTION_SCHEMA = {
    "type": "object",
    "properties": {
        "solution_code": {
            "type": "string",
            "description": "A complete, correct, working solution to the problem, "
            "written to read input from stdin and print output to stdout.",
        },
        "language": {
            "type": "string",
            "description": "The language the solution is written in, e.g. 'python'.",
        },
    },
    "required": ["solution_code", "language"],
}


def generate_solution(problem_statement: str, language: str = "python") -> dict:
    """
    Generate a reference solution for the given problem statement.

    Returns: {"solution_code": str, "language": str}
    """
    prompt = f"""
    You are writing a correct, working reference solution in {language} for the
    following coding problem:

    ---
    {problem_statement}
    ---

    Requirements:
    - The program must read all input from stdin and print the result to stdout.
    - Do not include comments explaining the problem, just clean working code.
    - Make sure the solution actually solves the problem correctly and handles
      the edge cases implied by the constraints.
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=SOLUTION_SCHEMA,
        ),
    )
    return json.loads(response.text)


if __name__ == "__main__":
    # Quick manual test: python -m src.agents.solution
    from src.agents.problem import generate_problem

    problem = generate_problem("easy")
    print(f"Title: {problem['title']}\n")
    print(problem["statement"])

    result = generate_solution(problem["statement"])
    print(f"\n--- Solution ({result['language']}) ---\n")
    print(result["solution_code"])