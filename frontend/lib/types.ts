// Mirrors backend/src/schemas.py -- keep these in sync manually when the
// backend schemas change.

export interface TestCase {
  id?: number;
  input: string;
  output: string;
}

export interface Problem {
  id: number;
  title: string;
  difficulty: "easy" | "medium" | "hard";
  statement: string; // markdown
  solution_code: string;
  created_at: string | null;
  test_cases: TestCase[];
}

export interface ProblemCreateRequest {
  difficulty: "easy" | "medium" | "hard";
}

export interface SubmissionRequest {
  language: string;
  version?: string; // defaults to "*" on the backend if omitted
  code: string;
}

export interface TestCaseResult {
  input: string;
  expected_output: string;
  actual_output: string | null;
  passed: boolean;
  stderr: string | null;
}

export interface SubmissionResult {
  problem_id: number;
  all_passed: boolean;
  results: TestCaseResult[];
}

export interface ExecuteResult {
  stdout: string | null;
  stderr: string | null;
  exit_code: number | null;
  output: string | null;
}

export interface SolutionResponse {
  solution_code: string;
}