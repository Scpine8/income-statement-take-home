from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field


class AccountType(str, Enum):
    asset = "asset"
    liability = "liability"
    equity = "equity"
    revenue = "revenue"
    expense = "expense"


class AccountSubtype(str, Enum):
    operating_revenue = "operating_revenue"
    contra_revenue = "contra_revenue"
    cogs = "cogs"
    operating_expense = "operating_expense"
    other_income = "other_income"
    balance_sheet = "balance_sheet"


class Account(BaseModel):
    number: str
    name: str
    type: AccountType
    subtype: AccountSubtype
    is_active: bool


class JournalLine(BaseModel):
    account: str
    debit: Decimal
    credit: Decimal


class JournalEntry(BaseModel):
    id: str
    date: date
    status: str
    memo: str
    lines: list[JournalLine]


class Ledger(BaseModel):
    company: str
    currency: str
    accounts: list[Account]
    journal_entries: list[JournalEntry]


class StatementLine(BaseModel):
    number: str
    name: str
    amount: str


class StatementSection(BaseModel):
    id: str
    title: str
    kind: str
    lines: list[StatementLine] = Field(default_factory=list)
    total: str


class IncomeStatement(BaseModel):
    company: str
    currency: str
    start: date
    end: date
    sections: list[StatementSection]
    net_income: str
