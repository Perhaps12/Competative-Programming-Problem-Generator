"use client";

import { LANGUAGE_OPTIONS } from "@/lib/languages";

interface LanguageSelectorProps {
  value: string;
  onChange: (id: string) => void;
}

export default function LanguageSelector({ value, onChange }: LanguageSelectorProps) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="rounded-lg bg-zinc-900 px-3 py-2 text-sm text-zinc-200 ring-1 ring-zinc-800 focus:outline-none focus:ring-indigo-500/50"
    >
      {LANGUAGE_OPTIONS.map((lang) => (
        <option key={lang.id} value={lang.id}>
          {lang.label}
        </option>
      ))}
    </select>
  );
}