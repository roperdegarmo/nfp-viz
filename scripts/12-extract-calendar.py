#!/usr/bin/env python3
"""
Extract Finance-relevant calendar events from precompute JSONL into diagnostic.db.

Reads /tmp/precompute/calendar-nfp-events.jsonl (74 NFP-matching events).
Filters further to Finance-domain (Bamford-attended, accounting keywords, Coupa, etc.).
"""
import hashlib
import json
import sqlite3
from pathlib import Path

JSONL = Path("/tmp/precompute/calendar-nfp-events.jsonl")
DIAG = Path.home() / "repos" / "nfp-integration" / "diagnostic.db"

FINANCE_SIGNALS = [
    "bamford", "accounting", "finance", "coupa", "ap onboarding", "vendor",
    "month end", "month-end", "reconciliation", "quickbooks", "qbo",
    "amex", "concur", "workday", "expense", "audit", "balance sheet",
    "rubinbrown", "rubin brown", "brooke",
]
FINANCE_ATTENDEES = [
    "mary.bamford@nfp.com", "jeff.gould@nfp.com", "amy.stewart@nfp.com",
    "jgould@nfp.com", "rajulla.nadar@nfp.com", "jackie.searles@nfp.com",
]

def main():
    if not JSONL.exists():
        print(f"MISSING: {JSONL}")
        return
    diag = sqlite3.connect(DIAG)
    inserted = 0
    finance_events = []
    for line in JSONL.read_text().splitlines():
        if not line.strip():
            continue
        ev = json.loads(line)
        haystack = ((ev.get("summary") or "") + " " + (ev.get("description") or "")).lower()
        attendees = [a.lower() for a in (ev.get("attendees") or [])]
        organizer = (ev.get("organizer") or "").lower()

        matched_kw = [k for k in FINANCE_SIGNALS if k in haystack]
        matched_atndee = [a for a in FINANCE_ATTENDEES if a in attendees or a == organizer]

        if matched_kw or matched_atndee:
            finance_events.append((ev, matched_kw, matched_atndee))

    print(f"Total NFP events in source: {sum(1 for line in JSONL.read_text().splitlines() if line.strip())}")
    print(f"Finance-matching events: {len(finance_events)}")

    for ev, kw, atn in finance_events:
        meta = {
            "matched_keywords": kw,
            "matched_attendees": atn,
            "matching_signals": ev.get("matching_signals", []),
            "status": ev.get("status"),
            "response_status": ev.get("response_status"),
            "location": ev.get("location"),
        }
        snippet = (ev.get("summary") or "") + ((" — " + ev["description"][:400]) if ev.get("description") else "")
        canonical = json.dumps([ev.get("id"), ev.get("summary"), ev.get("start"), ev.get("end")], sort_keys=True)
        content_hash = hashlib.sha256(canonical.encode()).hexdigest()[:16]

        diag.execute("""
            INSERT INTO source_items
              (source_type, source_id, date_occurred, subject, participants_json,
               body_snippet, body_full, raw_metadata, content_hash, source_updated_at)
            VALUES ('calendar', ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(source_type, source_id) DO UPDATE SET
              date_occurred=excluded.date_occurred, subject=excluded.subject,
              participants_json=excluded.participants_json, body_snippet=excluded.body_snippet,
              body_full=excluded.body_full, raw_metadata=excluded.raw_metadata,
              content_hash=excluded.content_hash, source_updated_at=excluded.source_updated_at,
              last_seen_at=CURRENT_TIMESTAMP
        """, (
            ev.get("id"),
            ev.get("start"),
            ev.get("summary"),
            json.dumps(ev.get("attendees") or []),
            snippet[:500],
            ev.get("description"),
            json.dumps(meta),
            content_hash,
            ev.get("start"),
        ))
        inserted += 1

    diag.commit()
    print(f"Inserted/updated: {inserted}")

    # Sample
    print("\n=== Sample Finance calendar events ===")
    for r in diag.execute("SELECT date_occurred, subject FROM source_items WHERE source_type = 'calendar' ORDER BY date_occurred LIMIT 10"):
        print(f"  {r[0][:10] if r[0] else '?':<12} {r[1]}")

if __name__ == "__main__":
    main()
