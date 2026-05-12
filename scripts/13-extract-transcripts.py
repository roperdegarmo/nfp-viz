#!/usr/bin/env python3
"""
Extract Finance-relevant transcripts from Anka into diagnostic.db.

Source: ~/Documents/Transcripts/anka.db (378 recordings, 84 NFP-tagged).
Filter NFP-tagged transcripts further by Finance keywords in title or text.
"""
import hashlib
import json
import sqlite3
from pathlib import Path

ANKA = Path.home() / "Documents" / "Transcripts" / "anka.db"
DIAG = Path.home() / "repos" / "nfp-integration" / "diagnostic.db"

FINANCE_TITLE_SIGNALS = [
    "bamford", "accounting", "finance", "coupa", "month end", "month-end",
    "quickbooks", "qbo", "reconciliation", "expense", "amex", "concur",
    "workday", "balance sheet", "rubinbrown", "rubin brown", "brooke",
    "smartsheet", "vendor", "audit", "audit log",
]
NFP_TITLE_SIGNALS = [
    "nfp", "mullen", "keara", "brett", "connelly", "seckner", "integration", "epic",
]

def main():
    anka = sqlite3.connect(f"file:{ANKA}?mode=ro", uri=True)
    anka.row_factory = sqlite3.Row
    diag = sqlite3.connect(DIAG)

    # Need schema first
    cols = [r[1] for r in anka.execute("PRAGMA table_info(recordings)")]
    print(f"Anka recordings columns: {cols}")

    rows = anka.execute("SELECT * FROM recordings").fetchall()
    print(f"Total recordings: {len(rows)}")

    finance_rows = []
    for r in rows:
        title = (r["title"] or "").lower() if "title" in r.keys() else ""
        account = (r["account_name"] or "").lower() if "account_name" in r.keys() else ""
        # Check if NFP-related
        is_nfp = any(s in (title + " " + account) for s in NFP_TITLE_SIGNALS)
        # Check if Finance-related
        is_finance = any(s in title for s in FINANCE_TITLE_SIGNALS)
        if is_nfp or is_finance:
            finance_rows.append(r)

    print(f"NFP+Finance candidate transcripts: {len(finance_rows)}")

    inserted = 0
    for r in finance_rows:
        # Get full transcript text via chunks
        chunks = anka.execute("SELECT text FROM chunks WHERE recording_id = ? ORDER BY chunk_index", (r["id"],)).fetchall()
        full_text = "\n".join(c["text"] for c in chunks if c["text"])
        snippet = full_text[:500] if full_text else None

        # Final Finance filter on full text
        finance_kw = [k for k in FINANCE_TITLE_SIGNALS if k in full_text.lower()]
        if not finance_kw and not any(s in (r["title"] or "").lower() for s in FINANCE_TITLE_SIGNALS):
            continue  # NFP but not Finance

        meta_keys = list(r.keys())
        raw_meta = {k: r[k] for k in meta_keys if k not in ("id",)}
        meta = {
            "matched_finance_keywords": finance_kw,
            "anka_id": r["id"],
            "title": r["title"],
            "account_name": r["account_name"] if "account_name" in r.keys() else None,
            "raw_metadata_keys": meta_keys,
        }

        canonical = (str(r["id"]) + "|" + (r["title"] or "") + "|" + snippet[:200] if snippet else "")
        content_hash = hashlib.sha256(canonical.encode()).hexdigest()[:16]

        date_field = r["created_at"] if "created_at" in r.keys() else (r["recorded_at"] if "recorded_at" in r.keys() else None)

        diag.execute("""
            INSERT INTO source_items
              (source_type, source_id, date_occurred, subject, participants_json,
               body_snippet, body_full, raw_metadata, content_hash, source_updated_at)
            VALUES ('transcript', ?, ?, ?, NULL, ?, ?, ?, ?, ?)
            ON CONFLICT(source_type, source_id) DO UPDATE SET
              date_occurred=excluded.date_occurred, subject=excluded.subject,
              body_snippet=excluded.body_snippet, body_full=excluded.body_full,
              raw_metadata=excluded.raw_metadata, content_hash=excluded.content_hash,
              source_updated_at=excluded.source_updated_at, last_seen_at=CURRENT_TIMESTAMP
        """, (
            f"anka:{r['id']}",
            date_field,
            r["title"],
            snippet,
            full_text,
            json.dumps(meta),
            content_hash,
            date_field,
        ))
        inserted += 1

    diag.commit()
    print(f"Inserted/updated: {inserted}")
    print("\n=== Sample Finance transcripts ===")
    for row in diag.execute("SELECT date_occurred, subject FROM source_items WHERE source_type = 'transcript' ORDER BY date_occurred DESC LIMIT 10"):
        print(f"  {(row[0] or '?')[:19]:<22} {row[1]}")

if __name__ == "__main__":
    main()
