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
            "description": "Full problem statement in markdown, written in a "
            "DMOJ/competitive-programming style: separate Description, Input, "
            "Output, and Constraints sections. All input/output must be "
            "described purely in terms of stdin/stdout -- no function "
            "signatures or implied parameters. Do NOT include worked "
            "examples with invented numbers -- verified examples are "
            "appended separately after generation.",
        },
    },
    "required": ["title", "statement"],
}


def generate_problem(difficulty: str, existing_titles: list[str] | None = None) -> dict:
    """
    Generate a problem title + statement for the given difficulty.

    existing_titles: titles of problems already in the database. Passed in
    (rather than queried here) to keep this agent decoupled from the
    database -- the caller (the route) is responsible for fetching them via
    crud.get_all_titles() and passing them in.

    Returns: {"title": str, "statement": str}
    """
    avoid_section = ""
    if existing_titles:
        titles_list = "\n".join(f"- {t}" for t in existing_titles)
        avoid_section = f"""
    The following problems already exist. Do NOT generate a problem that is
    the same or a close variant of any of these (e.g. don't just rename
    "Two Sum" to "Pair Sum" -- pick a genuinely different concept/pattern):
    {titles_list}
    """

    prompt = f"""
    You are generating an original competitive-programming-style problem at
    "{difficulty}" difficulty, in the style of DMOJ / Codeforces / AtCoder --
    NOT in the style of LeetCode.

    This is critical: submitted solutions are standalone programs that read
    from stdin and write to stdout. There is NO function signature and NO
    assumption that variables (arrays, numbers, strings, etc.) are simply
    "given" as parameters. Every single piece of input the program needs
    must be explicitly described as something read from stdin, in a
    precisely specified format.

    The statement (markdown) MUST include, as separate clearly-labeled
    sections, and displayed appropriately as a header with "## Description", "## Input", "## Output", and "## Constraints".:

    1. **Description** -- what the program needs to compute.

    2. **Input** -- an exact, line-by-line specification of stdin. For
       example: "The first line contains a single integer n (1 <= n <=
       1000), the number of elements. The second line contains n
       space-separated integers a_1, ..., a_n." Do not leave any input
       format ambiguous or implicit.

    3. **Output** -- an exact specification of what the program must print
       to stdout, and in what format (e.g. "Print a single integer on one
       line" or "Print the result array as space-separated integers on one
       line").

    4. **Constraints** -- bounds on all inputs (sizes, value ranges).

    5. **Examples** section will be appended automatically, do not write one.

    Formatting rule: do NOT use LaTeX or math notation (no $...$, no \\(...\\),
    no \\frac, \\le, \\times, etc.). This statement is rendered as plain
    markdown only, with no math-rendering support. Write all math in plain
    text instead -- e.g. "n^2" instead of LaTeX superscript, "<=" instead of
    "\\le", "a * b" instead of "\\times", "the sum of squares from 1 to n"
    written out in words where a formula would otherwise be needed.

    Do NOT include an "Examples" section with invented sample input/output.
    Do not compute or state any concrete example values yourself -- you are
    not able to reliably execute code, so any numbers you invent may be
    wrong. Verified examples (matching an actual working solution) will be
    appended to this statement separately, after generation.

    Do not include a solution or test cases -- only the problem itself.
    {avoid_section}
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