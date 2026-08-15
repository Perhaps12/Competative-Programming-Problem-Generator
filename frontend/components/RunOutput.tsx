import type { ExecuteResult } from "@/lib/types";

interface RunOutputProps {
  result: ExecuteResult;
}

export default function RunOutput({ result }: RunOutputProps) {
  const hasError = Boolean(result.stderr && result.stderr.trim().length > 0);

  return (
    <div className="space-y-2 rounded-lg bg-zinc-900 p-4 ring-1 ring-zinc-800">
      <div className="text-xs font-medium uppercase tracking-wide text-zinc-500">
        Output
      </div>
      <pre className="overflow-x-auto whitespace-pre-wrap font-mono text-sm text-zinc-200">
        {result.stdout || "(no output)"}
      </pre>

      {hasError && (
        <>
          <div className="mt-3 text-xs font-medium uppercase tracking-wide text-rose-500">
            stderr
          </div>
          <pre className="overflow-x-auto whitespace-pre-wrap font-mono text-sm text-rose-400">
            {result.stderr}
          </pre>
        </>
      )}
    </div>
  );
}