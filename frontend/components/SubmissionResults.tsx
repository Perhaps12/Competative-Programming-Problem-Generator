"use client";

import { useState } from "react";
import { CheckCircle2, XCircle, ChevronDown } from "lucide-react";
import type { SubmissionResult } from "@/lib/types";

interface SubmissionResultsProps {
  result: SubmissionResult;
}

export default function SubmissionResults({ result }: SubmissionResultsProps) {
  const passedCount = result.results.filter((r) => r.passed).length;

  return (
    <div className="space-y-3">
      <div
        className={`flex items-center gap-2 rounded-lg px-4 py-3 text-sm font-medium ${
          result.all_passed
            ? "bg-emerald-500/10 text-emerald-400"
            : "bg-rose-500/10 text-rose-400"
        }`}
      >
        {result.all_passed ? (
          <CheckCircle2 size={18} />
        ) : (
          <XCircle size={18} />
        )}
        {passedCount} / {result.results.length} test cases passed
      </div>

      <div className="space-y-2">
        {result.results.map((r, i) => (
          <TestCaseRow key={i} index={i + 1} result={r} />
        ))}
      </div>
    </div>
  );
}

function TestCaseRow({
  index,
  result,
}: {
  index: number;
  result: SubmissionResult["results"][number];
}) {
  const [open, setOpen] = useState(false);

  return (
    <div className="rounded-lg bg-zinc-900 ring-1 ring-zinc-800">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        className="flex w-full items-center justify-between px-4 py-2.5 text-left"
      >
        <div className="flex items-center gap-2 text-sm">
          {result.passed ? (
            <CheckCircle2 size={16} className="shrink-0 text-emerald-400" />
          ) : (
            <XCircle size={16} className="shrink-0 text-rose-400" />
          )}
          <span className="text-zinc-300">Test case {index}</span>
        </div>
        <ChevronDown
          size={16}
          className={`text-zinc-500 transition-transform ${
            open ? "rotate-180" : ""
          }`}
        />
      </button>

      {open && (
        <div className="space-y-2 border-t border-zinc-800 px-4 py-3 font-mono text-xs">
          <Field label="Input" value={result.input} />
          <Field label="Expected" value={result.expected_output} />
          <Field
            label="Actual"
            value={result.actual_output ?? "(no output)"}
            highlight={!result.passed}
          />
          {result.stderr && (
            <Field label="stderr" value={result.stderr} highlight />
          )}
        </div>
      )}
    </div>
  );
}

function Field({
  label,
  value,
  highlight = false,
}: {
  label: string;
  value: string;
  highlight?: boolean;
}) {
  return (
    <div>
      <div className="mb-1 text-zinc-500">{label}</div>
      <pre
        className={`overflow-x-auto whitespace-pre-wrap rounded bg-zinc-950 p-2 ${
          highlight ? "text-rose-400" : "text-zinc-300"
        }`}
      >
        {value}
      </pre>
    </div>
  );
}