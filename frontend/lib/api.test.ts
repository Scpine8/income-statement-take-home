import { afterEach, expect, test } from "bun:test";

import { incomeStatementUrl } from "./api";

const original = process.env.NEXT_PUBLIC_API_URL;

afterEach(() => {
  if (original === undefined) {
    delete process.env.NEXT_PUBLIC_API_URL;
  } else {
    process.env.NEXT_PUBLIC_API_URL = original;
  }
});

test("builds the income statement query", () => {
  expect(
    incomeStatementUrl("2026-01-01", "2026-03-31", "http://localhost:8000"),
  ).toBe(
    "http://localhost:8000/income-statement?start=2026-01-01&end=2026-03-31",
  );
});

test("defaults to the local API when the env var is unset", () => {
  delete process.env.NEXT_PUBLIC_API_URL;
  expect(incomeStatementUrl("2026-04-01", "2026-04-30")).toBe(
    "http://localhost:8000/income-statement?start=2026-04-01&end=2026-04-30",
  );
});

test("uses NEXT_PUBLIC_API_URL when it is set", () => {
  process.env.NEXT_PUBLIC_API_URL = "https://statements.example";
  expect(incomeStatementUrl("2026-01-01", "2026-01-31")).toBe(
    "https://statements.example/income-statement?start=2026-01-01&end=2026-01-31",
  );
});
