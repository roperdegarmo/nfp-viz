-- Diagnostic DB schema for NFP integration milestone rebuild
-- Stable across reruns; UPSERT-friendly via UNIQUE constraints

CREATE TABLE IF NOT EXISTS source_items (
  id INTEGER PRIMARY KEY,
  source_type TEXT NOT NULL,
  source_id TEXT NOT NULL,
  date_occurred TEXT,
  subject TEXT,
  participants_json JSON,
  body_snippet TEXT,
  body_full TEXT,
  raw_metadata JSON,
  content_hash TEXT,
  source_updated_at TEXT,
  last_seen_at TEXT DEFAULT CURRENT_TIMESTAMP,
  extracted_at TEXT DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(source_type, source_id)
);

CREATE TABLE IF NOT EXISTS baseline_milestones (
  row_num INTEGER PRIMARY KEY,
  milestone_key TEXT UNIQUE,
  function TEXT,
  primary_text TEXT,
  status TEXT,
  start_date TEXT,
  finish_date TEXT,
  notes_apr14 TEXT,
  next_action TEXT,
  owner TEXT,
  priority TEXT
);

CREATE TABLE IF NOT EXISTS candidate_links (
  id INTEGER PRIMARY KEY,
  source_item_id INTEGER NOT NULL REFERENCES source_items(id),
  baseline_row INTEGER REFERENCES baseline_milestones(row_num),
  prefilter_score REAL,
  prefilter_method TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(source_item_id, baseline_row)
);

CREATE TABLE IF NOT EXISTS clustering_decisions (
  id INTEGER PRIMARY KEY,
  source_item_id INTEGER NOT NULL REFERENCES source_items(id),
  decision TEXT NOT NULL,
  baseline_row INTEGER REFERENCES baseline_milestones(row_num),
  proposed_function TEXT,
  proposed_primary_text TEXT,
  proposed_rationale TEXT,
  owner_candidate TEXT,
  owner_basis TEXT,
  owner_confidence TEXT,
  status_signal TEXT,
  llm_confidence TEXT,
  model_used TEXT,
  decided_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS current_milestones (
  id INTEGER PRIMARY KEY,
  milestone_key TEXT UNIQUE NOT NULL,
  baseline_row INTEGER,
  function TEXT,
  primary_text TEXT,
  status TEXT,
  start_date TEXT,
  finish_date TEXT,
  notes_apr26 TEXT,
  next_action TEXT,
  owner TEXT,
  owner_basis TEXT,
  owner_confidence TEXT,
  priority TEXT,
  problem_type TEXT,
  eval_status TEXT,
  generated_at TEXT
);

CREATE TABLE IF NOT EXISTS milestone_evidence (
  id INTEGER PRIMARY KEY,
  milestone_key TEXT NOT NULL REFERENCES current_milestones(milestone_key),
  source_item_id INTEGER NOT NULL REFERENCES source_items(id),
  weight TEXT,
  cited_in_notes BOOLEAN DEFAULT 0,
  UNIQUE(milestone_key, source_item_id)
);

CREATE INDEX IF NOT EXISTS idx_source_items_date ON source_items(date_occurred);
CREATE INDEX IF NOT EXISTS idx_source_items_type ON source_items(source_type);
CREATE INDEX IF NOT EXISTS idx_candidate_links_baseline ON candidate_links(baseline_row);
CREATE INDEX IF NOT EXISTS idx_milestone_evidence_milestone ON milestone_evidence(milestone_key);
CREATE INDEX IF NOT EXISTS idx_clustering_decisions_source ON clustering_decisions(source_item_id);
