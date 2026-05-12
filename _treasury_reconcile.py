#!/usr/bin/env python3
"""Treasury reconcile pass — writes 5 baseline + 4 new milestones to current_milestones,
plus milestone_evidence cites. Suppresses pre-acquisition payroll per directive."""
import sqlite3, hashlib, datetime

DB = "/Users/roperdegarmo/repos/nfp-integration/diagnostic.db"
NOW = datetime.datetime.now().isoformat(timespec="seconds")
FN  = "05. Treasury"

def mkey(text: str) -> str:
    norm = " ".join(text.lower().strip().split())
    return hashlib.sha256(f"05. treasury|{norm}".encode()).hexdigest()[:16]

# ---- SUPPRESSED source_item_ids (pre-acquisition payroll: roper-personal bonuses)
SUPPRESS = {70, 87, 108}

# ---- Milestone definitions ------------------------------------------------------------
# Baseline 5 first (carry forward baseline rows)
baseline = [
    dict(
        baseline_row=62,
        primary_text="Banking Assessment",
        status="Complete",
        owner="Ryan Mediate",
        owner_basis="explicit",
        owner_confidence="high",
        problem_type=None,
        notes="Pre-close banking assessment / wire mechanics complete. $25k cap on Landmark legacy account confirmed [src 6, 34]; balance snapshots provided to outside counsel [src 9, 35]; Landmark confirmed as sole business account [src 38]; funds-flow + wire form delivered [src 21]; closing wires initiated and confirmed by NFP Treasury via Aon channels [src 397, 402, 403].",
        next_action=None,
    ),
    dict(
        baseline_row=63,
        primary_text="Creation of Wells Fargo Accounts (if needed)",
        status="Complete",
        owner="Keara Rodriguez",
        owner_basis="implied",
        owner_confidence="medium",
        problem_type=None,
        notes="Not needed per Keara recap (baseline notes_apr14). No new evidence in clustering pass.",
        next_action=None,
    ),
    dict(
        baseline_row=64,
        primary_text="Closing selected legacy bank accounts",
        status="Open",
        owner="Roper DeGarmo",
        owner_basis="implied",
        owner_confidence="medium",
        problem_type="ownership_vacuum",
        notes="Per baseline 4/10: one legacy account remains, slated to close as Wells Fargo transition progresses. No clustering evidence advanced this in the reconcile window — workstream stalled while NFP banking platform migration is TBC.",
        next_action="Confirm with NFP Treasury (Rajulla) which legacy account is targeted for closure and the dependency on Wells Fargo / NFP banking migration.",
    ),
    dict(
        baseline_row=65,
        primary_text="Addition of NFP signatory representative on legacy account (if applicable)",
        status="Complete",
        owner="Rajulla Nadar",
        owner_basis="explicit",
        owner_confidence="high",
        problem_type=None,
        notes="NFP Accounting intros opened the workstream [src 46]; NFP Treasury formally requested adding Caleb Noel + others as signers on Landmark [src 47]; Crystal confirmed three NFP signers added [src 67]; Rajulla acknowledged [src 68]. Signer addition is structurally complete — but see new milestone on portal access (signers without portal = ownership vacuum).",
        next_action=None,
    ),
    dict(
        baseline_row=66,
        primary_text="Migration to Wells Fargo / NFP Banking Platform (TBC)",
        status="Open",
        owner=None,
        owner_basis=None,
        owner_confidence="low",
        problem_type="ownership_vacuum",
        notes="No clustering evidence in reconcile window. Migration to NFP banking platform remains TBC; in the interim Roper continues to operate Landmark on NFP's behalf (see new milestones B and C).",
        next_action="NFP Treasury to confirm migration plan and target date; until then Landmark stays the de facto operating bank.",
    ),
]

# New 4 (per directive A/B/C/D) — owner_candidate, status_signal pulled from clustering
new_ms = [
    dict(  # A
        primary_text="Open new SPI business checking at Landmark post-close (Roper + Rachel + Danielle Williams; $50k transferred)",
        status="Complete",
        owner="Danielle Williams",
        owner_basis="explicit",
        owner_confidence="high",
        problem_type=None,
        notes="Post-close Roper + Rachel opened a separate Landmark business checking with Danielle Williams; Nick Border handled docs; Rachel + Roper provided DLs; Danielle confirmed account opened with $50k transferred [src 175, 179, 180, 191, 192, 203, 204]. Distinct from acquired/legacy account NFP now owns — this is SPI-residual / go-forward.",
        next_action=None,
        evidence=[(175,"high",1),(179,"medium",0),(180,"medium",0),(191,"medium",0),(192,"medium",0),(203,"high",1),(204,"low",1)],
    ),
    dict(  # B
        primary_text="NFP Treasury portal access to Landmark for Rajulla/Donna/Jessly",
        status="Stuck",
        owner="Rajulla Nadar",
        owner_basis="explicit",
        owner_confidence="high",
        problem_type="ownership_vacuum",
        notes="OWNERSHIP VACUUM. Baseline 65 closed (signers added) but NFP Treasury still has no portal access weeks later — Roper is operating the bank for NFP. Rajulla coordinating well; gap is on NFP side. Crystal handed off bank-question routing to Roper post-departure [src 169]; Rajulla repeatedly waiting on Roper for balances [src 170, 176]; Roper himself locked out / questioning why he's still operating the bank [src 178]; Rajulla confirms signers exist but no portal [src 182]; bottleneck illustrated by Roper's travel + password resets [src 183, 185, 188, 190, 195]; Roper escalates asking who go-forward NFP contact is [src 197, 201]; Rajulla defines the three NFP users (Rajulla/Donna/Jessly) [src 205]; Crystal loops Rajulla with Nick Border at Landmark [src 206, 207]; signer-addition wrap [src 208]; Rajulla provides Nick view-only e-statement details [src 231]; Nick sends DocuSign for the three NFP users [src 232, 233]. Rajulla is not the blocker — the access workflow has been crawling for weeks.",
        next_action="Track DocuSign completion for Rajulla/Donna/Jessly view-only e-statement access at Landmark (Nick Border initiated [src 232]); once live, route bank-balance requests off Roper.",
        evidence=[(169,"high",1),(170,"high",1),(171,"medium",1),(176,"high",1),(178,"high",1),(182,"high",1),(183,"medium",1),(185,"medium",1),(188,"medium",1),(190,"low",1),(195,"medium",1),(197,"medium",1),(201,"high",1),(205,"high",1),(206,"high",1),(207,"low",1),(208,"low",1),(231,"high",1),(232,"high",1),(233,"low",1)],
    ),
    dict(  # C
        primary_text="Monthly bank statement + commission delivery to Mary Bamford / NFP accounting",
        status="Open",
        owner="Roper DeGarmo",
        owner_basis="explicit",
        owner_confidence="high",
        problem_type="ownership_vacuum",
        notes="OWNERSHIP VACUUM. Recurring close cycle Roper still operates as books/cash-source for NFP. February month-end: Mary Bamford asks for outstanding items blocking QBO entries [src 63, 133]; Jenny De Cicco (RubinBrown) confirms interim accounting + asks Roper to undo 2/17 Landmark recon [src 137]; Jenny coordinates with Mary on sale accounting [src 139]; Jenny explicitly questions why NFP is not absorbing the accounting [src 142, 143] (Disputed). March cycle: Roper agrees to send March Landmark statement + un-reconcile [src 145, 159]; sends March statement [src 160]; Mary follows with more requests [src 161]; Roper asks Mary to be specific about doc/QBO needs [src 274] (Stuck). Drive folder access for deposits + commission reports [src 199]; Mary drilling on Progressive [src 362], AIG PCG [src 364], Landmark mobile deposit source docs [src 365]. Cross-cuts integration recap [src 294, 1446] and QBO admin access struggle [src 333].",
        next_action="Define and document the monthly close packet (statement + commission reports + source docs) with Mary B; tie un-reconcile cleanup to Jenny De Cicco; escalate transfer of accounting ownership to NFP via Mary Mullen recap thread.",
        evidence=[(63,"high",1),(133,"high",1),(137,"high",1),(139,"medium",1),(142,"high",1),(143,"medium",1),(145,"high",1),(159,"medium",1),(160,"high",1),(161,"high",1),(199,"medium",1),(274,"high",1),(294,"medium",1),(333,"medium",1),(362,"medium",1),(364,"medium",1),(365,"medium",1),(1446,"medium",1)],
    ),
    dict(  # D
        primary_text="SPI vendor onboarding into Aon Coupa supplier system",
        status="Stuck",
        owner="Logan Christianson",
        owner_basis="explicit",
        owner_confidence="high",
        problem_type="nfp_slow",
        notes="Logan Christianson (NFP) launched Coupa setup 3/18 to route SPI vendor expenses through Coupa rather than personal/operating account [src 117]; follow-up 3/24+ remains unanswered — NFP slow on vendor onboarding follow-through [src 156].",
        next_action="Roper to send Logan the consolidated SPI vendor list + W-9s; Logan to push Coupa team for supplier IDs.",
        evidence=[(117,"high",1),(156,"high",1)],
    ),
]

# Baseline evidence map (source_item_id, weight, cited_in_notes) per baseline_row
baseline_evidence = {
    62: [(6,"high",1),(9,"medium",1),(21,"high",1),(34,"high",1),(35,"high",1),(38,"high",1),(397,"high",1),(402,"high",1),(403,"high",1)],
    63: [],
    64: [],
    65: [(46,"medium",1),(47,"high",1),(67,"high",1),(68,"medium",1)],
    66: [],
}

# ---- Write --------------------------------------------------------------------------
con = sqlite3.connect(DB)
con.execute("PRAGMA foreign_keys = ON")
cur = con.cursor()

UPSERT = """
INSERT INTO current_milestones
  (milestone_key, baseline_row, function, primary_text, status,
   notes_apr26, next_action, owner, owner_basis, owner_confidence,
   problem_type, generated_at)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
ON CONFLICT(milestone_key) DO UPDATE SET
  baseline_row=excluded.baseline_row,
  function=excluded.function,
  primary_text=excluded.primary_text,
  status=excluded.status,
  notes_apr26=excluded.notes_apr26,
  next_action=excluded.next_action,
  owner=excluded.owner,
  owner_basis=excluded.owner_basis,
  owner_confidence=excluded.owner_confidence,
  problem_type=excluded.problem_type,
  generated_at=excluded.generated_at
"""

EV_UPSERT = """
INSERT OR IGNORE INTO milestone_evidence
  (milestone_key, source_item_id, weight, cited_in_notes)
VALUES (?, ?, ?, ?)
"""

written = 0

for m in baseline:
    key = mkey(m["primary_text"])
    cur.execute(UPSERT, (
        key, m["baseline_row"], FN, m["primary_text"], m["status"],
        m["notes"], m["next_action"], m["owner"], m["owner_basis"],
        m["owner_confidence"], m["problem_type"], NOW,
    ))
    for sid, w, cited in baseline_evidence.get(m["baseline_row"], []):
        if sid in SUPPRESS: continue
        cur.execute(EV_UPSERT, (key, sid, w, cited))
    written += 1

for m in new_ms:
    key = mkey(m["primary_text"])
    cur.execute(UPSERT, (
        key, None, FN, m["primary_text"], m["status"],
        m["notes"], m["next_action"], m["owner"], m["owner_basis"],
        m["owner_confidence"], m["problem_type"], NOW,
    ))
    for sid, w, cited in m["evidence"]:
        if sid in SUPPRESS: continue
        cur.execute(EV_UPSERT, (key, sid, w, cited))
    written += 1

con.commit()

# ---- Report -------------------------------------------------------------------------
print(f"Milestones written: {written}")
print()
print("problem_type distribution:")
for row in cur.execute("SELECT COALESCE(problem_type,'(none)') p, COUNT(*) FROM current_milestones WHERE function=? GROUP BY 1 ORDER BY 2 DESC", (FN,)):
    print(f"  {row[0]}: {row[1]}")
print()
print("owner distribution:")
for row in cur.execute("SELECT COALESCE(owner,'(unassigned)') o, COUNT(*) FROM current_milestones WHERE function=? GROUP BY 1 ORDER BY 2 DESC", (FN,)):
    print(f"  {row[0]}: {row[1]}")
print()
print("Stuck items:")
for row in cur.execute("SELECT primary_text, owner, problem_type FROM current_milestones WHERE function=? AND status='Stuck'", (FN,)):
    print(f"  - [{row[2]}] {row[0]} (owner: {row[1]})")
print()
print("Status distribution:")
for row in cur.execute("SELECT status, COUNT(*) FROM current_milestones WHERE function=? GROUP BY 1 ORDER BY 2 DESC", (FN,)):
    print(f"  {row[0]}: {row[1]}")
print()
ev_count = cur.execute("SELECT COUNT(*) FROM milestone_evidence me JOIN current_milestones cm ON me.milestone_key=cm.milestone_key WHERE cm.function=?", (FN,)).fetchone()[0]
print(f"Evidence rows: {ev_count}")
print(f"Suppressed source_items (out-of-scope payroll): {sorted(SUPPRESS)}")
con.close()
