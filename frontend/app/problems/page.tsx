import { redirect } from "next/navigation";

// There's no dedicated "/problems" list view -- the homepage already shows
// every problem. This route exists so a bare /problems URL (e.g. someone
// editing the address bar, or a stray link) doesn't just 404.
export default function ProblemsIndexPage() {
  redirect("/");
}