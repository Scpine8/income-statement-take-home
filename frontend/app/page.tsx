"use client";

import {
  type FormEvent,
  Fragment,
  useCallback,
  useEffect,
  useState,
} from "react";

import { incomeStatementUrl } from "@/lib/api";
import { formatMoney, formatPeriod } from "@/lib/format";
import type { IncomeStatement } from "@/lib/types";
import { fetchErrorMessage, hasAccountActivity, rangeError } from "@/lib/view";

const DEFAULT_START = "2026-01-01";
const DEFAULT_END = "2026-03-31";

export default function Page() {
  const [start, setStart] = useState(DEFAULT_START);
  const [end, setEnd] = useState(DEFAULT_END);
  const [appliedStart, setAppliedStart] = useState(DEFAULT_START);
  const [appliedEnd, setAppliedEnd] = useState(DEFAULT_END);
  const [statement, setStatement] = useState<IncomeStatement | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async (rangeStart: string, rangeEnd: string) => {
    const invalidRange = rangeError(rangeStart, rangeEnd);
    if (invalidRange) {
      setStatement(null);
      setError(invalidRange);
      setLoading(false);
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const response = await fetch(incomeStatementUrl(rangeStart, rangeEnd));
      if (!response.ok) {
        const body = (await response.json().catch(() => null)) as {
          detail?: string;
        } | null;
        throw new Error(body?.detail ?? `Request failed (${response.status})`);
      }
      const data = (await response.json()) as IncomeStatement;
      setStatement(data);
    } catch (cause) {
      setStatement(null);
      setError(fetchErrorMessage(cause));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load(DEFAULT_START, DEFAULT_END);
  }, [load]);

  function onSubmit(event: FormEvent) {
    event.preventDefault();
    setAppliedStart(start);
    setAppliedEnd(end);
    void load(start, end);
  }

  const hasAccountLines = statement ? hasAccountActivity(statement) : false;

  return (
    <main>
      <header>
        <h1>{statement?.company ?? "Income statement"}</h1>
        <p className="meta">
          {statement
            ? `${statement.currency} · ${formatPeriod(statement.start, statement.end)}`
            : `USD · ${formatPeriod(appliedStart, appliedEnd)}`}
        </p>
      </header>

      <form onSubmit={onSubmit}>
        <label>
          Start
          <input
            type="date"
            value={start}
            onChange={(event) => setStart(event.target.value)}
            required
          />
        </label>
        <label>
          End
          <input
            type="date"
            value={end}
            onChange={(event) => setEnd(event.target.value)}
            required
          />
        </label>
        <button type="submit">Apply</button>
      </form>

      {loading ? <p className="status">Loading statement…</p> : null}
      {error ? <p className="status error">{error}</p> : null}

      {!loading && !error && statement && !hasAccountLines ? (
        <p className="status">No posted P&L activity in this period.</p>
      ) : null}

      {!loading && statement ? (
        <table>
          <thead>
            <tr>
              <th>Account</th>
              <th className="num">Amount</th>
            </tr>
          </thead>
          <tbody>
            {statement.sections.map((section) => (
              <Fragment key={section.id}>
                {section.kind === "accounts" ? (
                  <>
                    <tr className="section-title">
                      <td colSpan={2}>{section.title}</td>
                    </tr>
                    {section.lines.map((line) => (
                      <tr className="indent" key={line.number}>
                        <td>
                          {line.number} · {line.name}
                        </td>
                        <td className="num">{formatMoney(line.amount)}</td>
                      </tr>
                    ))}
                    <tr className="total">
                      <td>Total {section.title.toLowerCase()}</td>
                      <td className="num">{formatMoney(section.total)}</td>
                    </tr>
                  </>
                ) : (
                  <tr
                    className={
                      section.id === "net_income" ? "result net" : "result"
                    }
                  >
                    <td>{section.title}</td>
                    <td className="num">{formatMoney(section.total)}</td>
                  </tr>
                )}
              </Fragment>
            ))}
          </tbody>
        </table>
      ) : null}
    </main>
  );
}
