# tools/tabular_demo.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Tuple


TABULAR_DATA: List[Dict[str, Any]] = [
    {"quarter": "Q1", "revenue_m": 120, "net_income_m": 15},
    {"quarter": "Q2", "revenue_m": 140, "net_income_m": 22},
    {"quarter": "Q3", "revenue_m": 135, "net_income_m": 18},
    {"quarter": "Q4", "revenue_m": 160, "net_income_m": 30},
]


@dataclass(frozen=True)
class TabularQAResult:
    mode: str
    question: str
    answer: str
    final_answer: str
    confidence: float
    reason_summary: str
    act_summary: str
    evidence: List[Dict[str, Any]]
    checks: Dict[str, Any]
    table: List[Dict[str, Any]]


def _validate_table(table: List[Dict[str, Any]], required_cols: Tuple[str, ...]) -> None:
    if not isinstance(table, list) or not table:
        raise ValueError("Table must be a non-empty list of row dictionaries.")
    for i, row in enumerate(table):
        if not isinstance(row, dict):
            raise ValueError(f"Row {i} is not a dict.")
        for col in required_cols:
            if col not in row:
                raise ValueError(f"Missing column '{col}' in row {i}.")


def _argmax_by_numeric_column(
    table: List[Dict[str, Any]],
    key_col: str,
    value_col: str
) -> Tuple[str, float, Dict[str, Any]]:
    best_row: Optional[Dict[str, Any]] = None
    best_val: Optional[float] = None

    for row in table:
        raw_val = row.get(value_col)
        if raw_val is None:
            continue
        try:
            val = float(raw_val)
        except (TypeError, ValueError):
            continue

        if best_val is None or val > best_val:
            best_val = val
            best_row = row

    if best_row is None or best_val is None:
        raise ValueError(f"Could not compute max for '{value_col}' (no valid numeric values).")

    best_key = str(best_row.get(key_col, "N/A"))
    return best_key, best_val, best_row


def answer_highest_net_income(table: List[Dict[str, Any]] = TABULAR_DATA) -> Dict[str, Any]:
    """
    Answers: 'Which quarter has the highest net income?'
    Returns a structured dict suitable for UI + evaluation (with evidence).
    """
    question = "Which quarter has the highest net income?"

    # ReAct - Reason (brief, not chain-of-thought)
    reason_summary = (
        "We need to identify the quarter with the maximum value in the 'net_income_m' column."
    )

    # Act: validate schema + compute argmax
    required_cols = ("quarter", "net_income_m")
    _validate_table(table, required_cols)

    best_q, best_val, best_row = _argmax_by_numeric_column(
        table=table, key_col="quarter", value_col="net_income_m"
    )

    act_summary = "Validated table schema and selected the maximum 'net_income_m' across all rows."

    # Checks for evaluation transparency
    all_vals = []
    for r in table:
        try:
            all_vals.append(float(r.get("net_income_m")))
        except (TypeError, ValueError):
            all_vals.append(None)

    checks = {
        "compared_column": "net_income_m",
        "quarters_seen": [r.get("quarter") for r in table],
        "net_income_values": all_vals,
        "max_net_income_m": best_val,
        "max_quarter": best_q,
    }

    evidence = [{
        "quarter": best_row.get("quarter"),
        "net_income_m": best_row.get("net_income_m"),
        "revenue_m": best_row.get("revenue_m"),
    }]

    answer = best_q
    final_answer = f"{best_q} has the highest net income ({best_val:g}M)."

    # This is deterministic from the table → very high confidence
    confidence = 0.99

    return TabularQAResult(
        mode="hard_plus_tabular",
        question=question,
        answer=answer,
        final_answer=final_answer,
        confidence=confidence,
        reason_summary=reason_summary,
        act_summary=act_summary,
        evidence=evidence,
        checks=checks,
        table=table,
    ).__dict__
