import { expect, test } from "bun:test";

import type { IncomeStatement } from "./types";
import { fetchErrorMessage, hasAccountActivity, rangeError } from "./view";

const emptyStatement: IncomeStatement = {
  company: "Northwind Coffee Roasters",
  currency: "USD",
  start: "2024-01-01",
  end: "2024-01-31",
  net_income: "0.00",
  sections: [
    {
      id: "revenue",
      title: "Revenue",
      kind: "accounts",
      lines: [],
      total: "0.00",
    },
    {
      id: "net_income",
      title: "Net income",
      kind: "result",
      lines: [],
      total: "0.00",
    },
  ],
};

test("rejects an inverted date range", () => {
  expect(rangeError("2026-03-31", "2026-01-01")).toBe(
    "Start date must be on or before end date.",
  );
  expect(rangeError("2026-01-01", "2026-01-01")).toBeNull();
  expect(rangeError("2026-01-01", "2026-03-31")).toBeNull();
});

test("explains a down API separately from other failures", () => {
  expect(fetchErrorMessage(new TypeError("Failed to fetch"))).toBe(
    "Cannot reach the API. Is the backend running on port 8000?",
  );
  expect(fetchErrorMessage(new Error("start must be on or before end"))).toBe(
    "start must be on or before end",
  );
  expect(fetchErrorMessage("nope")).toBe("Something went wrong.");
});

test("treats a statement with only result rows as empty activity", () => {
  expect(hasAccountActivity(emptyStatement)).toBe(false);
  expect(
    hasAccountActivity({
      ...emptyStatement,
      sections: [
        {
          ...emptyStatement.sections[0],
          lines: [
            { number: "4000", name: "Product Revenue", amount: "9100.00" },
          ],
        },
      ],
    }),
  ).toBe(true);
});
