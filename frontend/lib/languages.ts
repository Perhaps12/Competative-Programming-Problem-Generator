// Central list of languages available in the editor. Keep this in sync
// with whatever's actually installed on your Piston instance
// (check with: curl http://127.0.0.1:2000/api/v2/runtimes).
//
// Note: C++ was removed. This Piston instance's "gcc" package only
// compiles as plain C (confirmed by testing -- it reports back
// "language": "c" regardless of filename/extension sent), and no separate
// C++ package is available in the configured package repository.

export interface LanguageOption {
  id: string; // internal id, used as the <select> value
  label: string; // shown in the dropdown
  monacoLanguage: string; // syntax highlighting id for the editor
  pistonLanguage: string; // exact "language" value Piston expects
  pistonVersion: string; // exact "version" value Piston expects
  starterCode: string;
}

export const LANGUAGE_OPTIONS: LanguageOption[] = [
  {
    id: "python",
    label: "Python",
    monacoLanguage: "python",
    pistonLanguage: "python",
    pistonVersion: "3.10.0",
    starterCode: "# Read input, solve, print the result\n",
  },
  {
    id: "java",
    label: "Java",
    monacoLanguage: "java",
    pistonLanguage: "java",
    pistonVersion: "15.0.2",
    starterCode:
      "import java.util.Scanner;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        // Read input, solve, print the result\n    }\n}\n",
  },
];

export function getLanguageOption(id: string): LanguageOption {
  const found = LANGUAGE_OPTIONS.find((l) => l.id === id);
  return found ?? LANGUAGE_OPTIONS[0];
}