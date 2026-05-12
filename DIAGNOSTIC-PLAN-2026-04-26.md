# Integration Diagnostic Rebuild — Technical Plan

**Date:** 2026-04-26
**Author:** Roper DeGarmo (drafted with Claude, shaped by Willison patterns, hardened by Codex review)
**For:** Execution Sunday/Monday after corrected Stage 0 verification
**Output deliverable:** `Signature Integration Milestone View — Roper Update 2026-04-26.xlsx`

**Revision history:**
- v0.1 — initial draft from Claude session
- v0.2 — Willison shaping (sqlite-utils + llm CLI + Datasette stack, eval criteria)
- **v0.3 (current) — Codex review applied:** model name corrected, FTS replaces LIKE, evidence_ids normalized to join table, csv-diff key stabilized, MCP-backed sources get manual precompute step, owner attribution split into 3 fields, prefilter stage added, hybrid hydration, content hashing, QuickBooks audit + SharePoint/Drive manifests added as sources

---

## Goal

Comb every relevant source (email, calendar, transcripts, Airtable, repo baseline, NFP-side artifacts) and produce a refreshed master milestone view in Keara's xlsx format. Add `Problem Type` column. Populate `Owner` ruthlessly — every blank Owner is a structural finding.

The xlsx is the artifact for the Brett 3pm Monday meeting. The supporting `diagnostic.db` (browseable via Datasette) is the receipt drawer that proves every row.

## Operating principles (from Willison CIO briefing + Codex review)

1. **Use the tools.** `sqlite-utils`, `llm` CLI, `files-to-prompt`, `csv-diff`, `datasette` — not bespoke Python.
2. **Evals beat prompts.** Define what a "good milestone row" looks like before extraction. Run the eval against output before publishing.
3. **Cognitive debt check.** Every script readable in one screen. No 500-line Python files.
4. **Compound flywheel.** Don't sync bad data. Baseline is hypothesis, not authority — evidence overrides.
5. **Outbound approval gate.** Diagnostic is read-only. If it becomes the basis for outbound action, gate reapplies.
6. **(NEW from Codex) Deterministic prefilter before LLM.** Don't ask the LLM to compare every evidence item to every milestone. Cheap lexical/embedding narrowing first; LLM only on shortlisted candidates.
7. **(NEW from Codex) Cheap model first, premium model on ambiguous.** Sonnet 4.6 for the bulk extraction; Opus 4.6 only for ambiguous or final-row reconcile.
8. **(NEW from Codex) Hybrid hydration.** Ingest metadata + ids + hashes + short snippets up front; pull full bodies only for shortlisted evidence and final citations.

---

## Data sources

| # | Source | Location | Volume | Access |
|---|---|---|---|---|
| 1 | Email archive | `~/Documents/Palmer-Export/emails.db` | 702,500 msgs total, current through 2026-04-26 20:15 UTC | Direct SQL via `archive_messages_fts` (see Stage 1) |
| 2 | Google Calendar | API via MCP | ~60d back + 60d forward | **Manual precompute:** export to JSON file, then shell pipes from disk |
| 3 | Transcripts | `~/Documents/Transcripts/anka.db` (374 recordings, 6,861 chunks) | All NFP-tagged or integration-keyword | Direct SQL + `transcripts_ask` MCP for semantic; **explicit discovery gate** before downstream stages |
| 4 | Airtable | Signature base `app73mbDkkwMc0kNj` | Tasks + Accounts | `airtable-export` → SQLite |
| 5 | Repo baseline | `~/repos/nfp-integration/` | 04/14 xlsx (108 data rows; 109 max_row includes header), action queue, handoffs | File reads + `openpyxl` |
| 6 | Bamford screenshots | 4 PNGs in email msg `19dc06bfc916c066` | 15 source-doc asks | `llm -a image.png "extract line items"` |
| 7 | SharePoint folder manifest | `Signature Personal` (Bamford-created) | What's actually been uploaded vs. what's still asked | Local Drive mount if synced; manual list if not. **Codex-added.** |
| 8 | NFP-side calendar invites in Outlook | Indirect — visible only via accepted/declined events on your Google Calendar | — | Same as #2; lower priority per Codex |
| 9 | **QuickBooks audit history** | QBO web UI → Reports > Audit Log; export CSV | Who actually transacted in QB vs. who's listed as owner | Manual export (no API access); **Codex-added; high signal for accounting ownership questions** |
| 10 | **Drive activity log** (Google Drive admin or activity API) | NFP SharePoint side requires NFP admin; client Drive activity available locally | Who uploaded what to Bamford's SharePoint folder | Manual / TBD; **Codex-added** |

### Known blind spots
- MS Teams 1:1s with Mary not auto-recorded unless captured by Anka
- NFP internal Slack/Teams channels — no access
- Friday 04/24 integration call you skipped — no transcript

### Lower-value sources Codex deprioritized
- 1Password access logs — likely noise relative to effort
- Outlook duplicates of accepted events — Google Calendar already captures

### Schema caveats
- **Palmer email schema lacks separate from/to/cc columns.** Workaround: use `archive_messages_fts` (FTS5 index already built) querying for `@nfp.com`. **Codex-validated:** FTS pass surfaces 4,050 candidate messages across 1,139 threads since 2026-02-01, vs. only 1,099 from a LIKE pattern. Use FTS.
- **Transcript attribution is fuzzy** for team meetings (multi-speaker, often unidentified). Flag rather than treat as authoritative.
- **04/14 baseline contains stale truths** — e.g., Bamford QB item marked RESOLVED but Bamford's 04/24 red-line proves it isn't. Use evidence to override.

---

## Pipeline architecture

### Stage 0: Setup (once)
```bash
brew install llm
pip install sqlite-utils files-to-prompt airtable-export csv-diff datasette openpyxl
llm install llm-anthropic
llm keys set anthropic   # paste API key
mkdir -p ~/repos/nfp-integration/scripts ~/repos/nfp-integration/runs/2026-04-26
```

**Codex note:** `sqlite-utils`, `llm`, `datasette`, `openpyxl` already installed in this env. `csv-diff` was NOT on PATH — install needed.

### Stage 1: Discovery + access verification
**`scripts/00-discovery.sh`** — counts volume from each source AND verifies access. Output: budget estimate + go/no-go.

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "=== Email volume since 2026-02-01 (FTS) ==="
sqlite3 ~/Documents/Palmer-Export/emails.db \
  "SELECT COUNT(DISTINCT m.id) AS msgs, COUNT(DISTINCT m.gmail_thread_id) AS threads
   FROM archive_messages m
   JOIN archive_messages_fts f ON f.rowid = m.id
   WHERE archive_messages_fts MATCH '\"@nfp.com\"'
     AND m.date_sent >= '2026-02-01';"

echo "=== Transcript discovery gate ==="
# Codex flagged: transcripts DB access not verifiable from sandboxed sessions.
# Verify before proceeding to Stage 2.
ls -la ~/Documents/Transcripts/anka.db 2>&1
sqlite3 ~/Documents/Transcripts/anka.db ".tables" 2>&1 | head -5
# If the above fails, downstream stages must skip transcript ingestion or get manual export.

echo "=== Calendar precompute ==="
# Calendar requires manual MCP call from Claude session, then writes to disk:
# /tmp/precompute/calendar-2026-02-17-to-future.json
# Then shell scripts read from /tmp/precompute/.
ls -la /tmp/precompute/calendar-*.json 2>/dev/null || echo "MISSING: run calendar precompute first"

echo "=== Airtable open tasks tagged NFP/integration ==="
# requires airtable-export run first; counts after.

echo "=== Baseline rows (04/14 xlsx) ==="
python3 -c "import openpyxl; ws = openpyxl.load_workbook('Signature Integration Milestone View — Roper Update 2026-04-14.xlsx').worksheets[0]; print('data rows:', ws.max_row - 1)"
```

**Decision point after discovery:** if email volume > 5,000 candidate messages, scope down to high-signal threads only. LLM cost cap = $50 unless approved higher.

### Stage 2: Manual precompute step (Codex-added)

For sources that require interactive/MCP access (Calendar primarily; Airtable can run unattended via airtable-export), produce JSON exports to `/tmp/precompute/` that downstream shell scripts can consume non-interactively.

```bash
# Run from active Claude session (interactive — has MCP):
mkdir -p /tmp/precompute

# Calendar: dump events 2026-02-17 → today+60 to JSON
# (Claude session calls mcp__google-calendar__list-events and writes results)
# Output: /tmp/precompute/calendar-2026-02-17-to-future.json

# Airtable: airtable-export runs unattended, no precompute needed
airtable-export ~/repos/nfp-integration/data/ app73mbDkkwMc0kNj --sqlite

# Bamford screenshots: precompute via llm vision into JSON
for img in /tmp/bamford-image00*.png; do
  llm -a "$img" -m claude-sonnet-4-6 -t extract-bamford-asks \
    > /tmp/precompute/$(basename "$img" .png).json
done
```

### Stage 3: Extract → diagnostic.db

Schema (`scripts/10-init-schema.sh`):
```sql
CREATE TABLE source_items (
  id INTEGER PRIMARY KEY,
  source_type TEXT NOT NULL,    -- 'email', 'calendar', 'transcript', 'baseline', 'airtable', 'screenshot', 'qbo_audit', 'drive_activity'
  source_id TEXT NOT NULL,
  date_occurred TEXT,
  subject TEXT,
  participants_json JSON,        -- store as JSON; participant analytics rare enough to not need a join table
  body_snippet TEXT,             -- first ~500 chars; full body hydrated on demand
  body_full TEXT,                -- NULL until hydrated for a shortlisted item
  raw_metadata JSON,
  content_hash TEXT,             -- sha256 of canonical content; detects upstream edits on rerun
  source_updated_at TEXT,        -- when the source last changed (if known)
  last_seen_at TEXT DEFAULT CURRENT_TIMESTAMP,
  extracted_at TEXT DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(source_type, source_id)
);

CREATE TABLE baseline_milestones (
  row_num INTEGER PRIMARY KEY,
  milestone_key TEXT UNIQUE,     -- generated stable key: hash(function + primary_text); survives reword
  function TEXT, primary_text TEXT, status TEXT,
  start_date TEXT, finish_date TEXT,
  notes_apr14 TEXT, next_action TEXT, owner TEXT, priority TEXT
);

CREATE TABLE candidate_links (
  -- Codex-added: deterministic prefilter output. Cheap lexical/embedding narrowing
  -- proposes which (source_item, milestone) pairs the LLM should evaluate.
  id INTEGER PRIMARY KEY,
  source_item_id INTEGER NOT NULL REFERENCES source_items(id),
  baseline_row INTEGER REFERENCES baseline_milestones(row_num),
  prefilter_score REAL,          -- 0-1 lexical/embedding match
  prefilter_method TEXT,         -- 'keyword' | 'embedding' | 'date_window'
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(source_item_id, baseline_row)
);

CREATE TABLE clustering_decisions (
  id INTEGER PRIMARY KEY,
  source_item_id INTEGER NOT NULL REFERENCES source_items(id),
  decision TEXT NOT NULL,         -- 'linked' | 'new_milestone' | 'noise'
  baseline_row INTEGER REFERENCES baseline_milestones(row_num),
  proposed_function TEXT,
  proposed_primary_text TEXT,
  proposed_rationale TEXT,
  owner_candidate TEXT,
  owner_basis TEXT,               -- 'explicit' | 'implied' | 'mentioned' | 'unknown'
  owner_confidence TEXT,          -- 'high' | 'medium' | 'low'
  status_signal TEXT,
  llm_confidence TEXT,
  model_used TEXT,
  decided_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE current_milestones (
  id INTEGER PRIMARY KEY,
  milestone_key TEXT UNIQUE NOT NULL,    -- stable across runs; baseline_row's key for existing, generated for new
  baseline_row INTEGER,                  -- NULL if newly discovered
  function TEXT, primary_text TEXT, status TEXT,
  start_date TEXT, finish_date TEXT,
  notes_apr26 TEXT, next_action TEXT,
  owner TEXT,                            -- final displayed owner
  owner_basis TEXT,                      -- explicit | implied | mentioned | unknown | unassigned
  owner_confidence TEXT,                 -- high | medium | low
  priority TEXT,
  problem_type TEXT,                     -- Sequencing | Ownership Vacuum | Resolved | Active
  eval_status TEXT,                      -- pass | fail:<reason> | warn:<reason>
  generated_at TEXT
);

CREATE TABLE milestone_evidence (
  -- Codex-added: replaces comma-separated evidence_ids. Many-to-many.
  id INTEGER PRIMARY KEY,
  milestone_key TEXT NOT NULL REFERENCES current_milestones(milestone_key),
  source_item_id INTEGER NOT NULL REFERENCES source_items(id),
  weight TEXT,                           -- 'authoritative' | 'supporting' | 'contradicts'
  cited_in_notes BOOLEAN DEFAULT 0,
  UNIQUE(milestone_key, source_item_id)
);

CREATE INDEX idx_source_items_date ON source_items(date_occurred);
CREATE INDEX idx_source_items_type ON source_items(source_type);
CREATE INDEX idx_candidate_links_baseline ON candidate_links(baseline_row);
CREATE INDEX idx_milestone_evidence_milestone ON milestone_evidence(milestone_key);
```

Each extract script: under 30 lines, idempotent (UPSERT on `(source_type, source_id)` with content_hash check for re-extraction triggers), uses `sqlite-utils insert`.

```
scripts/
  00-discovery.sh
  10-init-schema.sh
  11-extract-emails.sh        # FTS query → sqlite-utils insert (metadata + snippets only)
  12-extract-calendar.sh      # reads /tmp/precompute/calendar-*.json
  13-extract-transcripts.sh   # gated by Stage 1 verification
  14-extract-airtable.sh
  15-extract-baseline.sh      # openpyxl one-shot Python (xlsx → SQL); generates milestone_key
  16-extract-screenshots.sh   # reads /tmp/precompute/bamford-*.json
  17-extract-qbo-audit.sh     # reads manually-exported CSV
  18-extract-drive-activity.sh # reads manually-exported list
```

### Stage 4: Prefilter (Codex-added — runs before LLM clustering)

**`scripts/25-prefilter.sh`** — deterministic narrowing. Populates `candidate_links`.

For each source_item, propose milestone candidates via:
1. **Keyword match** — if source_item content contains keywords from milestone's primary_text or function, link with score
2. **Date window** — if source_item date is within ±14 days of any baseline milestone's start/finish dates, propose
3. **Embedding similarity** — local `bge-large` embeddings on source_item snippets vs milestone primary_text; top-5 above threshold

Cap candidates per source_item at 5. LLM only sees the shortlist, not the full milestone universe.

### Stage 5: Cluster

**`scripts/30-cluster.sh`** uses saved `llm` template (cheap model — Sonnet 4.6):

```bash
llm --save cluster-milestone -m claude-sonnet-4-6 -s '
You review one piece of evidence about an insurance agency acquisition integration.
Below is the evidence and a SHORTLIST of candidate milestones (pre-filtered).

Decide whether the evidence belongs to one of these candidate milestones, suggests a new
milestone not in the shortlist, or is noise. Return JSON:

{
  "decision": "linked" | "new_milestone" | "noise",
  "baseline_row": int | null,           // if linked
  "proposed_function": "...",            // if new_milestone
  "proposed_primary_text": "...",
  "proposed_rationale": "...",
  "owner_candidate": "..." | null,       // who at NFP appears to own this
  "owner_basis": "explicit" | "implied" | "mentioned" | "unknown",
  "owner_confidence": "high" | "medium" | "low",
  "status_signal": "Complete" | "Open" | "Stuck" | "Disputed" | "Unknown",
  "llm_confidence": "high" | "medium" | "low"
}
'
```

Per evidence item: pipe content + the shortlisted milestones, get JSON back, write to `clustering_decisions`.

### Stage 6: Reconcile (Codex-revised — premium model, hydrated bodies on shortlist)

**`scripts/40-reconcile.sh`** uses second saved template, premium model only on ambiguous rows:

```bash
llm --save reconcile-milestone -m claude-opus-4-6 -s '...'
```

For each baseline milestone:
1. Pull all clustering_decisions linked to it, sorted chronologically
2. **Hydrate full bodies** for the top-N most authoritative evidence items (set body_full from source via Palmer / Anka / Calendar JSON)
3. Pass to LLM with reconcile template
4. Get back: refreshed Status, Owner (with basis + confidence), Notes (with evidence cites by source_item.id), Problem Type, Next Action
5. Write to `current_milestones`, populate `milestone_evidence`

For new proposed milestones with strong evidence (multiple high-confidence cluster decisions): same template, draft as new row, generate stable `milestone_key`.

**Cost shape per Codex:** $25-75 realistic for 3-5k items after lexical narrowing. Sonnet for cluster (cheap); Opus only for ambiguous reconcile or final-pass on flagged rows.

All `llm` calls auto-log to `~/.io.datasette.llm/logs.db` — built-in audit trail.

### Stage 7: Eval

**`scripts/50-eval.sh`** runs the milestone-row eval against every row in `current_milestones`:

```sql
-- Eval queries:
SELECT id, primary_text FROM current_milestones
  WHERE owner IS NULL OR owner = ''
    AND owner_basis != 'unassigned';   -- FAIL: blank owner without explicit "unassigned" rationale

SELECT cm.id, cm.primary_text FROM current_milestones cm
  LEFT JOIN milestone_evidence me ON me.milestone_key = cm.milestone_key
  WHERE me.id IS NULL;                 -- FAIL: no evidence linked

SELECT id, primary_text FROM current_milestones
  WHERE problem_type NOT IN ('Sequencing','Ownership Vacuum','Resolved','Active');  -- FAIL

SELECT id, primary_text FROM current_milestones
  WHERE status = 'Complete' AND length(notes_apr26) < 30;   -- WARN

SELECT id, primary_text FROM current_milestones
  WHERE baseline_row IS NULL AND length(notes_apr26) < 100; -- WARN: new row needs full justification

SELECT cm.id, cm.primary_text, COUNT(*) AS evidence_count
  FROM current_milestones cm
  JOIN milestone_evidence me ON me.milestone_key = cm.milestone_key
  WHERE cm.baseline_row IS NULL
  GROUP BY cm.id
  HAVING evidence_count < 2;            -- WARN: new milestone with only single evidence item
```

Update `eval_status` column. Rows that fail get flagged in the xlsx (Comments tab) — not silently published.

### Eval criteria

```
MILESTONE ROW EVAL:
[ ] Has Function (matches one of the 8+ canonical categories)
[ ] Owner is named NFP person OR explicit "unassigned" with owner_basis='unassigned' and rationale
[ ] Status reflects most recent evidence date, not last update
[ ] At least one row in milestone_evidence cites this milestone_key
[ ] Problem Type assigned (Sequencing | Ownership Vacuum | Resolved | Active)
[ ] Next Action exists or row is closed
[ ] If Status conflicts with baseline, conflict is explained in Notes
[ ] If Owner is blank/unassigned, that blank is itself the diagnostic (note must call it out)
[ ] If new row (baseline_row IS NULL): backed by ≥2 evidence items
```

### Stage 8: Generate xlsx + diff

**`scripts/60-generate-xlsx.sh`** (openpyxl one-shot Python):
- Read `current_milestones` from diagnostic.db
- Match Keara's column order
- Add `Problem Type` column
- Add `Owner Confidence` column (so Brett can see which Owner assignments are high vs. low confidence)
- Comments tab: changelog (rows added, status flips, owner changes vs. 04/14)

**`scripts/61-csv-diff.sh`** — Codex-corrected key:
```bash
# Export both xlsx to CSV via openpyxl
# Diff keyed on milestone_key (stable across reword), not primary_text
csv-diff baseline_2026-04-14.csv current_2026-04-26.csv --key=milestone_key > runs/2026-04-26/diff.txt
```

For 04/14 baseline: generate `milestone_key` retroactively at extract time (Stage 3 step 15) using `hash(function + normalized(primary_text))` so the diff has stable keys on both sides.

### Stage 9: Publish (local-only per Codex)

```bash
datasette serve diagnostic.db --port 8001 &
# Local browse for Travis review. Roper sends path or screen-shares.
```

**No Vercel push** until a redacted dataset and access controls exist. Email/transcript-backed diagnostic data is sensitive.

---

## File layout

```
~/repos/nfp-integration/
  DIAGNOSTIC-PLAN-2026-04-26.md          # this file
  diagnostic.db                          # gitignored (working data)
  Signature Integration Milestone View — Roper Update 2026-04-14.xlsx   # baseline (108 data rows)
  Signature Integration Milestone View — Roper Update 2026-04-26.xlsx   # output
  scripts/
    00-discovery.sh
    10-init-schema.sh
    11-extract-emails.sh
    12-extract-calendar.sh
    13-extract-transcripts.sh
    14-extract-airtable.sh
    15-extract-baseline.sh
    16-extract-screenshots.sh
    17-extract-qbo-audit.sh
    18-extract-drive-activity.sh
    25-prefilter.sh
    30-cluster.sh
    40-reconcile.sh
    50-eval.sh
    60-generate-xlsx.sh
    61-csv-diff.sh
  data/
    airtable-export-2026-04-26.db        # output of airtable-export
  runs/
    2026-04-26/
      discovery.txt
      precompute_manifest.txt
      cluster_decisions.jsonl
      reconcile_decisions.jsonl
      eval_results.txt
      diff.txt
      llm_cost_summary.txt
```

`.gitignore` adds: `diagnostic.db`, `runs/*/`, `data/*.db`, `*.tmp`

---

## Risks & mitigations

| Risk | Mitigation |
|---|---|
| Email body_text proxy false positives/negatives | FTS replaces LIKE per Codex (4,050 vs 1,099 hits). Spot-check 20 random items after cluster pass; if accuracy < 90% switch to Gmail API header pull on flagged threads. |
| Transcript attribution fuzz on team meetings | Tag every transcript-derived evidence with `confidence: low` if attribution unclear; flag in xlsx Comments |
| LLM cost explosion | Discovery sets the budget. Hard cap $50 unless approved. Codex realistic estimate $25-75 with prefiltering. |
| LLM hallucinated new milestones | Every proposed-new row must have ≥2 evidence items; eval rejects rows that fail |
| Baseline drift / accidentally trusting 04/14 | Reconcile template explicitly told: baseline is hypothesis. Evidence dated > baseline date overrides. |
| Cognitive debt | Every script under 30 lines; no Python files > 50 lines; Roper reads each before running |
| Slop reaching Brett | Eval is mandatory; failed rows surface in Comments tab; Roper does final eyeballing pass |
| Lethal trifecta | Diagnostic is read-only. No outbound. Re-evaluate if scope grows. |
| Milestone reword treated as delete/add in diff | csv-diff keyed on stable `milestone_key`, not primary_text (Codex fix) |
| MCP-backed sources unavailable in shell | Manual precompute step writes JSON to /tmp/precompute/; shell scripts read from disk (Codex fix) |
| Source content changes between runs | content_hash + source_updated_at columns detect; trigger re-extract on hash mismatch |

---

## Codex's confirmed answers to original open questions

1. **Tooling alignment.** sqlite-utils + llm CLI + Datasette is the right core. Skip Datasette plugins and dogsheep-beta for one-shot.
2. **LLM template design.** Two-template pattern (cluster + reconcile) is sound. Add deterministic prefilter so LLM doesn't compare every item to every milestone.
3. **Schema.** source_items fine as raw store. Add milestone_evidence + candidate_links tables. Keep participants as JSON unless analytics needed.
4. **Idempotency.** UPSERT alone insufficient for mutable sources. Add content_hash, source_updated_at, last_seen_at. Full versioning only for transcripts/OCR if reruns matter.
5. **Dogsheep-beta.** Skip for one-shot. Reconsider if recurring.
6. **Cost.** $25-75 realistic with lexical narrowing + cheap-model-first. `claude-opus-4-7` does NOT exist in this env — use `claude-opus-4-6`.
7. **Hydration.** Hybrid: metadata + ids + hashes + snippets up front; full bodies on demand for shortlisted items.
8. **Owner inference.** Three-field model: `owner_candidate`, `owner_basis` (explicit/implied/mentioned/unknown), `owner_confidence`.
9. **Missing sources.** High value: SharePoint/Drive manifests, QuickBooks audit history, repo handoff docs. Low value: Outlook duplicates, 1Password logs.
10. **Recurring vs one-shot.** If biweekly: add stable milestone ids (DONE), source watermarks (DONE), content hashing (DONE), delta-only reruns. Then dogsheep-beta makes sense.
11. **Publishing.** Local-only. No Vercel without redaction + access controls.

---

## Suggested ordering

1. **(NOW) Run corrected Stage 0** — access verification, source counts via FTS, stable milestone keys generated for baseline, one pilot Function (e.g., HR) end-to-end as a sample.
2. Validate pilot quality. Eyeball every row in HR Function output.
3. Apply learnings to remaining Functions.
4. Full run.
5. Stage 7 eval. Fix flagged rows.
6. Generate xlsx + diff.
7. Sunday evening: send xlsx + Datasette URL to Travis for Monday strategy session.

---

## Out of scope (for now)

- Auto-emailing NFP about findings (outbound gate doesn't apply yet — manual only)
- Real-time updates as new emails land (this is a snapshot, not a live dashboard)
- Cross-acquisition comparison (other NFP-acquired books) — interesting future work
- Predictive timeline modeling — interesting future work
- Internal NFP system queries (Epic, Coupa, etc.) — no API access
- Vercel/cloud publishing — local Datasette only until redaction layer exists

---

*v0.3 — drafted by Claude, shaped by Willison's CIO patterns, hardened by Codex's technical review (5 specific fixes + architectural additions). Ready for execution.*
