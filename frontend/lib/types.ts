export type StatementLine = {
  number: string;
  name: string;
  amount: string;
};

export type StatementSection = {
  id:
    | "revenue"
    | "cogs"
    | "gross_profit"
    | "operating_expenses"
    | "operating_income"
    | "other_income"
    | "net_income";
  title: string;
  kind: "accounts" | "result";
  lines: StatementLine[];
  total: string;
};

export type IncomeStatement = {
  company: string;
  currency: string;
  start: string;
  end: string;
  sections: StatementSection[];
  net_income: string;
};
