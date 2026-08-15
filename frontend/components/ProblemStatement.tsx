import ReactMarkdown from "react-markdown";

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
              className="rounded bg-zinc-800 px-1.5 py-0.5 font-mono text-[13px] text-indigo-300"
              {...props}
            />
          ),
          pre: (props) => (
            <pre
              className="overflow-x-auto rounded-lg bg-zinc-900 p-4 font-mono text-[13px] ring-1 ring-zinc-800"
              {...props}
            />
          ),
        }}
      >
        {statement}
      </ReactMarkdown>
    </div>
  );
}