"use client";

interface SubmitButtonProps {
  onClick: () => void;
  isSubmitting?: boolean;
  disabled?: boolean;
}

export default function SubmitButton({
  onClick,
  isSubmitting = false,
  disabled = false,
}: SubmitButtonProps) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled || isSubmitting}
      className="rounded-lg bg-indigo-500 px-5 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-indigo-400 disabled:cursor-not-allowed disabled:bg-zinc-700 disabled:text-zinc-400"
    >
      {isSubmitting ? "Running…" : "Submit"}
    </button>
  );
}