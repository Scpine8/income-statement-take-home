from __future__ import annotations

from collections import defaultdict
from datetime import date
from decimal import Decimal

from app.models import (
    Account,
    AccountSubtype,
    AccountType,
    IncomeStatement,
    Ledger,
    StatementLine,
    StatementSection,
)

CENTS = Decimal("0.01")


def format_money(amount: Decimal) -> str:
    return f"{amount.quantize(CENTS)}"


def activity_for_account(
    account: Account, debit: Decimal, credit: Decimal
) -> Decimal | None:
    """Return signed P&L activity for one journal line, or None if off-statement."""
    if account.subtype == AccountSubtype.balance_sheet:
        return None
    if account.type == AccountType.revenue:
        return credit - debit
    if account.type == AccountType.expense:
        return debit - credit
    return None


def _lines_and_total(
    ledger: Ledger,
    totals: dict[str, Decimal],
    *subtypes: AccountSubtype,
) -> tuple[list[StatementLine], Decimal]:
    lines: list[StatementLine] = []
    total = Decimal("0.00")
    for account in ledger.accounts:
        if account.subtype not in subtypes:
            continue
        amount = totals.get(account.number, Decimal("0.00"))
        if amount == 0:
            continue
        lines.append(
            StatementLine(
                number=account.number, name=account.name, amount=format_money(amount)
            )
        )
        total += amount
    return lines, total


def build_income_statement(ledger: Ledger, start: date, end: date) -> IncomeStatement:
    if start > end:
        raise ValueError("start must be on or before end")

    by_number = {account.number: account for account in ledger.accounts}
    totals: dict[str, Decimal] = defaultdict(lambda: Decimal("0.00"))

    for entry in ledger.journal_entries:
        if entry.status != "posted":
            continue
        if entry.date < start or entry.date > end:
            continue
        for line in entry.lines:
            account = by_number[line.account]
            delta = activity_for_account(account, line.debit, line.credit)
            if delta is None:
                continue
            totals[account.number] += delta

    revenue_lines, revenue_total = _lines_and_total(
        ledger,
        totals,
        AccountSubtype.operating_revenue,
        AccountSubtype.contra_revenue,
    )
    cogs_lines, cogs_total = _lines_and_total(ledger, totals, AccountSubtype.cogs)
    gross_profit = revenue_total - cogs_total
    opex_lines, opex_total = _lines_and_total(
        ledger, totals, AccountSubtype.operating_expense
    )
    operating_income = gross_profit - opex_total
    other_lines, other_total = _lines_and_total(
        ledger, totals, AccountSubtype.other_income
    )
    net_income = operating_income + other_total

    sections = [
        StatementSection(
            id="revenue",
            title="Revenue",
            kind="accounts",
            lines=revenue_lines,
            total=format_money(revenue_total),
        ),
        StatementSection(
            id="cogs",
            title="Cost of goods sold",
            kind="accounts",
            lines=cogs_lines,
            total=format_money(cogs_total),
        ),
        StatementSection(
            id="gross_profit",
            title="Gross profit",
            kind="result",
            total=format_money(gross_profit),
        ),
        StatementSection(
            id="operating_expenses",
            title="Operating expenses",
            kind="accounts",
            lines=opex_lines,
            total=format_money(opex_total),
        ),
        StatementSection(
            id="operating_income",
            title="Operating income",
            kind="result",
            total=format_money(operating_income),
        ),
        StatementSection(
            id="other_income",
            title="Other income",
            kind="accounts",
            lines=other_lines,
            total=format_money(other_total),
        ),
        StatementSection(
            id="net_income",
            title="Net income",
            kind="result",
            total=format_money(net_income),
        ),
    ]

    return IncomeStatement(
        company=ledger.company,
        currency=ledger.currency,
        start=start,
        end=end,
        sections=sections,
        net_income=format_money(net_income),
    )
