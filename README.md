# Northwind Coffee Roasters — income statement

A small full-stack app that serves an income statement for any inclusive date range from `ledger.json`.

## Prerequisites

Verified on macOS (Apple Silicon):

| Tool | Version |
| --- | --- |
| Python (via uv) | 3.12.14 |
| uv | 0.12.21 |
| FastAPI | 0.142.1 |
| Pydantic | 2.13.5 |
| Uvicorn | 0.54.0 |
| Bun | 1.4.2 |
| Next.js | 15.5.26 |
| React | 19.1 |
| TypeScript | 5.9.3 |

Install [uv](https://docs.astral.sh/uv/) and [Bun](https://bun.sh/) if they are not already on the machine. uv downloads Python 3.12 for the backend; the system Python is not used.

## Run

From the repository root:

```sh
make install
```

Then, in two terminals:

```sh
make backend    # http://localhost:8000
make frontend   # http://localhost:3000
```

Open http://localhost:3000. The page defaults to Q1 2026 (`2026-01-01` through `2026-03-31`). Change the dates and press Apply.

The API is `GET /income-statement?start=YYYY-MM-DD&end=YYYY-MM-DD`.

## Tests

```sh
make test
```

That runs pytest in `backend/` and `bun test` from the repository root. Backend and frontend can also be run separately with `make test-backend` and `make test-frontend`.
