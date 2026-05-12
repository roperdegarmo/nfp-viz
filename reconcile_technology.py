#!/usr/bin/env python3
"""Reconcile pass for the Technology function."""

import hashlib
import sqlite3
from collections import Counter
from datetime import datetime

DB = "/Users/roperdegarmo/repos/nfp-integration/diagnostic.db"
GENERATED_AT = datetime.now().isoformat(timespec="seconds")
FUNCTION = "03. Technology"


def mkey(text: str) -> str:
    norm = text.strip().lower()
    return hashlib.sha256(f"03. technology|{norm}".encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Milestone definitions
# Each tuple: (baseline_row_or_None, primary_text, status, owner, owner_basis,
#              owner_confidence, problem_type, notes, next_action,
#              evidence: [(source_item_id, weight, cited)])
# ---------------------------------------------------------------------------

MILESTONES = [
    # ---- Email security / NFP IT delivery (positive case) -----------------
    (
        36, "Cybersecurity Environment Assessment / Security Scan",
        "Complete", "Brandon Jackson + Tracy McClain (NFP)",
        "explicit", "high", "On Track",
        "NFP IT delivery model worked cleanly — Brandon Jackson + Tracy McClain "
        "owned scan + credentials handoff end-to-end (src 89, 414, 415, 420, 424, 805).",
        "None — closed.",
        [(89, "primary", True), (89, "primary", True), (414, "supporting", True),
         (415, "supporting", True), (420, "supporting", True),
         (424, "supporting", True), (805, "supporting", False)],
    ),
    (
        37, "Cybersecurity Environment Remediation (FortiClient + Ninjio)",
        "In Progress", "NFP Tech (FortiClient: NFP Tech Ops)",
        "explicit", "high", "On Track",
        "FortiClient rollout 04/22 (src 506, 543); Ninjio episode delivered 04/20 "
        "(src 551); ongoing remediation cadence (src 660).",
        "Confirm FortiClient install on Roper's machine; finish Ninjio episode.",
        [(414, "supporting", False), (506, "primary", True),
         (543, "primary", True), (551, "primary", True), (660, "supporting", True)],
    ),
    (
        35, "Technology Intro call with acquisition IT team",
        "Complete", "Marco Alta (NFP)", "explicit", "high", "On Track",
        "Closed at intro call (src 386).",
        "None.",
        [(386, "primary", True)],
    ),

    # ---- Application deep dives (Roper-side, in motion) -------------------
    (
        49, "Application Deep Dive — Airtable",
        "In Progress", "Roper / Courtney Kendrick",
        "explicit", "high", "On Track",
        "Day-in-the-life follow-up scheduled, Airtable deep dive on agenda "
        "(src 349, 652).",
        "Hold scheduled deep-dive session w/ Courtney.",
        [(349, "primary", True), (652, "supporting", True)],
    ),
    (
        50, "Application Deep Dive — Claude AI",
        "Not Started", "Roper (waiting)",
        "explicit", "medium", "Sequencing",
        "Claude AI deep-dive deferred behind Epic + DNS workstreams; not blocked, "
        "queued by Roper.",
        "Schedule once Epic hypercare stabilizes.",
        [],
    ),

    # ---- Epic — sequencing/stuck (per lens) -------------------------------
    (
        96, "Epic smoke testing + go-live (KC1 branch)",
        "In Progress", "NFP Tech (Mary Ondrasek, Jane Harlow, Julie Lovall) + Roper",
        "explicit", "high", "Sequencing/Stuck",
        "KC1 branch live 04/16 BUT downloads NOT enabled — manual workflow only "
        "(src 615). Activity & Policy Type codes tied to Sam Brown / Nolan, "
        "blocking automation (src 586). Training in flight (src 346, 347, 348). "
        "Smoke test conducted (src 307); ongoing PTO/cutover sequencing (src 351). "
        "Genuine sequencing blocker, not ownership vacuum.",
        "Push Carrier Mgmt for codes-tied resolution; enable downloads on KC1.",
        [(48, "supporting", False), (90, "supporting", False),
         (243, "supporting", False), (305, "supporting", False),
         (307, "primary", True), (340, "supporting", False),
         (346, "primary", True), (347, "primary", True),
         (348, "primary", True), (351, "primary", True),
         (355, "supporting", False), (586, "primary", True),
         (602, "supporting", False), (607, "supporting", False),
         (609, "supporting", False), (615, "primary", True),
         (616, "supporting", False)],
    ),

    # ---- DNS migration — Roper-paused, Sequencing -------------------------
    (
        86, "DNS/Registrar migration + domain admin",
        "In Progress", "John Seckner (NFP) / Roper",
        "explicit", "high", "Sequencing",
        "Roper paused 04/23 due to email-outage risk during client work crunch "
        "(src 494, 511, 520, 593). Right call — staged async work continues; "
        "TrustSPI / SignatureAdviser / SignatureAdvisor.com queued for export. "
        "NOT an Ownership Vacuum — clear owner, deliberate timing.",
        "Send DNS export to Seckner async; revisit standing 1:1 post-Epic.",
        [(494, "primary", True), (511, "primary", True),
         (520, "primary", True), (593, "supporting", True),
         (652, "supporting", False)],
    ),

    # ---- AI Strategy / Gaya ----------------------------------------------
    (
        82, "AI Strategy deep dive + Gaya pilot",
        "In Progress", "Mark Rieder / Katherine Minami / Roper",
        "explicit", "high", "On Track",
        "AI strategy + technology roadmap discussed on 04/01 NFP team meeting "
        "(src 356).",
        "Schedule Gaya pilot scoping with Rieder/Minami.",
        [(356, "primary", True)],
    ),

    # ---- CanopyConnect ----------------------------------------------------
    (
        83, "CanopyConnect credentials",
        "In Progress", "Josh Zacher → Roper",
        "explicit", "high", "On Track",
        "Discovery covered on 03/27 NFP team meeting; Roper noted pricing "
        "favorable (src 341).",
        "Receive credentials from Josh Zacher.",
        [(341, "primary", True)],
    ),

    # ---- Email migration ETL milestones (carry baseline forward) ---------
    (101, "Email system migration to @nfp.com", "Waiting", "NFP Tech",
     "mentioned", "medium", "Sequencing",
     "Sequenced behind DNS migration pause and Epic hypercare.",
     "Reactivate after DNS export delivered to Seckner.", []),
    (102, "Office integration (conduct)", "Waiting", "NFP Tech",
     "mentioned", "medium", "Sequencing",
     "Sequenced w/ email migration.",
     "Carry forward; no action this week.", []),
    (89, "Copilot license", "Not Started", "Roper",
     "explicit", "medium", "On Track",
     "No new evidence this cycle.",
     "Request license at next NFP IT touchpoint.", []),

    # ---- Day in the Life --------------------------------------------------
    (48, '"Day in the life" sessions', "In Progress", "Roper / Keith Clemons (NFP)",
     "explicit", "high", "On Track",
     "Keith Clemons blocked Tue 04/21 11am Teams session w/ recording (src 652). "
     "Day-in-the-life follow-up Airtable deep dive logged 04/21 (src 349).",
     "Complete recorded session; share artifacts.",
     [(349, "supporting", True), (652, "primary", True)]),

    # ---- Carry-forward of remaining baseline rows w/o new evidence -------
    (33, "@NFP email addresses creation", "Complete", "Roper",
     "explicit", "high", "On Track", "Closed in baseline.", "None.", []),
    (34, "Adjustments on legacy email system to avoid spam", "Complete", "NFP Tech",
     "mentioned", "low", "On Track", "Closed in baseline.", "None.", []),
    (38, "Ninjio Launch", "Complete", "NFP Tech",
     "mentioned", "low", "On Track", "Closed in baseline.", "None.", []),
    (39, "Ninjio Training Period", "Complete", "Roper",
     "mentioned", "low", "On Track", "Closed in baseline; ongoing episodes (src 551).",
     "None.", [(551, "supporting", False)]),
    (40, "Ninjio Training Completed", "Complete", "Roper",
     "mentioned", "low", "On Track", "Closed in baseline.", "None.", []),
    (41, "Email System Migration (TBC)", "Not Started", "NFP Tech",
     "mentioned", "low", "Sequencing",
     "TBC; sequenced after DNS.", "Hold.", []),
    (42, "Email domain change to @nfp.com (TBC)", "Not Started", "NFP Tech",
     "mentioned", "low", "Sequencing", "TBC.", "Hold.", []),
    (43, "Email Migration Hypercare", "Not Started", "NFP Tech",
     "mentioned", "low", "Sequencing", "TBC.", "Hold.", []),
    (44, "Conduct Office Integration (TBC)", "Not Started", "NFP Tech",
     "mentioned", "low", "Sequencing", "TBC.", "Hold.", []),
    (45, "Hypercare", "Not Started", "NFP Tech",
     "mentioned", "low", "Sequencing", "TBC.", "Hold.", []),
    (46, "Post-IT Integration Training (Acadame)", "Not Started", "NFP Tech",
     "mentioned", "low", "On Track", "TBC.", "Hold.", []),
    (47, "Phone Migration", "Complete", "NFP Tech",
     "mentioned", "low", "On Track", "Closed in baseline.", "None.", []),

    # ---- NEW MILESTONE A: Workday HCM go-live -----------------------------
    (
        None,
        "Workday HCM go-live June 29 (HRIS migration, cross-function w/ HR)",
        "In Progress", "NFP HRIS / Workday team",
        "mentioned", "medium", "On Track",
        "Corporate-wide rollout announced 04/14 (src 193); reinforced on Central "
        "Region team meeting 04/23 (src 352). Cross-function w/ HR — Roper as "
        "downstream consumer, not owner.",
        "Watch for SPI-team enrollment training schedule.",
        [(193, "primary", True), (352, "primary", True),
         (802, "supporting", False), (845, "supporting", False),
         (927, "supporting", False)],
    ),

    # ---- NEW MILESTONE B: Agency Cybersecurity (NY DFS) ------------------
    (
        None,
        "Agency Cybersecurity (NY DFS 23 NYCRR 500) annual renewal",
        "In Progress", "Roper / Lisa",
        "explicit", "high", "Time-Critical",
        "Annual compliance filing due 04/15/2026 per Lisa via Idaho/licenses email "
        "(src 116). NFP IT delivers underlying controls (Brandon/Tracy stack); "
        "Roper owns the filing.",
        "File on dfs.ny.gov compliance portal before 04/15.",
        [(116, "primary", True), (816, "supporting", False)],
    ),
]


def main():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    # Wipe + re-insert Technology rows so this is reproducible
    cur.execute("DELETE FROM milestone_evidence WHERE milestone_key IN "
                "(SELECT milestone_key FROM current_milestones WHERE function = ?)",
                (FUNCTION,))
    cur.execute("DELETE FROM current_milestones WHERE function = ?", (FUNCTION,))

    written = 0
    problem_counts = Counter()
    owner_counts = Counter()
    stuck = []

    for (baseline_row, text, status, owner, owner_basis, owner_conf,
         problem_type, notes, next_action, evidence) in MILESTONES:

        key = mkey(text)

        # Pull start/finish from baseline if linked
        start_date, finish_date, priority = None, None, None
        if baseline_row is not None:
            row = cur.execute(
                "SELECT start_date, finish_date, priority FROM baseline_milestones "
                "WHERE row_num = ?", (baseline_row,)).fetchone()
            if row:
                start_date, finish_date, priority = row

        cur.execute("""
            INSERT INTO current_milestones
              (milestone_key, baseline_row, function, primary_text, status,
               start_date, finish_date, notes_apr26, next_action,
               owner, owner_basis, owner_confidence, priority,
               problem_type, eval_status, generated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(milestone_key) DO UPDATE SET
              baseline_row = excluded.baseline_row,
              function = excluded.function,
              primary_text = excluded.primary_text,
              status = excluded.status,
              notes_apr26 = excluded.notes_apr26,
              next_action = excluded.next_action,
              owner = excluded.owner,
              owner_basis = excluded.owner_basis,
              owner_confidence = excluded.owner_confidence,
              problem_type = excluded.problem_type,
              eval_status = excluded.eval_status,
              generated_at = excluded.generated_at
        """, (key, baseline_row, FUNCTION, text, status, start_date, finish_date,
              notes, next_action, owner, owner_basis, owner_conf, priority,
              problem_type, "reconciled", GENERATED_AT))
        written += 1
        problem_counts[problem_type] += 1
        owner_counts[owner] += 1
        if "stuck" in problem_type.lower():
            stuck.append((text, owner, next_action))

        seen = set()
        for sid, weight, cited in evidence:
            if sid in seen:
                continue
            seen.add(sid)
            try:
                cur.execute("""
                    INSERT INTO milestone_evidence
                      (milestone_key, source_item_id, weight, cited_in_notes)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(milestone_key, source_item_id) DO UPDATE SET
                      weight = excluded.weight,
                      cited_in_notes = excluded.cited_in_notes
                """, (key, sid, weight, 1 if cited else 0))
            except sqlite3.IntegrityError:
                pass

    conn.commit()

    print(f"WRITTEN: {written} milestones")
    print(f"PROBLEM_TYPE: {dict(problem_counts)}")
    print("OWNER:")
    for o, n in owner_counts.most_common():
        print(f"  {n:2d}  {o}")
    print("STUCK:")
    for t, o, na in stuck:
        print(f"  - {t}  [{o}]  next: {na}")

    conn.close()


if __name__ == "__main__":
    main()
