// Typed wrappers around calls to the FastAPI backend.
// Mirrors backend/src/routes/problems_routes.py.

import type {
  ExecuteResult,
  Problem,
  ProblemCreateRequest,
  SolutionResponse,
  SubmissionRequest,
  SubmissionResult,
} from "./types";

// Set NEXT_PUBLIC_API_URL in a .env.local file if your backend isn't on
// the default localhost:8000 (e.g. when deployed later).
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const text = await res.text().catch(() => res.statusText);
    throw new Error(`API error ${res.status}: ${text}`);
  }
  return res.json() as Promise<T>;
}

/**
 * Trigger the full AI generation pipeline (problem -> solution -> test
 * cases) and save the result. Can take a while (several seconds+), since
 * it chains multiple AI calls and Piston executions server-side.
 */
export async function createProblem(
  difficulty: ProblemCreateRequest["difficulty"]
): Promise<Problem> {
  const res = await fetch(`${API_URL}/problems/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ difficulty }),
  });
  return handleResponse<Problem>(res);
}

/** Fetch every saved problem. */
export async function listProblems(): Promise<Problem[]> {
  const res = await fetch(`${API_URL}/problems/`);
  return handleResponse<Problem[]>(res);
}

/** Fetch a single saved problem, including its test cases. */
export async function getProblem(problemId: number): Promise<Problem> {
  const res = await fetch(`${API_URL}/problems/${problemId}`);
  return handleResponse<Problem>(res);
}

/**
 * Fetch just a problem's reference solution, on demand. Kept separate from
 * getProblem() so the solution isn't loaded until someone actually asks to
 * see it (e.g. clicking a "reveal solution" dropdown).
 */
export async function getSolution(problemId: number): Promise<SolutionResponse> {
  const res = await fetch(`${API_URL}/problems/${problemId}/solution`);
  return handleResponse<SolutionResponse>(res);
}

/**
 * Submit code against a problem's saved test cases. Runs the code once per
 * test case via Piston server-side and returns pass/fail for each.
 */
export async function submitSolution(
  problemId: number,
  submission: SubmissionRequest
): Promise<SubmissionResult> {
  const res = await fetch(`${API_URL}/problems/${problemId}/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(submission),
  });
  return handleResponse<SubmissionResult>(res);
}

/**
 * Run code directly, without checking it against any problem's test cases.
 * Wraps the standalone /execute route -- useful for a "Run" button that
 * just shows raw output, separate from "Submit" which grades against a
 * problem's saved test cases.
 */
export async function runCode(
  language: string,
  code: string,
  stdin: string = "",
  version: string = "*"
): Promise<ExecuteResult> {
  const res = await fetch(`${API_URL}/execute/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ language, version, code, stdin }),
  });
  return handleResponse<ExecuteResult>(res);
}