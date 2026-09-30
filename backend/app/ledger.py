from __future__ import annotations

from pathlib import Path

from app.models import Ledger

DEFAULT_LEDGER_PATH = Path(__file__).resolve().parents[2] / "ledger.json"


def load_ledger(path: Path | None = None) -> Ledger:
    source = path or DEFAULT_LEDGER_PATH
    return Ledger.model_validate_json(source.read_text())
