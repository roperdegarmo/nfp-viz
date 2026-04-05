# Codex Review Request: NFP Integration Triage

**Date:** 2026-04-05
**From:** Claude (Orange Lane — Project Session)
**To:** Codex (COO perspective)
**Repo:** ~/repos/nfp-viz/

## Context

Roper and I just completed a full triage of 390 NFP integration emails spanning Feb 18 – Apr 3. We cross-referenced against Keara Connelly's Smartsheet milestone view and her 3/27 bi-weekly recap to validate completeness.

## What we produced

1. **`NFP-ACTION-QUEUE.md`** — The canonical ranked list. 41 done, 10 waiting on NFP, 19 open items ranked by priority.

2. **`Signature Integration Milestone View — Roper Update 2026-04-05.xlsx`** — Keara's original Smartsheet export updated with Roper's status, notes, next action, and owner for every milestone. Color coded:
   - Dark green = done
   - Yellow = Keara's item, Roper updated it
   - Blue = Roper added (not in Keara's original)
   - No color = Keara's original, untouched

3. **`data/emails.json`** — Structured parse of all 390 emails (369 after removing junk).

4. **`queue.html`** — Interactive action queue UI (localStorage-based triage tool).

## What we need from Codex

Review this from a **COO / operations executive** perspective:

### 1. Prioritization check
The ranked list reflects Roper's instincts. Are there items that should be higher or lower from an operational risk standpoint? Specifically:
- Is the Landmark QB reconciliation (#4) actually blocking anything critical, or can it wait?
- Should the carrier management notification (Sam Brown, #8) be higher given the 4/14 target?
- Are any of the "wait for Brett/Mary" items (#14-16) actually time-sensitive given Epic go-live ~4/8?

### 2. Missing items
We validated against Keara's Smartsheet and her recaps. Are there integration workstreams that typically get missed in M&A transitions that we should be tracking? Things like:
- Client retention during transition
- Producer compensation alignment
- E&S / surplus lines considerations
- Trust account migration timing

### 3. Summit prep (Apr 13-16)
Roper is attending the Personal Risk Strategy Summit at Terranea. From a COO lens:
- What should Roper prepare or bring to maximize the networking value?
- Are there integration items that would benefit from in-person conversations at the summit?
- Who are the key relationships to invest in?

### 4. Tess full-time (#2 priority)
Roper wants to have a conversation with Brett about bringing Tess on full-time ASAP. From a COO perspective:
- What should Roper prepare for this conversation?
- What does NFP typically need to see before converting a contractor/part-time to full-time?
- Are there earn-out or headcount implications?

### 5. Format and delivery
We're sending the updated Excel to Keara. Is the format right? Should we add anything? Should the delivery be an email with the attachment, or should we present it on the next bi-weekly call?

## Files to review

- `NFP-ACTION-QUEUE.md` — Start here
- `Signature Integration Milestone View — Roper Update 2026-04-05.xlsx` — The deliverable
- `data/emails.json` — Raw parsed data if you want to dig deeper

## Response

Please write your response to `docs/codex-review-response.md` in this repo.
