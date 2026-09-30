import { describe, expect, test } from "bun:test";

import { formatMoney, formatPeriod } from "./format";

describe("formatMoney", () => {
  test("keeps the API decimal string and adds thousands separators", () => {
    expect(formatMoney("37850.50")).toBe("37,850.50");
    expect(formatMoney("1099.97")).toBe("1,099.97");
    expect(formatMoney("0.00")).toBe("0.00");
  });

  test("shows negatives in parentheses", () => {
    expect(formatMoney("-44480.14")).toBe("(44,480.14)");
    expect(formatMoney("-800.25")).toBe("(800.25)");
  });

  test("does not pass the amount through a binary float", () => {
    expect(formatMoney("0.10")).toBe("0.10");
    expect(formatMoney("0.30")).not.toBe("0.29999999999999998");
  });
});

describe("formatPeriod", () => {
  test("joins the inclusive dates", () => {
    expect(formatPeriod("2026-01-01", "2026-03-31")).toBe(
      "2026-01-01 to 2026-03-31",
    );
  });
});
