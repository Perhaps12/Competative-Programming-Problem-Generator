"""
Agent responsible for generating test case INPUTS ONLY, given the problem
statement and reference solution.

Important: this agent does NOT generate expected output. Having the model
compute expected output itself is unreliable (it's just guessing/simulating
execution). Instead, expected output is determined objectively by actually
running the reference solution through Piston for each generated input --
see src/services/piston.py. That execution happens in the problem-creation
route, after this agent runs.

Standardized to always generate 7 test cases.
"""

import json
import os

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ["API_KEY"])

MODEL_NAME = "gemini-3.5-flash-lite"

NUM_TEST_CASES = 7

TESTCASE_INPUTS_SCHEMA = {
    "type": "object",
    "properties": {
        "inputs": {
            "type": "array",
            "description": f"Exactly {NUM_TEST_CASES} stdin inputs for the problem.",
            "items": {
                "type": "string",
                "description": "Exact stdin input, matching what the reference "
                "solution expects to read.",
            },
        },
    },
    "required": ["inputs"],
}


def generate_testcase_inputs(problem_statement: str, solution_code: str) -> dict:
    """
    Generate NUM_TEST_CASES (7) test case inputs for the given problem +
    reference solution. Does NOT compute expected output -- that's done
    separately by actually running the solution via Piston.

    Returns: {"inputs": [str, str, ...]}  (length == NUM_TEST_CASES)
    """
    prompt = f"""
    Given the following coding problem and its reference solution, generate
    exactly {NUM_TEST_CASES} distinct stdin inputs to test it with.

    Problem:
    ---
    {problem_statement}
    ---

    Reference solution:
    ---
    {solution_code}
    ---

    Requirements:
    - Include at least one simple/typical case.
    - Include edge cases implied by the problem's constraints (e.g. empty
      input, minimum/maximum sizes, duplicate values, negative numbers --
      whichever are relevant to this specific problem).
    - Each input must exactly match the stdin format the reference solution
      expects to read.
    - Do NOT compute or include expected output -- only generate the inputs.
    - Return exactly {NUM_TEST_CASES} inputs, no more, no fewer.
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=TESTCASE_INPUTS_SCHEMA,
        ),
    )
    return json.loads(response.text)


if __name__ == "__main__":
    # Quick manual test: python -m src.agents.testcase
    import time
    from src.agents.problem import generate_problem
    from src.agents.solution import generate_solution
 
    t0 = time.time()
    problem = generate_problem("easy")
    t1 = time.time()
 
    print(f"Title: {problem['title']}\n")
    print(problem["statement"])
    print(f"\n[generate_problem took {t1 - t0:.2f}s]")
 
    solution = generate_solution(problem["statement"])
    t2 = time.time()
 
    print(f"\n--- Solution ({solution['language']}) ---\n")
    print(solution["solution_code"])
    print(f"\n[generate_solution took {t2 - t1:.2f}s]")
 
    result = generate_testcase_inputs(problem["statement"], solution["solution_code"])
    t3 = time.time()
 
    print(f"\n--- Test case inputs ({len(result['inputs'])}) ---\n")
    for i, test_input in enumerate(result["inputs"], start=1):
        print(f"[{i}] {test_input!r}")
    print(f"\n[generate_testcase_inputs took {t3 - t2:.2f}s]")
    print(f"[total: {t3 - t0:.2f}s]")