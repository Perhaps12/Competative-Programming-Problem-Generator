"use client";

import { useState } from "react";

type Difficulty = "easy" | "medium" | "hard";

const DIFFICULTIES: {
  value: Difficulty;
  label: string;
  activeClasses: string;
}[] = [
  {
    value: "easy",
    label: "Easy",
    activeClasses: "bg-emerald-500/15 text-emerald-400 ring-emerald-500/40",
  },
  {
    value: "medium",
    label: "Medium",
    activeClasses: "bg-amber-500/15 text-amber-400 ring-amber-500/40",
  },
  {
    value: "hard",
    label: "Hard",
    activeClasses: "bg-rose-500/15 text-rose-400 ring-rose-500/40",
  },
];

interface DifficultySelectorProps {
  onGenerate: (difficulty: Difficulty) => void;
  isGenerating?: boolean;
}

export default function DifficultySelector({
  onGenerate,
  isGenerating = false,
}: DifficultySelectorProps) {
  const [selected, setSelected] = useState<Difficulty>("easy");

  return (
    <div className="flex flex-wrap items-center gap-3">
      <div className="flex gap-2 rounded-lg bg-zinc-900 p-1 ring-1 ring-zinc-800">
        {DIFFICULTIES.map((d) => (
          <button
            key={d.value}
            type="button"
            onClick={() => setSelected(d.value)}
            className={`rounded-md px-3 py-1.5 text-sm font-medium transition-colors ${
              selected === d.value
                ? `${d.activeClasses} ring-1`
                : "text-zinc-400 hover:text-zinc-200"
            }`}
          >
            {d.label}
          </button>
        ))}
      </div>

      <button
        type="button"
        onClick={() => onGenerate(selected)}
        disabled={isGenerating}
        className="rounded-lg bg-indigo-500 px-4 py-2 text-sm font-semibold text-white transition-colors hover:bg-indigo-400 disabled:cursor-not-allowed disabled:bg-zinc-700 disabled:text-zinc-400"
      >
        {isGenerating ? "Generating…" : "Generate problem"}
      </button>
    </div>
  );
}