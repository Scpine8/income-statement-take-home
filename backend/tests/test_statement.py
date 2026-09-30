from datetime import date
from decimal import Decimal

from fastapi.testclient import TestClient

from app.ledger import load_ledger
from app.models import AccountSubtype, AccountType
from app.statement import activity_for_account, build_income_statement, format_money

LEDGER = load_ledger()
Q1_START = date(2026, 1, 1)
Q1_END = date(2026, 3, 31)


def section_map(statement):
    return {section.id: section for section in statement.sections}


def test_q1_2026_net_income_and_section_totals():
    statement = build_income_statement(LEDGER, Q1_START, Q1_END)
    sections = section_map(statement)

    assert statement.net_income == "-44480.14"
    assert sections["revenue"].total == "37850.50"
    assert sections["cogs"].total == "14272.75"
    assert sections["gross_profit"].total == "23577.75"
    assert sections["operating_expenses"].total == "68100.07"
    assert sections["operating_income"].total == "-44522.32"
    assert sections["other_income"].total == "42.18"
    assert sections["net_income"].total == "-44480.14"


def test_q1_includes_expected_accounts_and_omits_zeros():
    statement = build_income_statement(LEDGER, Q1_START, Q1_END)
    sections = section_map(statement)
    revenue_numbers = {line.number for line in sections["revenue"].lines}
    opex_numbers = {line.number for line in sections["operating_expenses"].lines}

    assert revenue_numbers == {"4000", "4100", "4900"}
    assert "6300" in opex_numbers
    assert sections["revenue"].lines[2].amount == "-800.25"


def test_void_and_draft_are_excluded():
    statement = build_income_statement(LEDGER, Q1_START, Q1_END)
    product = next(
        line
        for line in section_map(statement)["revenue"].lines
        if line.number == "4000"
    )
    salaries = next(
        line
        for line in section_map(statement)["operating_expenses"].lines
        if line.number == "6000"
    )
    assert product.amount == "35650.75"
    assert salaries.amount == "55500.00"


def test_dates_outside_range_are_excluded():
    december = build_income_statement(LEDGER, date(2025, 12, 1), date(2025, 12, 31))
    april = build_income_statement(LEDGER, date(2026, 4, 1), date(2026, 4, 30))
    assert section_map(december)["revenue"].total == "5000.00"
    assert section_map(april)["revenue"].total == "9100.00"
    q1 = build_income_statement(LEDGER, Q1_START, Q1_END)
    assert "5000.00" not in [line.amount for line in section_map(q1)["revenue"].lines]


def test_inclusive_end_date_includes_march_31_interest():
    through_30 = build_income_statement(LEDGER, Q1_START, date(2026, 3, 30))
    through_31 = build_income_statement(LEDGER, Q1_START, Q1_END)
    assert section_map(through_30)["other_income"].total == "0.00"
    assert section_map(through_31)["other_income"].total == "42.18"


def test_deferred_subscription_bill_is_not_revenue():
    statement = build_income_statement(LEDGER, Q1_START, Q1_END)
    subscription = next(
        line
        for line in section_map(statement)["revenue"].lines
        if line.number == "4100"
    )
    assert subscription.amount == "3000.00"


def test_software_vendor_credit_reduces_expense():
    statement = build_income_statement(LEDGER, Q1_START, Q1_END)
    software = next(
        line
        for line in section_map(statement)["operating_expenses"].lines
        if line.number == "6200"
    )
    assert software.amount == "1099.97"


def test_format_money_quantizes_decimal_not_float():
    assert format_money(Decimal("1.1") + Decimal("2.2")) == "3.30"
    assert isinstance(format_money(Decimal("1.00")), str)


def test_activity_signs():
    revenue = next(a for a in LEDGER.accounts if a.number == "4000")
    expense = next(a for a in LEDGER.accounts if a.number == "5000")
    cash = next(a for a in LEDGER.accounts if a.number == "1000")
    assert revenue.type == AccountType.revenue
    assert expense.subtype == AccountSubtype.cogs
    assert activity_for_account(revenue, Decimal("0"), Decimal("10.00")) == Decimal("10.00")
    assert activity_for_account(expense, Decimal("10.00"), Decimal("0")) == Decimal("10.00")
    assert activity_for_account(cash, Decimal("10.00"), Decimal("0")) is None


def test_http_rejects_inverted_range():
    from app.main import app

    client = TestClient(app)
    response = client.get("/income-statement", params={"start": "2026-03-31", "end": "2026-01-01"})
    assert response.status_code == 400
