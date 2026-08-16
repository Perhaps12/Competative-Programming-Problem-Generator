"use client";

import { useState, isValidElement } from "react";
import ReactMarkdown from "react-markdown";
import { Copy, Check } from "lucide-react";

interface ProblemStatementProps {
  statement: string;
}

export default function ProblemStatement({ statement }: ProblemStatementProps) {
  return (
    <div className="space-y-4 text-[15px] leading-relaxed text-zinc-300">
      <ReactMarkdown
        components={{
          h1: (props) => (
            <h1 className="text-xl font-semibold text-zinc-100" {...props} />
          ),
          h2: (props) => (
            <h2
              className="mt-6 text-base font-semibold text-zinc-100"
              {...props}
            />
          ),
          h3: (props) => (
            <h3
              className="mt-4 text-sm font-semibold text-zinc-200"
              {...props}
            />
          ),
          p: (props) => <p className="text-zinc-300" {...props} />,
          strong: (props) => (
            <strong className="font-semibold text-zinc-100" {...props} />
          ),
          ul: (props) => (
            <ul
              className="list-disc space-y-1 pl-5 text-zinc-300"
              {...props}
            />
          ),
          ol: (props) => (
            <ol
              className="list-decimal space-y-1 pl-5 text-zinc-300"
              {...props}
            />
          ),
          code: (props) => (
            <code
              className="font-mono text-[13px] text-indigo-300 [&:not(pre_*)]:rounded [&:not(pre_*)]:bg-zinc-800 [&:not(pre_*)]:px-1.5 [&:not(pre_*)]:py-0.5"
              {...props}
            />
          ),
          pre: (props) => <CodeBlock {...props} />,
        }}
      >
        {statement}
      </ReactMarkdown>
    </div>
  );
}

// A <pre> wrapper with a copy-to-clipboard button. Pulled out as its own
// component (rather than an inline function in `components` above) because
// it needs its own `copied` state per code block.
function CodeBlock(props: React.ComponentProps<"pre">) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    const text = extractText(props.children);
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      // Clipboard access can fail (e.g. non-HTTPS context, permissions) --
      // fail silently rather than showing a broken "copied" state.
    }
  }

  return (
    <div className="group relative">
      <pre
        className="overflow-x-auto whitespace-pre rounded-lg bg-zinc-900 p-4 font-mono text-[13px] leading-relaxed text-zinc-200 ring-1 ring-zinc-800"
        {...props}
      />
      <button
        type="button"
        onClick={handleCopy}
        aria-label="Copy code"
        className="absolute right-2 top-2 rounded-md bg-zinc-800 p-1.5 text-zinc-400 opacity-0 transition-opacity hover:text-zinc-200 group-hover:opacity-100"
      >
        {copied ? (
          <Check size={14} className="text-emerald-400" />
        ) : (
          <Copy size={14} />
        )}
      </button>
    </div>
  );
}

// react-markdown passes a <code> element as children of <pre>; its own
// children is the raw text. Recursively flatten in case of nested nodes.
function extractText(node: React.ReactNode): string {
  if (typeof node === "string") return node;
  if (typeof node === "number") return String(node);
  if (Array.isArray(node)) return node.map(extractText).join("");
  if (isValidElement<{ children?: React.ReactNode }>(node)) {
    return extractText(node.props.children);
  }
  return "";
}