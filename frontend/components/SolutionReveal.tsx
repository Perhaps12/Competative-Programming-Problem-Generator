"use client";

import { useState } from "react";
import { ChevronDown, Eye } from "lucide-react";
import { getSolution } from "@/lib/api";

interface SolutionRevealProps {
  problemId: number;
}

export default function SolutionReveal({ problemId }: SolutionRevealProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [solutionCode, setSolutionCode] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleToggle() {
    const opening = !isOpen;
    setIsOpen(opening);

    // Fetch only the first time it's opened -- not on every toggle.
    if (opening && solutionCode === null && !isLoading) {
      setIsLoading(true);
      setError(null);
      try {
        const res = await getSolution(problemId);
        setSolutionCode(res.solution_code);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load solution.");
      } finally {
        setIsLoading(false);
      }
    }
  }

  return (
    <div className="mt-6 rounded-lg ring-1 ring-zinc-800">
      <button
        type="button"
        onClick={handleToggle}
        className="flex w-full items-center justify-between rounded-lg bg-zinc-900 px-4 py-3 text-left"
      >
        <span className="flex items-center gap-2 text-sm font-medium text-zinc-300">
          <Eye size={15} />
          Reveal AI-generated solution
        </span>
        <ChevronDown
          size={16}
          className={`text-zinc-500 transition-transform ${
            isOpen ? "rotate-180" : ""
          }`}
        />
      </button>

      {isOpen && (
        <div className="border-t border-zinc-800 p-4">
          {isLoading && (
            <p className="text-sm text-zinc-500">Loading solution…</p>
          )}
          {error && <p className="text-sm text-rose-400">{error}</p>}
          {solutionCode && (
            <pre className="overflow-x-auto whitespace-pre rounded-lg bg-zinc-950 p-4 font-mono text-[13px] leading-relaxed text-zinc-200 ring-1 ring-zinc-800">
              {solutionCode}
            </pre>
          )}
        </div>
      )}
    </div>
  );
}