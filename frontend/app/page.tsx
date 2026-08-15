"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import DifficultySelector from "@/components/DifficultySelector";
import ProblemCard from "@/components/ProblemCard";
import { createProblem, listProblems } from "@/lib/api";
import type { Problem } from "@/lib/types";

export default function HomePage() {
  const router = useRouter();

  const [problems, setProblems] = useState<Problem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listProblems()
      .then(setProblems)
      .catch((err) => setError(err.message))
      .finally(() => setIsLoading(false));
  }, []);

  async function handleGenerate(difficulty: "easy" | "medium" | "hard") {
    setIsGenerating(true);
    setError(null);
    try {
      const problem = await createProblem(difficulty);
      // New problems can take a while to generate (multiple AI calls +
      // Piston runs server-side), so jump straight to the finished result
      // rather than making the person find it in the list.
      router.push(`/problems/${problem.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate problem.");
      setIsGenerating(false);
    }
  }

  return (
    <main className="mx-auto max-w-3xl px-6 py-12">
      <header className="mb-8">
        <h1 className="text-2xl font-semibold text-zinc-100">Problems</h1>
        <p className="mt-1 text-sm text-zinc-400">
          Pick a difficulty and generate a new AI-written problem, or jump
          back into one you've already saved.
        </p>
      </header>

      <div className="mb-10">
        <DifficultySelector onGenerate={handleGenerate} isGenerating={isGenerating} />
        {isGenerating && (
          <p className="mt-3 text-sm text-zinc-500">
            This can take up to a minute — writing the problem, a reference
            solution, and generating test cases.
          </p>
        )}
      </div>

      {error && (
        <div className="mb-6 rounded-lg bg-rose-500/10 px-4 py-3 text-sm text-rose-400">
          {error}
        </div>
      )}

      {isLoading ? (
        <p className="text-sm text-zinc-500">Loading problems…</p>
      ) : problems.length === 0 ? (
        <p className="text-sm text-zinc-500">
          No problems yet — generate your first one above.
        </p>
      ) : (
        <div className="grid gap-3 sm:grid-cols-2">
          {problems.map((p) => (
            <ProblemCard key={p.id} problem={p} />
          ))}
        </div>
      )}
    </main>
  );
}