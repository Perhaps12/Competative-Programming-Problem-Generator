"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import ProblemStatement from "@/components/ProblemStatement";
import CodeEditor from "@/components/CodeEditor";
import SubmitButton from "@/components/SubmitButton";
import SubmissionResults from "@/components/SubmissionResults";
import RunOutput from "@/components/RunOutput";
import { getProblem, submitSolution, runCode } from "@/lib/api";
import type { ExecuteResult, Problem, SubmissionResult } from "@/lib/types";

const DIFFICULTY_STYLES: Record<Problem["difficulty"], string> = {
  easy: "bg-emerald-500/15 text-emerald-400",
  medium: "bg-amber-500/15 text-amber-400",
  hard: "bg-rose-500/15 text-rose-400",
};

const DEFAULT_STARTER_CODE = "# Read input, solve, print the result\n";

export default function ProblemPage() {
  const params = useParams<{ id: string }>();
  const problemId = Number(params.id);

  const [problem, setProblem] = useState<Problem | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [code, setCode] = useState(DEFAULT_STARTER_CODE);

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitResult, setSubmitResult] = useState<SubmissionResult | null>(null);

  const [isRunning, setIsRunning] = useState(false);
  const [runResult, setRunResult] = useState<ExecuteResult | null>(null);
  const [stdin, setStdin] = useState("");

  useEffect(() => {
    if (!Number.isFinite(problemId)) return;
    getProblem(problemId)
      .then(setProblem)
      .catch((err) => setError(err.message))
      .finally(() => setIsLoading(false));
  }, [problemId]);

  async function handleRun() {
    setIsRunning(true);
    setError(null);
    setRunResult(null);
    try {
      const res = await runCode("python", code, stdin, "3.10.0");
      setRunResult(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Run failed.");
    } finally {
      setIsRunning(false);
    }
  }

  async function handleSubmit() {
    setIsSubmitting(true);
    setError(null);
    setSubmitResult(null);
    try {
      const res = await submitSolution(problemId, {
        language: "python",
        version: "3.10.0",
        code,
      });
      setSubmitResult(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Submission failed.");
    } finally {
      setIsSubmitting(false);
    }
  }

  if (isLoading) {
    return (
      <main className="mx-auto max-w-5xl px-6 py-12">
        <p className="text-sm text-zinc-500">Loading problem…</p>
      </main>
    );
  }

  if (error && !problem) {
    return (
      <main className="mx-auto max-w-5xl px-6 py-12">
        <p className="text-sm text-rose-400">{error}</p>
      </main>
    );
  }

  if (!problem) return null;

  return (
    <main className="mx-auto max-w-6xl px-6 py-8">
      <Link
        href="/"
        className="mb-6 inline-flex items-center gap-1.5 text-sm text-zinc-400 hover:text-zinc-200"
      >
        <ArrowLeft size={15} />
        All problems
      </Link>

      <div className="grid gap-8 lg:grid-cols-2">
        {/* Left: problem statement */}
        <section>
          <div className="mb-4 flex items-center gap-3">
            <h1 className="text-xl font-semibold text-zinc-100">
              {problem.title}
            </h1>
            <span
              className={`rounded-full px-2.5 py-0.5 text-xs font-medium capitalize ${
                DIFFICULTY_STYLES[problem.difficulty]
              }`}
            >
              {problem.difficulty}
            </span>
          </div>
          <ProblemStatement statement={problem.statement} />
        </section>

        {/* Right: editor + run/submit + results */}
        <section className="flex flex-col gap-4">
          <CodeEditor language="python" value={code} onChange={setCode} />

          <div>
            <label className="mb-1 block text-xs font-medium uppercase tracking-wide text-zinc-500">
              stdin (for Run only)
            </label>
            <textarea
              value={stdin}
              onChange={(e) => setStdin(e.target.value)}
              rows={2}
              placeholder="Optional input for Run"
              className="w-full rounded-lg bg-zinc-900 px-3 py-2 font-mono text-sm text-zinc-200 ring-1 ring-zinc-800 placeholder:text-zinc-600 focus:outline-none focus:ring-indigo-500/50"
            />
          </div>

          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={handleRun}
              disabled={isRunning}
              className="rounded-lg bg-zinc-800 px-4 py-2 text-sm font-semibold text-zinc-200 transition-colors hover:bg-zinc-700 disabled:cursor-not-allowed disabled:text-zinc-500"
            >
              {isRunning ? "Running…" : "Run"}
            </button>
            <SubmitButton onClick={handleSubmit} isSubmitting={isSubmitting} />
            {error && <span className="text-sm text-rose-400">{error}</span>}
          </div>

          {runResult && <RunOutput result={runResult} />}
          {submitResult && <SubmissionResults result={submitResult} />}
        </section>
      </div>
    </main>
  );
}