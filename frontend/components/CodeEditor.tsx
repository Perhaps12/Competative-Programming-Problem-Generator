"use client";

import Editor from "@monaco-editor/react";

interface CodeEditorProps {
  language: string;
  value: string;
  onChange: (value: string) => void;
  height?: string;
}

export default function CodeEditor({
  language,
  value,
  onChange,
  height = "420px",
}: CodeEditorProps) {
  return (
    <div className="overflow-hidden rounded-lg ring-1 ring-zinc-800">
      <Editor
        height={height}
        language={language}
        value={value}
        theme="vs-dark"
        onChange={(val) => onChange(val ?? "")}
        options={{
          minimap: { enabled: false },
          fontSize: 14,
          fontFamily: "JetBrains Mono, ui-monospace, monospace",
          padding: { top: 16 },
          scrollBeyondLastLine: false,
          automaticLayout: true,
        }}
      />
    </div>
  );
}