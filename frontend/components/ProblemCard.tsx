import Link from "next/link";
import type { Problem } from "@/lib/types";

const DIFFICULTY_STYLES: Record<Problem["difficulty"], string> = {
  easy: "bg-emerald-500/15 text-emerald-400",
  medium: "bg-amber-500/15 text-amber-400",
  hard: "bg-rose-500/15 text-rose-400",
};

interface ProblemCardProps {
  problem: Problem;
}

export default function ProblemCard({ problem }: ProblemCardProps) {
  // Pull the first line of the statement as a short preview, stripping
  // markdown heading/emphasis characters for a cleaner snippet.
  const preview = problem.statement
    .split("\n")
    .find((line) => line.trim().length > 0)
    ?.replace(/[#*_`]/g, "")
    .slice(0, 120);

  return (
    <Link
      href={`/problems/${problem.id}`}
      className="group block rounded-xl bg-zinc-900 p-5 ring-1 ring-zinc-800 transition-colors hover:ring-indigo-500/50"
    >
      <div className="flex items-start justify-between gap-3">
        <h3 className="font-medium text-zinc-100 group-hover:text-white">
          {problem.title}
        </h3>
        <span
          className={`shrink-0 rounded-full px-2.5 py-0.5 text-xs font-medium capitalize ${
            DIFFICULTY_STYLES[problem.difficulty]
          }`}
        >
          {problem.difficulty}
        </span>
      </div>

      {preview && (
        <p className="mt-2 line-clamp-2 text-sm text-zinc-400">{preview}</p>
      )}

      <div className="mt-4 flex items-center gap-1 font-mono text-xs text-zinc-500">
        <span>{problem.test_cases.length} test cases</span>
      </div>
    </Link>
  );
}