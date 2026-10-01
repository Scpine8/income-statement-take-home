# Notes

## Q1 2026 net income

For **2026-01-01 through 2026-03-31**, the app shows **net income of -44,480.14 USD**.

| Section | Amount |
| --- | --- |
| Revenue | 37,850.50 |
| Cost of goods sold | 14,272.75 |
| Gross profit | 23,577.75 |
| Operating expenses | 68,100.07 |
| Operating income | -44,522.32 |
| Other income | 42.18 |
| Net income | -44,480.14 |

## Decisions

Only `posted` journal entries in the inclusive date range are included. `draft` and `void` stay out of the books, so the duplicate February sale (JE-009), the unsigned check (JE-025), and the pending bonus (JE-019) do not affect the statement.

Amounts are `Decimal` values, serialized as cent strings. Revenue activity is credit minus debit, so Sales Returns & Discounts reduces revenue. Expense activity is debit minus credit, so the software vendor credit reduces Software. Balance-sheet accounts are ignored. Gross profit is revenue minus cost of goods sold. Operating income is gross profit minus operating expenses. Net income adds other income.

Entries are reported as recorded. The January 1 rent payment stays entirely in January even though the memo says it covers January through March. The $12,000 Acme Cafes bill stays in deferred revenue; only the three $1,000 recognition entries are subscription revenue. Marketing (6300) is inactive, and the posted Coffee Expo charge is still included. Accounts with zero activity in the range are omitted; section totals are still shown.

## How the numbers were checked

Q1 was totaled by hand from the posted P&L lines, then locked in `backend/tests/test_statement.py`. Those tests also cover the void duplicate, the draft bonus, December and April activity outside the range, the inclusive March 31 end date, deferred revenue, the vendor credit, and the sign of revenue versus expense. `make test` is the check.

## AI

Cursor drafted the API, the page, and the first tests. The Q1 total was recomputed from the ledger before it was trusted. Two places the draft was not trusted: it is easy to book the $12,000 subscription invoice as revenue, and easy to include the void February sale and the draft bonus. Both are excluded, and the tests fail if either comes back. Separately, `align-items: end` made the Next dev server warn; the stylesheet uses `flex-end`.

## With more time

A trial balance that ties every entry (debits equal credits) before the statement is built, and a second statement view that can show zero-balance accounts when an accountant wants the full chart.
