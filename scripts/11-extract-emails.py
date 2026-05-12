#!/usr/bin/env python3
"""
Extract Finance-relevant emails from Palmer into diagnostic.db.

- Source: ~/Documents/Palmer-Export/emails.db (FTS5 indexed).
- Filter: nfp.com participants AND Finance keyword present.
- Snippet only (first 500 chars of body_text); body_full deferred to hydration.
- content_hash for change detection on rerun.
"""
import hashlib
import json
import re
import sqlite3
import sys
from pathlib import Path

PALMER = Path.home() / "Documents" / "Palmer-Export" / "emails.db"
DIAG = Path.home() / "repos" / "nfp-integration" / "diagnostic.db"

# STRONG Finance keywords (high precision). Multi-word phrases or domain-specific terms.
# Each is matched as a substring (already non-ambiguous) OR with word boundaries for short tokens.
FINANCE_STRONG = [
    "bamford", "quickbooks", "qbo ", " qbo", "coupa", "amex", "american express",
    "landmark", "commission statement", "carrier statement", "deposit support",
    "accounting", "vendor invoice", "reconciliation", "reconcile",
    "workday", "concur", "month end", "month-end",
    "rubinbrown", "rubin brown", "brooke mckenzie", "ogletree", "acumen kc",
    "acumen kansas", "w-9", " w9 ", "ap onboarding", "balance sheet",
    "rubinbrown", "brooke", "smartsheet finance",
]
# Word-boundary tokens (short / risky if substring)
FINANCE_BOUNDED = ["ach", "w9", "qbo"]
# Compose a single regex for boundary tokens
BOUNDED_RE = re.compile(r"\b(" + "|".join(re.escape(t) for t in FINANCE_BOUNDED) + r")\b", re.IGNORECASE)

def has_finance_signal(text: str) -> list:
    """Returns list of matched finance keywords. Empty if none."""
    if not text:
        return []
    lower = text.lower()
    matched = [kw.strip() for kw in FINANCE_STRONG if kw in lower]
    bounded_hits = BOUNDED_RE.findall(text)
    matched.extend(b.lower() for b in bounded_hits)
    return list(set(matched))

def main():
    palmer = sqlite3.connect(f"file:{PALMER}?mode=ro", uri=True)
    palmer.row_factory = sqlite3.Row

    # Step 1: Get all nfp.com candidate threads since 02/01
    nfp_query = """
        SELECT m.id, m.gmail_message_id, m.gmail_thread_id, m.subject,
               m.date_sent, m.body_plain_cleaned, m.body_text, m.gmail_labels
        FROM archive_messages m
        JOIN archive_messages_fts f ON f.rowid = m.id
        WHERE archive_messages_fts MATCH '"@nfp.com"'
          AND m.date_sent >= '2026-02-01'
        ORDER BY m.date_sent
    """
    candidates = palmer.execute(nfp_query).fetchall()
    print(f"NFP candidates (FTS): {len(candidates)}")

    # Step 2: Filter to Finance-keyword present
    finance_msgs = []
    for c in candidates:
        body = (c["body_plain_cleaned"] or c["body_text"] or "")
        subj = c["subject"] or ""
        matched = has_finance_signal(subj + " " + body)
        if matched:
            finance_msgs.append((c, matched))

    print(f"Finance-keyword filter: {len(finance_msgs)} of {len(candidates)}")

    # Step 3: Insert into source_items
    diag = sqlite3.connect(DIAG)
    inserted = 0
    skipped = 0
    for c, matched in finance_msgs:
        body = (c["body_plain_cleaned"] or c["body_text"] or "")
        snippet = body[:500] if body else None

        canonical = (str(c["gmail_message_id"]) + "|" + str(c["subject"]) + "|" + (snippet or ""))
        content_hash = hashlib.sha256(canonical.encode()).hexdigest()[:16]

        meta = {
            "gmail_thread_id": c["gmail_thread_id"],
            "gmail_labels": c["gmail_labels"],
            "matched_keywords": matched,
            "palmer_id": c["id"],
        }

        # Fall back to palmer_id when gmail_message_id is NULL (older / orphaned rows)
        source_id = c["gmail_message_id"] or f"palmer:{c['id']}"

        try:
            diag.execute("""
                INSERT INTO source_items
                  (source_type, source_id, date_occurred, subject, participants_json,
                   body_snippet, body_full, raw_metadata, content_hash, source_updated_at)
                VALUES ('email', ?, ?, ?, NULL, ?, NULL, ?, ?, ?)
                ON CONFLICT(source_type, source_id) DO UPDATE SET
                  date_occurred=excluded.date_occurred,
                  subject=excluded.subject,
                  body_snippet=excluded.body_snippet,
                  raw_metadata=excluded.raw_metadata,
                  content_hash=excluded.content_hash,
                  source_updated_at=excluded.source_updated_at,
                  last_seen_at=CURRENT_TIMESTAMP
            """, (
                source_id,
                c["date_sent"],
                c["subject"],
                snippet,
                json.dumps(meta),
                content_hash,
                c["date_sent"],
            ))
            inserted += 1
        except sqlite3.Error as e:
            print(f"  ERR on {source_id}: {e}", file=sys.stderr)
            skipped += 1

    diag.commit()
    print(f"\nInserted/updated: {inserted}")
    print(f"Errors: {skipped}")

    # Stats
    print("\n=== Top matched keywords ===")
    from collections import Counter
    kw_counts = Counter()
    for _, matched in finance_msgs:
        for kw in matched:
            kw_counts[kw] += 1
    for kw, n in kw_counts.most_common(15):
        print(f"  {kw}: {n}")

    print("\n=== Date distribution by month ===")
    month_counts = Counter()
    for c, _ in finance_msgs:
        if c["date_sent"]:
            month_counts[c["date_sent"][:7]] += 1
    for m, n in sorted(month_counts.items()):
        print(f"  {m}: {n}")

    palmer.close()
    diag.close()

if __name__ == "__main__":
    main()
