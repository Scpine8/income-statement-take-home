from datetime import date

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.ledger import load_ledger
from app.models import IncomeStatement
from app.statement import build_income_statement

LEDGER = load_ledger()

app = FastAPI(title="Northwind income statement")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/income-statement", response_model=IncomeStatement)
def income_statement(
    start: date = Query(..., description="Inclusive period start, YYYY-MM-DD"),
    end: date = Query(..., description="Inclusive period end, YYYY-MM-DD"),
) -> IncomeStatement:
    if start > end:
        raise HTTPException(status_code=400, detail="start must be on or before end")
    return build_income_statement(LEDGER, start, end)
