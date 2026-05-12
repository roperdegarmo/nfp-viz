#!/usr/bin/env python3
"""
Extract baseline milestones from 04/14 xlsx into diagnostic.db.

- Filters out color-legend / non-data rows (anything where Function isn't in the canonical 9).
- Generates stable milestone_key = sha256(canonical_function + normalized(primary_text))[:16].
- UPSERTs into baseline_milestones.
"""
import hashlib
import re
import sqlite3
import sys
from pathlib import Path

import openpyxl

REPO = Path.home() / "repos" / "nfp-integration"
XLSX = REPO / "Signature Integration Milestone View — Roper Update 2026-04-14.xlsx"
DB = REPO / "diagnostic.db"

# Canonical Functions seen in 04/14 baseline (numbered ones + Roper's overflow)
CANONICAL_FUNCTIONS = {
    "01. HR", "02. Marketing", "03. Technology", "04. Finance", "05. Treasury",
    "07. Risk Management", "08. Carrier Management", "09. Licensing & Registrations",
    "10. Region/Sales/Ops",
    # Roper's overflow rows (added 4/5)
    "HR", "Marketing", "Technology", "Carrier Mgmt", "Regional/Sales", "Integration",
    "ROPER'S ADDITIONAL ITEMS (added 4/5)", "WAITING ON NFP (added 4/5)",
}
SKIP_FUNCTIONS = {"Blue", "Yellow", "Dark Green", "No color", "COLOR LEGEND"}

def normalize_text(s: str) -> str:
    if not s:
        return ""
    s = re.sub(r"\s+", " ", s.strip().lower())
    s = re.sub(r"[^\w\s]", "", s)
    return s

def make_key(function: str, primary: str) -> str:
    """Stable key surviving primary_text reword: based on (function, normalized first 60 chars)."""
    fn = (function or "").strip().lower()
    pr = normalize_text(primary)[:60]
    raw = f"{fn}|{pr}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

def main():
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    ws = wb.worksheets[0]
    headers = [c.value for c in ws[1]]
    print(f"Headers: {headers}")

    rows_inserted = 0
    rows_skipped = 0
    rows_legend = 0

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    for idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        function, primary, status, start, finish, notes, next_action, owner, priority = (row + (None,)*9)[:9]

        if not function or function in SKIP_FUNCTIONS:
            rows_legend += 1
            continue
        if function not in CANONICAL_FUNCTIONS:
            print(f"  WARN row {idx}: unknown function '{function}' — keeping anyway")

        if not primary:
            rows_skipped += 1
            continue

        key = make_key(function, primary)
        conn.execute("""
            INSERT INTO baseline_milestones
              (row_num, milestone_key, function, primary_text, status, start_date, finish_date, notes_apr14, next_action, owner, priority)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(row_num) DO UPDATE SET
              milestone_key=excluded.milestone_key,
              function=excluded.function,
              primary_text=excluded.primary_text,
              status=excluded.status,
              start_date=excluded.start_date,
              finish_date=excluded.finish_date,
              notes_apr14=excluded.notes_apr14,
              next_action=excluded.next_action,
              owner=excluded.owner,
              priority=excluded.priority
        """, (
            idx, key, function, primary, status,
            str(start) if start else None,
            str(finish) if finish else None,
            notes, next_action, owner, priority,
        ))
        rows_inserted += 1

    conn.commit()

    print(f"\nInserted/updated: {rows_inserted}")
    print(f"Color-legend skipped: {rows_legend}")
    print(f"Empty primary_text skipped: {rows_skipped}")

    print("\n=== Function distribution in diagnostic.db ===")
    for f, n in conn.execute("SELECT function, COUNT(*) FROM baseline_milestones GROUP BY function ORDER BY function"):
        print(f"  {f}: {n}")

    print("\n=== Pilot: Finance milestones ===")
    for r in conn.execute("SELECT row_num, milestone_key, status, primary_text FROM baseline_milestones WHERE function = '04. Finance' ORDER BY row_num"):
        print(f"  [{r['row_num']}] {r['milestone_key']} {r['status'] or '-':<10} {(r['primary_text'] or '')[:60]}")

    conn.close()

if __name__ == "__main__":
    main()
