import type { IncomeStatement } from "./types";

export function rangeError(start: string, end: string): string | null {
  if (start > end) {
    return "Start date must be on or before end date.";
  }
  return null;
}

export function fetchErrorMessage(cause: unknown): string {
  if (cause instanceof Error && cause.message === "Failed to fetch") {
    return "Cannot reach the API. Is the backend running on port 8000?";
  }
  if (cause instanceof Error) {
    return cause.message;
  }
  return "Something went wrong.";
}

export function hasAccountActivity(statement: IncomeStatement): boolean {
  return statement.sections.some(
    (section) => section.kind === "accounts" && section.lines.length > 0,
  );
}
