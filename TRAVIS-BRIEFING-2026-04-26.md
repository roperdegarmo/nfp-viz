# NFP Integration Diagnostic — Travis Briefing

**Date:** 2026-04-26 (Sunday evening)
**Prepared by:** Roper DeGarmo with Claude
**For:** Travis Carpenter, in advance of Monday 4/27 strategy session and Brett Woodward 3pm
**Length:** Long. Read TL;DR first, then dive in by section.
**Companion data:**
- Refreshed milestone view: `Signature Integration Milestone View — Roper Update 2026-04-26.xlsx`
- Full evidence base: `~/repos/nfp-integration/diagnostic.db` (Datasette browseable)
- This document embeds load-bearing emails and transcripts so you don't need the database to read them.

---

## TL;DR (60 seconds)

We rebuilt the integration milestone view from scratch using every email, calendar event, transcript, and Airtable record touching NFP since the 02/17 close. The 4/14 baseline had 95 milestones; the refreshed view has 137 (46 new). We found three things:

1. **Sequencing is partly working.** NFP can do the client-work side. Epic + service center will absorb the policy book once the technical preconditions land (codes tied, downloads flowing, service center picking up cases). Tech function shows zero ownership-vacuum items — Brandon Jackson + Tracy McClain + John Seckner deliver. AmEx/Concur runs (Jackie Searles). Workday GL is created and mapped. AIG > PCS auto-downloads went live 2/27.

2. **Ownership of the back-office is a vacuum.** 25 milestones tagged Ownership Vacuum across the audit. The Bamford Finance pattern is the loudest — rows 53/54/55/56/59/60/61 from the 4/14 baseline are all confirmed Stuck because she keeps re-asking through 4/24 for the same things. Treasury is "the loudest operating-bank-for-NFP surface." Carrier intel (AIG Collector Auto Re-Class, Chubb/PCG bulletins) doesn't get routed to Roper proactively — has to be requested.

3. **The dark variant: NFP needs the work done but explicitly refused to absorb it.** The agency entity licenses are the cleanest case. NFP needs them active for the 6-year shell-life (rolling broker-of-record transitions + E&O tail). Lisa Black (NFP Licensing Director) told Roper on 03/04: "NFP will not be handling any of the agency licenses." 46 entity licenses across states. Same Lisa Black + same RegEd vendor handles individual producer licenses cleanly — proving the agency-license vacuum is a deliberate scope decision, not a process failure.

**Roper appears as Owner on 33+4 of 137 milestones (27%)** — most of which should be NFP. That's the diagnostic in one number.

### Recommendation for Brett 3pm Monday

Lead with what's working (sequencing thesis), then ask for **names**:

> "On the client-work side, I trust the sequencing. Codes tied, downloads, service center — I see that path working. What I need from you today is names on the back-office side. Who at NFP specifically owns mail for the acquired SPI entity? Who owns QuickBooks? Who owns licensing for the entity-level renewals? When I get pinged about a May license renewal I don't recognize, who is the right person to forward it to? If you can't name them, the back-office handoff hasn't been planned, just assumed."

**Brett response → action**:
- Names specific people / commits to back-office takeover with dates → Plan A confirmed. Travis stays in wings.
- Vague / pushes to Mary or Keara / treats as producer-comfort → Travis Plan B email goes Tuesday morning.
- Aggressive / defensive → Plan C decisions about compensation/role/exit.

---

## How this document is organized

1. TL;DR (above)
2. The Diagnostic Method — what we ingested, how we processed
3. Quantitative Findings — full numbers
4. The Three Theses — sequencing / ownership vacuum / dark variant
5. The Wedge: Agency Licenses — cleanest dark-variant case (with full smoking-gun embeds)
6. Function-by-Function Audit — all 9 Functions with milestones
7. Smoking Gun Emails (Full Text) — load-bearing email bodies embedded
8. Smoking Gun Transcripts (Full Text) — load-bearing transcript chunks embedded
9. The Brett Play — Monday 3pm tactical guide
10. What I Want From You — push back on
11. Appendix: data sources & methodology

---

## 2. The Diagnostic Method

### Sources ingested

| Source | Volume | Filter | What we got |
|---|---|---|---|
| Email archive | 1,397 emails | NFP-domain participants since 2026-02-01 | All NFP-touching email with snippets; full bodies hydrated for cited items |
| Calendar | 74 events | NFP-attended or NFP-keyword | Bi-weekly Integration Reviews, Summit, coordination calls |
| Transcripts | 87 recordings | NFP-tagged or integration keyword | Internal NFP team meetings, Travis coaching, Roper-Crystal sessions, Epic training, agency-license discussions |
| Bamford screenshots | 4 PNGs / 15 line items | OCR'd via vision | Bamford's 04/24 red-line of 15 specific source documents required by 5/1 |
| Repo baseline | 108 rows (04/14 xlsx) | Drop color-legend | Roper's last manual milestone pass |

**Total source items: 1,573.**

### Pipeline

1. **Extract** all sources into a working SQLite DB (`diagnostic.db`).
2. **Cluster** each source item against the 95 baseline milestones using LLM (Claude Sonnet 4.5 via parallel subagents). Each item gets `linked` / `new_milestone` / `noise` plus owner attribution (`owner_candidate`, `owner_basis`, `owner_confidence`).
3. **Reconcile** each milestone using all linked evidence. Produce final Status / Owner / Notes / Problem Type / Next Action per milestone.
4. **Generate** the refreshed xlsx and this briefing.

### Key methodological choices

- **Baseline is hypothesis, not authority.** Where evidence dated after 04/14 contradicts baseline status, evidence wins.
- **Owner attribution split into 3 fields.** This separates "who's named in the email" from "who's actually delivering the work."
- **Bamford pattern recognition.** When Bamford's "ownership" is *demanding from Roper* (asking for documents she should have access to herself), we tag the milestone as **Ownership Vacuum** with owner=Roper. Bamford is the demand source, not the delivery owner.
- **Suppressions:** Pre-acquisition payroll wires for Crystal & Tess (Roper-personal bonus) and Roper's 2025 personal tax return (out of NFP scope) excluded.

---

## 3. Quantitative Findings

### Per-function counts

| Function | Total | New | Ownership Vacuum | Stuck |
|---|---|---|---|---|
| 01. HR | 24 | 5 | 2 | 1 |
| 02. Marketing | 19 | 2 | 0 | 1 |
| 03. Technology | 27 | 2 | 0 | 0 |
| 04. Finance | 18 | 7 | 10 | 8 |
| 05. Treasury | 9 | 4 | 4 | 2 |
| 07. Risk Management | 4 | 2 | 2 | 1 |
| 08. Carrier Management | 17 | 12 | 3 | 0 |
| 09. Licensing & Registrations | 3 | 3 | 2 | 2 |
| 10. Region/Sales/Ops | 16 | 8 | 1 | 1 |

**Total: 137 milestones (46 new, 25 ownership vacuum, 16 stuck).**

### Status distribution

| Status | Count |
|---|---|
| Complete | 46 |
| Open | 29 |
| Stuck | 16 |
| In Progress | 16 |
| Waiting | 14 |
| Not Started | 12 |
| Active | 4 |

### Owner distribution (top 15)

| Owner | Count |
|---|---|
| Roper | 32 |
| unassigned | 12 |
| NFP Tech | 11 |
| Mary Mullen | 6 |
| Jackie Searles | 5 |
| Susan Clifford | 4 |
| Roper DeGarmo | 4 |
| Rajulla Nadar | 4 |
| NFP Marketing | 4 |
| Teresa Wharton | 3 |
| NFP HR (corporate) | 3 |
| Mary Bamford | 3 |
| Andria Griffin | 3 |
| Sam Brown | 2 |
| Ryan Mediate | 2 |

**Roper appears as Owner on ~37 of 137 (27%). That is the load-bearing diagnostic.**

### All Stuck items (16)

| Function | Milestone | Owner |
|---|---|---|
| 01. HR | HSA accounts (Optum) | Andria Griffin |
| 02. Marketing | Define client communication / letters | Roper |
| 04. Finance | Closing balance sheet review and upload | Roper |
| 04. Finance | Month end and finance & accounting processes onboarding | Mary Bamford |
| 04. Finance | Upload month 1 closing activity | Roper |
| 04. Finance | Upload month 2 closing activity | Roper |
| 04. Finance | AmEx statement — 3/20 payment for Mary Bamford | Roper |
| 04. Finance | Expense descriptions — Acumen KS $1,250 + OgleTree Deakins $170.10 | Roper |
| 04. Finance | Deposit support — carrier statements for March | Roper |
| 04. Finance | Landmark Bank portal access provisioning for NFP Treasury | Rajulla Nadar |
| 05. Treasury | NFP Treasury portal access to Landmark for Rajulla/Donna/Jessly | Rajulla Nadar |
| 05. Treasury | SPI vendor onboarding into Aon Coupa supplier system | Logan Christianson |
| 07. Risk Management | Operational E&O exposure from manual post-close service workflow (no AMS, no service center) | Roper DeGarmo |
| 09. Licensing & Registrations | Agency entity license renewals during 6-year SPI shell-life — NFP needs them active for rolling BoR + E&O tail, refused to absorb administrative burden | Roper |
| 09. Licensing & Registrations | Roper KS Surplus Lines license renewal due 5/1/2026 — unrecognized May renewal sitting in the seam between NFP/RegEd individual scope and agency/state-line scope | Unassigned |
| 10. Region/Sales/Ops | Susan Clifford — ALT report / AI agent | Susan Clifford |

### All dark-variant Ownership Vacuum items (NFP needs, Roper or unassigned owns)

These are the items where NFP either explicitly refused to absorb the work or quietly routed it back to Roper without naming a successor. The pattern is structural, not personal.

| Function | Milestone | Owner |
|---|---|---|
| 01. HR | Vendor onboarding into Aon Coupa supplier system | unassigned |
| 04. Finance | Closing balance sheet review and upload | Roper |
| 04. Finance | Upload month 1 closing activity | Roper |
| 04. Finance | Upload month 2 closing activity | Roper |
| 04. Finance | AmEx statement — 3/20 payment for Mary Bamford | Roper |
| 04. Finance | Expense descriptions — Acumen KS $1,250 + OgleTree Deakins $170.10 | Roper |
| 04. Finance | Deposit support — carrier statements for March | Roper |
| 04. Finance | Bamford 4/24 SharePoint source-doc demand list — 15 specific transactions by 5/1 | Roper |
| 04. Finance | Concur T&E onboarding for Roper specifically | unassigned |
| 04. Finance | Agency entity license renewals during 6-year SPI shell-life (46 entity licenses across sta | Roper |
| 05. Treasury | Closing selected legacy bank accounts | Roper DeGarmo |
| 05. Treasury | Migration to Wells Fargo / NFP Banking Platform (TBC) | unassigned |
| 05. Treasury | Monthly bank statement + commission delivery to Mary Bamford / NFP accounting | Roper DeGarmo |
| 07. Risk Management | Determine agency license retention requirement under E&O retroactive coverage / 6-year ERP | Roper DeGarmo |
| 07. Risk Management | Operational E&O exposure from manual post-close service workflow (no AMS, no service cente | Roper DeGarmo |
| 09. Licensing & Registrations | Agency entity license renewals during 6-year SPI shell-life — NFP needs them active for ro | Roper |
| 09. Licensing & Registrations | Roper KS Surplus Lines license renewal due 5/1/2026 — unrecognized May renewal sitting in  | Unassigned |

---

## 4. The Three Theses

### Thesis 1: Sequencing is partly working

NFP can do the client-work side. The technical preconditions are in motion and several functions show NFP delivering cleanly.

**Counter-examples that prove NFP CAN coordinate:**
- **Technology** function: 27 milestones, **zero Ownership Vacuum**. Brandon Jackson + Tracy McClain own email security cleanly. John Seckner owns DNS planning. NFP HRIS owns the Workday HCM go-live. Roper paused DNS migration 04/23 due to email outage risk during client work crunch — that's a sequencing call (right call), not a vacuum.
- **AmEx + Concur**: Jackie Searles owns from NFP. Cards issued, Concur went live 4/2.
- **Workday GL Creation + GL Mapping** (Finance rows 51, 52): both Resolved.
- **AIG > PCS One auto-downloads** went live 02/27 (Teresa Wharton). One half of the codes-tied dependency is real.
- **E&O Tail / ERP procurement**: Christopher Sam authorized, Riana Sherwood chased, Barb Wise (KAIA) executed. Cleanly tracked NFP-side. Counter-example to the vacuum.
- **Marketing**: Alma Ko owns client comms cleanly. Most of the 17 Marketing milestones are sequencing-bound on June cutover (correct sequencing, not vacuum).

**Where sequencing is genuinely stuck (not a vacuum):**
- **Epic KC1 branch** is live (4/17) but downloads NOT enabled — blocked on Sam Brown / Nolan finishing AIG/PURE code-tying. That's real sequencing dependency.
- **Berkley One + Chubb code decisions** still open, Brad Millican working it.
- **PURE/MetLife/Hagerty Epic policy entry rules** unresolved (Amy Hill).
- **!ALT / Download Suspense** is the chronic downstream queue (Susan Clifford) once codes ARE tied.

### Thesis 2: Ownership of the back-office is a vacuum

Every back-office process that used to have a clear owner (Roper, Crystal, the Philippines team) needs a new clear owner at NFP, and many don't have one. NFP's structure is functional silos (Bamford for accounting, Treasury for cash, RegEd for individual licenses) — none of which sees "the back office of the acquired SPI entity" as a whole. So when something doesn't fit cleanly into a silo, it bounces back to Roper.

**The Bamford pattern** (most concentrated example):
- 04/06: Bamford asks Roper for AmEx 3/20 statement, Acumen + OgleTree expense descriptions, March carrier deposit support.
- 04/14: Roper captures the 3 asks as ⬅️ items in the milestone view (rows 59, 60, 61).
- 04/24: Bamford re-asks the same items, plus 12 more, in her 04/24 SharePoint demand list (15 total). Some are duplicates (Acumen, OgleTree). Others escalate (full carrier deposit support for 8 March transactions).
- 04/26 audit: rows 53/54/55/56/59/60/61 ALL confirmed Stuck. Bamford keeps re-asking what she should already have access to herself.

**Treasury operating-bank-for-NFP pattern:**
- Baseline says signers added (row 65 Complete). Reality: Roper still pulling Landmark balances on demand. NFP Treasury portal access STUCK — Rajulla Nadar coordinating but signers don't have portal credentials. DocuSign workflow finally in motion via Nick Border 4/16.
- Monthly bank statement + commission delivery to Bamford routes through Roper as recurring close cycle. Not a one-time onboarding gap; recurring operational dependency.
- Coupa vendor onboarding launched 3/18 by Logan Christianson; follow-up unanswered through 4/26. Stuck.

**Carrier intel routing:**
- AIG Collector Auto Re-Classification announced on Central Region call 3/27. Mary Mullen forwarded notice to Stephanie Brock. **Roper's producer code was not on the distribution list.** Tess only got the notice 4/7 after explicitly emailing Mary to ask.
- Same pattern on Chubb/PCG DNR + NY hurricane deductible bulletins (Mary Mullen routes selectively).
- BOR/CORG carrier signaling — same family.

NFP is not routing carrier intel to Roper proactively. Three independent evidence chains.

**HR vacuums (smaller but real):**
- HSA accounts (Optum) — Andria Griffin flagged on 3/17 with promise to address 4/6 paycheck. No Optum open-confirmation since. Blocks pre-tax HSA contributions for Roper & Crystal.
- Aon Coupa supplier intake — no NFP-side owner named for SPI vendor onboarding.

### Thesis 3: Dark variant — NFP needs the work but explicitly refused to absorb it

This is a darker variant of Thesis 2. Not "nobody owns it" — "NFP needs it, NFP shouldn't hold the cost, NFP pushed it to Roper anyway."

**Cleanest case: Agency entity licenses.** See Section 5 below for full evidence. NFP needs SPI's 46-state agency licenses active for the rolling broker-of-record transition AND the 6-year E&O tail. Lisa Black explicitly declined NFP responsibility on 03/04. Same Lisa Black + same RegEd vendor handles individual producer renewals cleanly. The agency-license vacuum is a deliberate scope decision, not a process failure.

**Other dark variants:**
- **Bamford's 04/24 SharePoint upload demand** (15 source documents by 5/1): Bamford has accounting firm access to QBO since 2/25. Roper provided AmEx credentials, shared Drive folders for deposits + commission reports. Bamford is *demanding source documents that are already accessible to her* rather than retrieving them. The recurring re-asks (4/06 → 4/14 → 4/24) confirm the pattern.
- **Roper KS Surplus Lines license renewal due 5/1** (the unrecognized May renewal): notice landed at roper.degarmo@nfp.com on 4/15 with 5/1 deadline. NFP/RegEd doesn't claim it (agency-line); Roper doesn't recognize it (didn't initiate). Sitting in the seam between scopes.
- **Operational E&O exposure from manual post-close workflow**: Roper to Caleb 4/21 — "just trying to make sure we don't drop any balls that result in E&O" describing post-close state as 'sketchy.' NFP not coordinating exposure tracking; Roper alone tracking.
- **AIG Collector Auto Re-Classification distribution gap**: Roper's book has exposure, NFP knew about the change before Roper did, Roper had to explicitly ask to be on the distribution list.

### What this trichotomy implies for Brett

If Sequencing is the only thesis: 6-9 months of friction, then it works. Ride it out.

If Ownership Vacuum is the dominant thesis: the integration playbook hasn't been adapted to the back-office of an acquired entity. Solvable with explicit ownership assignment from leadership. Brett can fix it Monday by naming people.

If Dark Variant is real: NFP made deliberate scope decisions to push transferred operational obligations to Roper. That's not a planning failure — it's a deal mechanic. Different conversation. Travis Plan B becomes appropriate.

The data shows all three are present, with Dark Variant being the smallest in count but the most consequential per item.

---

## 5. The Wedge: Agency Licenses

This is the cleanest case for the dark-variant thesis. Walk into Brett with this story.

### Timeline

- **02/17/2026** — NFP closes asset purchase of SPI. Roper retains the LLC for the 6-year E&O tail period.
- **02/27/2026** — Roper, in a Crystal working session, independently flags the coupling: *"a new wrinkle has occurred that we might want to keep licenses open for the agency during the earn-out period when we have to carry E&O coverage over the next 6 years."* (Transcript 120, ~3:11hr mark.)
- **03/04/2026** — Lisa Black (NFP Licensing Director) emails Crystal + Roper with the scope decision: NFP/RegEd will handle individual licenses (Roper, Crystal, Tess). NFP will NOT handle agency licenses or agency cybersecurity filings. Asset purchase scope.
- **03/05/2026** — Roper accepts the void: *"the agency licenses are on me. If they need to be maintained, I'll bring in an outside firm."* (Email id 65.)
- **03/05/2026** — Lisa locks in the rolling tail: agency licenses must stay active *"until all the business written under the licenses has officially expired."*
- **03/18/2026** — Crystal escalates concrete renewals to Roper (Idaho SOS 3/31, NY Cybersec 4/15). Roper notes intention to use RubinBrown's small biz department.
- **04/10/2026** — In an NFP internal HR ops meeting on Concur/AmEx, the agency-license question surfaces in a multi-speaker exchange. Sam Brown confirms broker-of-record updates only happen at policy renewal (rolling). Speaker 3 (Mullen team) acknowledges: *"they should stay open as long as they have active policies on them."* Roper: *"Wouldn't can can we ask for some help on that then? Like, that seems like it's an operations need... I would probably have to hire a third party to do that."* Compliance interest in keeping licenses active surfaces as a shared NFP need. (Transcript 190, chunks 8-9.)
- **04/15/2026** — KS Surplus Lines renewal notice lands at roper.degarmo@nfp.com with 5/1 deadline. Sits in scope-seam — NFP/RegEd doesn't claim it, Roper doesn't recognize it.
- **04/26/2026 (today)** — agency entity license renewal milestone status: **Stuck. Owner: Roper. Problem Type: Ownership Vacuum (Dark Variant).**

### Why this is the wedge

1. NFP needs the agency licenses active (rolling broker-of-record + 6-year E&O tail).
2. NFP explicitly refused to absorb them (Lisa Black 03/04, in writing).
3. The administrative lift is real: 46 entity licenses, multiple state-specific renewal cycles, surplus lines reporting requirements.
4. RegEd already handles individual licenses for NFP — the system to handle agency licenses exists internally; NFP just chose not to extend it to the SPI shell.
5. Cost falls entirely on Roper, who would have to hire a third party (RubinBrown's small biz dept proposed but not engaged).
6. **Same Lisa Black + same RegEd vendor handle individual producer renewals cleanly** (Tess MA P&C in motion, Roper NC auto-renew handled, NY Cybersecurity processed). Counter-example proves it's not a process failure — it's a scope decision.

### Smoking gun: Lisa Black 03/04 (full email body)

**From:** Lisa Black <lblack@nfp.com>
**Date:** 2026-03-05 13:51:32+00
**Subject:** RE: Licenses
**Gmail ID:** 19cbe44ae4a845fb

```
Hi Roper,

I would recommend keeping the licenses active until all the business written under the licenses has officially expired.  I would keep any state licenses active if there are policies still in force.

Lisa Black
Licensing Director
Legal and Compliance
NFP, an Aon company
16150 N. Arrowhead Fountains Center Drive,Suite120 | Peoria, AZ 85382
P: 623.866.4362 | F: 623.217.2469 | lblack@nfp.com<mailto:lblack@nfp.com> | NFP.com
[cid:image001.png@01DCAC6C.7EABB560]



From: Roper DeGarmo <roper@signatureadvisor.com>
Sent: Thursday, March 5, 2026 6:49 AM
To: crystal <crystal@signatureadvisor.com>; Roper DeGarmo <roper.degarmo@nfp.com>; Crystal Stuart <crystal.stuart@nfp.com>; Lisa Black <LBlack@nfp.com>
Subject: RE: Licenses

You don't often get email from roper@signatureadvisor.com<mailto:roper@signatureadvisor.com>. Learn why this is important<https://aka.ms/LearnAboutSenderIdentification>
ATTENTION - EXTERNAL EMAIL - The sender of this email is EXTERNAL to our email system. Do not click links or open attachments unless you recognize the sender and know the content is safe.
Hey Lisa — one more thing on the license front.

Going forward, the agency licenses are on me. If they need to be maintained, I'll bring in an outside firm to handle renewals (likely RubinBrown, who has a division that handles this).

But here's the real question: do I even need to? Since this was an asset purchase and SPI isn't writing new business, is there a requirement to keep agency licenses active? Or can I let them lapse as they come up for renewal? Our E&O has retroactive coverage for prior acts, so I believe we're covered on that side.

Would love your thoughts — or if someone on your compliance team is better suited to weigh in, happy to connect with them.

Roper

Roper C. DeGarmo, Founder
Signature Personal Insurance LLC
Office: 913-904-1881
Cell: 913-210-9054
linkd.in/RoperDeGarmo<https://t.shortwave.com/links/v1/-kMSddA1cJxOjOLEuUB06CUf9L5Jp_qhdZEVorJgsOqo0jJSp9dfG7LAOG3vrMtFLCnEQ7xiEz-xLEOknWu4gD-N_x5PYZACc0nOp2CzlqgeR3mSeKw15RTmxaR3IBA3hcrAVBfSZVmorV_KchWD-oSzs36u_1Mw_9BaLlJXwL0>
SignaturePersonalInsurance.com<https://t.shortwave.com/links/v1/VjQvGqoiPqdfFYFk-MUeDRXwWt4PXCvlWi3TVaHY8OAo08dR-wF-W5fJ2RSlZagBoMU8FqO0XEZARrOCb8uPmv8fxcpsxgipTEV3E3M2doB3IzywRJignYIHM_9jIQYo0MO2upY8NNd5iUVEMlfrcNj_bkOyDyKGYQ7dg3M73No>


On Wed Mar 4, 2026, 07:41 PM GMT, Roper DeGarmo<mailto:Roper@signatureadvisor.com> wrote:
Lisa,

Thanks for laying this out so clearly.

☐ Review and Renew needed Agency Licenses for Signature Personal Insurance LLC.

I'm adding the license transfer details to our master list of transition tasks. Once I have a complete picture, we'll start prioritizing across the board.

If anything comes up that needs immediate attention on my end, just shoot me an email and I'll jump on it. Otherwise, this goes into the work queue for the full project.

Appreciate the help.

Roper

On Wed Mar 4, 2026, 06:41 PM GMT, Lisa Black<mailto:LBlack@nfp.com> wrote:
Thank you Crystal.   Since this was an asset purchase, NFP will not be handling any of the agency licenses or the agency Cyber security filing.   We will be handling the individual licenses, and cyber security(if applicable) for you and Roper.   In a few days, you should receive a welcome email from our licensing vendor RegEd.  The email will instruct you to login to the RegEd app and complete your background questions.  This will ensure that RegEd has all the information they need to handle any licensing needs.

RegEd will usually get the licenses renewed about 30-45 days prior to expiration.  They reach out to you directly if anything is needed.

Please email me or call anytime with questions.


Lisa Black
Licensing Director
Legal and Compliance
NFP, an Aon company
16150 N. Arrowhead Fountains Center Drive,Suite120 | Peoria, AZ 85382
P: 623.866.4362 | F: 623.217.2469 | lblack@nfp.com<mailto:lblack@nfp.com> | NFP.com



From: Crystal Stuart <crystal@signatureadvisor.com<mailto:crystal@signatureadvisor.com>>
Sent: Wednesday, March 4, 2026 10:10 AM
To: Roper DeGarmo <roper.degarmo@nfp.com<mailto:roper.degarmo@nfp.com>>; Crystal Stuart <crystal.stuart@nfp.com<mailto:crystal.stuart@nfp.com>>; Lisa Black <LBlack@nfp.com<mailto:LBlack@nfp.com>>
Subject: Re: Licenses

You don't often get email from crystal@signatureadvisor.com<mailto:crystal@signatureadvisor.com>. Learn why this is important<https://aka.ms/LearnAboutSenderIdentification>
ATTENTION - EXTERNAL EMAIL - The sender of this email is EXTERNAL to our email system. Do not click links or open attachments unless you recognize the sender and know the content is safe.
Hi Lisa,

Please do! 😊

The attached excel file likely gives you more information than you need, as it contains SPI's agency licenses as well, but this should give you a good timeline of what you should be looking for. Coming up soon, I see that Roper's NC license is supposed to automatically renew by 3/31/26 and the NY Cybersecurity requirement is set to be due 4/15/26, which I assume you'll take from here as well?

Let us know if you need any further information or questions, but this should be all inclusive for now—feel free to use if helpful!

Thanks,

Crystal Stuart
Signature Personal Insurance
Fax: (913) 416-9392
www.SignaturePersonalInsurance.com<http://www.signaturepersonalinsurance.com/>

On Wed Mar 4, 2026, 04:08 PM GMT, Lisa Black<mailto:LBlack@nfp.com> wrote:
Hi Crystal and Roper,

Good to meet you last week.  Just wanted to give you this information in writing but there is no rush on licensing at all.

As mentioned in the integration meeting, NFP does partner with RegEd as our licensing vendor.  When you are ready for NFP/RegEd to handle your license renewals, please just let me know and we will get your profile set up.  If anything, license related comes up urgently, please let me know.




Lisa Black
Licensing Director
Legal and Compliance
NFP, an Aon company
16150 N. Arrowhead Fountains Center Drive,Suite120 | Peoria, AZ 85382
P: 623.866.4362 | F: 623.217.2469 | lblack@nfp.com<mailto:lblack@nfp.com> | NFP.com



This e-mail may contain information that is privileged, confidential or protected under state or federal law. If you are not an intended recipient of this email, please delete it, notify the sender immediately, and do not copy, use or disseminate any information in the e-mail. Any tax advice in this email may not be used to avoid any penalties imposed under U.S. tax laws. E-mail sent to or from this e-mail address may be monitored, reviewed and archived.
This e-mail may contain information that is privileged, confidential or protected under state or federal law. If you are not an intended recipient of this email, please delete it, notify the sender immediately, and do not copy, use or disseminate any information in the e-mail. Any tax advice in this email may not be used to avoid any penalties imposed under U.S. tax laws. E-mail sent to or from this e-mail address may be monitored, reviewed and archived.
This e-mail may contain information that is privileged, confidential or protected under state or federal law. If you are not an intended recipient of this email, please delete it, notify the sender immediately, and do not copy, use or disseminate any information in the e-mail. Any tax advice in this email may not be used to avoid any penalties imposed under U.S. tax laws. E-mail sent to or from this e-mail address may be monitored, reviewed and archived.
```

**Why it matters:** This is the explicit scope declination. NFP/RegEd handles individual licenses — agency licenses are SIG's responsibility because asset purchase. The decision is documented in writing.

### Smoking gun: Transcript 190 (04/10) — the realization moment

**Title:** NFP internal HR ops meeting - Concur Amex launched
**Date:** 2026-04-10
**Source:** soundcore-anker, recording id 190, chunks 8-9 (~12-16 min mark)

**Chunk 8:**

```
Speaker 3: well, see, that was the other part. She she asked me a very valid question as to which license in Massachusetts to get, but, of course, they're state specific. So I'm not sure if Massachusetts has personal lines only or

Speaker 3: She asked me who. Like me. Talked to Mary. Yeah. It's property and casualty. Okay. Yes. Good. And and, Tess, is there I I don't I haven't asked you this, so sorry to ask on the call. But do you do you know any idea when the you'd be able to schedule a a testing date?

Speaker 13: Yeah. I can take it any day. So you can take it remotely, and they offer literally twenty four hours a day that you can take it.

Speaker 13: So my goal is to finish studying and take it and pass

Speaker 13: by the end of the month.

Speaker 1: Really great, Seth. I know you. Thank you.

Speaker 0: And I I saw Robert, I think in an email, you had a question about the NTT license.

Speaker 0: Yeah. I think the answer to that, if you have heard already, is that given we didn't acquire the NTT,

Speaker 0: then we won't be able to track down Ragged. So

Speaker 0: so, I guess you need to to track that separately.

Speaker 3: Yeah. I'm gonna have to get with, legal somewhere because I don't I actually

Speaker 3: it seems kinda strange

Speaker 3: that I would keep entity licenses for a Shell LLC.

Speaker 3: I'd be I'm not it's not really the cost because I don't think it costs that much, but it it's a pretty hefty,

Speaker 3: administrative lift to keep 46

Speaker 3: licenses open.

Speaker 0: Yep.

Speaker 0: We are and and and and,

Speaker 0: Sam,

Speaker 0: are we moving all this

Speaker 0: I guess, in the end is, who's the broker of record on the policies now? And are we changing that to NFP and C?

Speaker 6: Yep. We're working to update those to NFP

Speaker 6: and CNN go forward. And,


```

**Chunk 9:**

```
Speaker 0: I guess, in the end is, who's the broker of record on the policies now? And are we changing that to NFP and C?

Speaker 6: Yep. We're working to update those to NFP

Speaker 6: and CNN go forward. And,

Speaker 6: Nolan has

Speaker 6: reached out to all of the PNC markets.

Speaker 6: So they're actively being updated. I can't say they're all updated right now.

Speaker 6: And, typically, the business is updated on a renewal basis,

Speaker 6: so it doesn't cause cancel rewrites.

Speaker 0: So

Speaker 0: we would just need to go through our renewal cycle. We talking about a year? And then and then

Speaker 0: the license would be,

Speaker 0: also.

Speaker 3: Oh, that's a good point. Yeah. That's thank you, Martha, that,

Speaker 3: they they should stay open as long as they have active policies on them.

Speaker 0: Right.

Speaker 3: Yeah. I'm just thinking about that, but I think that's the case. Right? Yeah. Yeah. I think that makes sense. Wouldn't can can we ask for some help on that then? Like, that seems like it's a

Speaker 3: an operations

Speaker 3: need,

Speaker 3: and

Speaker 3: I I don't know how to do it. I would probably have to hire a third party to do that.

Speaker 3: To do what? I'm sorry. To renew the entity licenses.

Speaker 4: When what did you do?

Speaker 3: Say again?

Speaker 3: When when is the license due for renewal? Well, there's probably 40 green? There's probably 46 of them.

Speaker 0: Oh,

Speaker 0: alright. We why don't we check this offline? If we can we can

Speaker 0: chat with Lisa here.

Speaker 3: Yeah. Probably, now that you say that, I bet they're going to want to compliance will wanna know that they're active.

Speaker 0: Yep.

Speaker 4: Right.

Speaker 1: Yeah. We'll we'll circle up Roper

Speaker 1: and get Lisa involved.


```

**Why it matters:** Sam Brown (NFP) confirms BoR transitions are at-renewal (rolling). Mullen team acknowledges licenses must stay open while policies are in force. Roper makes the operational ask explicit ("would probably have to hire a third party"). The shared NFP need surfaces but no one volunteers ownership.

### Smoking gun: Transcript 120 (02/27) — Roper's prior warning

**Title:** Crystal extended working session - Block, Clark, Downs, Kozin
**Date:** 2026-02-27
**Source:** zoom, recording id 120, chunk 85

**Chunk 85:**

```
Roper DeGarmo: Let's just say to her, Claude thinks I didn't reply to you on this question about where to send endorsements, if that's true. I don't have a blanket answer. What I want to do is have AI create as many as possible for us, and then route the edge cases to tests, but we'll work on them on a case-by-case basis.

Roper DeGarmo: Can you make detailed notes so that we could reverse anything that we did together?

Roper DeGarmo: she and I just got off a call where someone at NFP said, yes, just send me your spreadsheet and we'll take it from there. So we think we're in good shape. However, a new wrinkle has occurred that we might want to keep licenses open for the agency.

Roper DeGarmo: during the earn-out period when we have to carry E&O coverage over the next 6 years. I don't know if we need the licensings as we go forward, but I want to make a note that we need to decide, do we need the agency licenses going forward.

Roper DeGarmo: That's way too many for me to look at once. If they're grouped together, like, I could look at login and authorization at once, but not that many. If you want my opinion, you're gonna have to shorten the loops a lot.

Roper DeGarmo: I don't know what that is, show me the full email.

Roper DeGarmo: Let's just say something fairly casual, like…

Roper DeGarmo: Hey, Tess, I just wanted to check in and reassure you that if these meetings Feel strange, and… unproductive.

Roper DeGarmo: And you wonder, are we making any progress?

Roper DeGarmo: I just assure you, you're not alone. It feels very helter-skelter. I really want a copy of the master

Roper DeGarmo: spreadsheet she was showing us, and then I think we'll understand what's happening then.

Roper DeGarmo: make that draft better as short as possible. The goal is that… I'm just making sure Tess knows that if she feels confused or out of the loop.


```

**Chunk 86:**

```
Roper DeGarmo: spreadsheet she was showing us, and then I think we'll understand what's happening then.

Roper DeGarmo: make that draft better as short as possible. The goal is that… I'm just making sure Tess knows that if she feels confused or out of the loop.

Roper DeGarmo: she's… Not alone, because I am confused and feel out of the loop on a bunch of stuff.

Roper DeGarmo: Any idea what the meeting was about and who was in it?

Roper DeGarmo: Market as read and remove the…

Roper DeGarmo: Today, tomorrow, next week, next year labels.

Roper DeGarmo: Okay, one at a time.

Roper DeGarmo: No, just the last email I received from Rachel Finger, asking Rachel if she has a copy of the GEICO commercial auto policy she bound.

Roper DeGarmo: put that on a draft email and a knowledge transfer blurb on my clipboard. I'm gonna have Shortwave send this one.

Roper DeGarmo: Can you find all the emails that are related to setting up new accounts, and…

Roper DeGarmo: Group them together under a to-do.

Roper DeGarmo: Probably not, no.

Roper DeGarmo: Shit.

Roper DeGarmo: Can you open the last email I received from Rachel Finger that I can reply to?

Roper DeGarmo: I think I did that last night, can you double check?

Roper DeGarmo: There should be an email going out to Julie.

Roper DeGarmo: draft a quick reply to him, saying, hey John, nothing to worry about.

Roper DeGarmo: In AIG's terms, Anything less than 30 days is speedy processing.

Roper DeGarmo: We'll let you know if there's anything to worry about. Have a nice weekend.

Roper DeGarmo: Please put the draft on my clipboard with a knowledge transfer blurb so I can let Shortwave

Roper DeGarmo: Draft and send the message.


```

**Why it matters:** Roper independently flagged the 6-year E&O / agency license coupling 10 days post-close, before NFP's compliance gap surfaced on 04/10. Documents that Roper saw the issue early; NFP did not address it for 6 weeks.


---

## 6. Function-by-Function Audit

Every milestone, grouped by function. ★ NEW = newly surfaced (not in 4/14 baseline).

### 01. HR

| # | Status | Owner | Problem Type | Primary | Notes (excerpt) |
|---|---|---|---|---|---|
| row 2 | Complete | Doug Hammond | Resolved | Welcome to NFP - email from Doug Hammond | Doug Hammond welcome email landed 2/18 confirming SPI is officially on the NFP family roster. Foundational kickoff communication; no further... |
| row 3 | Complete | Stephanie Goldman | Resolved | Welcome leaders to NFP and introduction of HR team and regional support | HR team and regional support introductions completed via Stephanie Goldman handoff [email#386, email#1317, email#1318] and reinforced across... |
| row 4 | Complete | NFP HR (corporate) | Resolved | "Brand New Day" Welcome Meeting (March 10) | Brand New Day welcome session held 3/10 as planned per baseline tracker.... |
| row 5 | Complete | Mary Mullen | Resolved | HR Technical Training | HR technical training delivered 3/3 with Mary Mullen as central coordinator [email#16, email#17, email#18, email#24, email#25]. Reinforced i... |
| row 6 | Complete | Nancy Cronin | Resolved | HR Systems/MyApplications, PeopleFirst Portal and Workplace | PeopleFirst Portal and MyApplications walkthroughs delivered with Nancy Cronin support [email#1227, email#1228, email#1231, email#1232, emai... |
| row 7 | Complete | Mary Mullen | Resolved | Utipro Time Management Training (employees and supervisors) | UltiPro Time Management training closed per baseline; PTO cutover sequencing now folded into Workday HCM go-live tracker [transcript#351].... |
| row 8 | Complete | Kellie Green | Resolved | 1st Payroll under NFP (March 6) | First NFP payroll processed 3/6 with Kellie Green driving from the payroll side [email#74, email#75, email#76, email#78, email#1178]. Andria... |
| row 9 | Complete | Kim Pillar | Resolved | Benefits Training Session | Benefits training delivered through Kim Pillar's session series [email#374-378, email#380, email#383, email#464-477]. Marked complete per ba... |
| row 10 | Complete | Andria Griffin | Resolved | Benefits Enrollment Period (March 1) | Benefits enrollment closed 3/17 with Andria Griffin operating ground truth [email#889, email#890, email#899, email#928, email#929, email#109... |
| row 11 | Complete | Andria Griffin | Resolved | NFP Benefits Enrollment Due | Enrollment deadline met; Andria Griffin confirmed completion and applied premium catch-up to 3/20 paycheck [email#1061].... |
| row 12 | Complete | Kim Pillar | Resolved | 401(k) Employee Training Session | 401(k) employee training session delivered per baseline.... |
| row 13 | Complete | Jackie Searles | Resolved | 401(k) Employee Enrollment in NFP Plan | 401(k) enrollment completed via Jackie Searles' onboarding pipeline [email#93, email#96, email#100, email#104].... |
| row 14 | Complete | NFP HR (corporate) | Resolved | 401(k) Employee Transition into NFP's plan | 401(k) transition closed per baseline; legacy plan rollover paths communicated.... |
| row 15 | Complete | Jackie Searles | Resolved | NFPs Policies and Handbook | Handbook reviewed in Chicago session per baseline. Jackie Searles confirmed acknowledgements via HRIS template completion [email#101, email#... |
| row 16 | Complete | NFP Compliance (corporate | Resolved | Compliance Training Period | Ninjio core complete per baseline; broader compliance modules deferred to post-July 45-60 day window [email#551, email#828, email#829].... |
| row 17 | Complete | NFP Compliance (corporate | Resolved | Compliance Training Completed | Compliance training completed per baseline tracker.... |
| row 18 | Complete | Roper | Resolved | Concur (Travel & Expense) | Concur launched 4/2; Roper learned the booking/expense flow before 4/13 NFP Personal Risk Summit [email#155, email#334]. Note: separate 'Con... |
| row 19 | Complete | Jackie Searles | Resolved | AMEX Corporate Cards | AmEx corporate cards received per baseline. Jackie Searles closed loop on issuance [email#96, email#97, email#112, email#113]. (Bamford 3/20... |
| row 95 | Stuck | Andria Griffin | Ownership Vacuum | HSA accounts (Optum) | Optum HSA accounts still not opened as of 4/26 — weeks past the original baseline. Andria Griffin flagged the missing accounts on 3/17 and c... |
| ★ NEW | Complete | Jackie Searles | Resolved | HRIS Employee Tracker / I-9 / Onboarding Template completion | Jackie Searles delivered the HR import template and Employee Tracker pre-close [email#410] and walked the SPI roster through PeopleFirst onb... |
| ★ NEW | Open | unassigned | Ownership Vacuum | Vendor onboarding into Aon Coupa supplier system | Cross-function HR/Finance: NFP Procurement (via Coupa) requested SPI vendor list to onboard business-related expense vendors [email#117]. No... |
| ★ NEW | Open | Mary Mullen | Active | UltiPro 2026 goals setup meetings (Mary Mullen) | Mary Mullen scheduled 1:1 goals meetings for the SPI leaders [email#1167, cal#1523] and walked Roper through the UltiPro Myself/Goals workfl... |
| ★ NEW | Open | Julie Lovall | Active | Laptop / hardware provisioning for SPI team | Julie Lovall (SVP National Operations) opened the laptop provisioning thread on 2/19 asking platform [email#416]. Hardware request is owned ... |
| ★ NEW | Open | NFP HR (corporate) | Sequencing | Workday HCM Go-Live June 29 | Corporate-wide Workday HCM go-live scheduled June 29 [email#193]. Central Region team meeting 4/23 confirmed cutover testing in progress and... |

### 02. Marketing

| # | Status | Owner | Problem Type | Primary | Notes (excerpt) |
|---|---|---|---|---|---|
| row 20 | Complete | Marco Altamirano | none | Marketing Kick-off call | 4/10: Complete [apr26] [src#335 2026-04-10 NFP marketing intro call with Alba and Robyn]; [src#56 2026-02-27 Summary, notes & next steps for... |
| row 21 | Complete | unassigned | none | Initial drafts of Client/employee/carrier communication templates | 4/10: Complete... |
| row 22 | Stuck | Roper | risk_pause | Define client communication / letters | 4/10: Email preferred over printed letters. Draft client email + press release to be shared for review [apr26] [src#515 2026-04-21 RE: For R... |
| row 23 | In Progress | Alma Ko | in_flight | Client communication period | Ends 4/7 per dashboard... |
| row 24 | Waiting | unassigned | sequencing | Finalize client communication | ... |
| row 25 | Complete | unassigned | none | PR Cyber Security Environment Validation (from IT/IMO) | Done — Roper DIY + Umzuzu... |
| row 26 | Waiting | unassigned | sequencing | PR Precautionary message to employees | ... |
| row 27 | Waiting | unassigned | sequencing | "Go-Green" (rebranding to NFP - TBC) | 4/10: Timing aligned with tech milestones (email migration, Day-in-Life sessions). Go Green date proposed after IT assessment... |
| row 28 | Waiting | unassigned | sequencing | Business Cards | ... |
| row 29 | Complete | Susan Clifford | none | Collateral materials | [apr26] [src#953 2026-03-25 *NEW* Yacht Practice Collateral]; [src#1182 2026-03-06 New Marketing Piece]... |
| row 30 | Waiting | unassigned | sequencing | Website Transition | 4/10: Minimal collateral to transition; expected to be light... |
| row 31 | Waiting | unassigned | sequencing | Transition Social media | [apr26] [src#1236 2026-03-02 NFP Corp Daily Digest]... |
| row 32 | Waiting | unassigned | sequencing | Signage | ... |
| row 97 | Waiting | NFP Marketing | sequencing | Go-Green rebranding | Target ~June... |
| row 98 | Waiting | NFP Marketing | sequencing | Business cards + collateral + signage | Target ~June... |
| row 99 | Waiting | NFP Marketing | sequencing | Website transition | Target ~June... |
| row 100 | Waiting | NFP Marketing | sequencing | Social media transition | Target ~June... |
| ★ NEW | In Progress | Susan Clifford | recurring_hygiene | PCG Confidential Client coding -- recurring report flagging Signature clients at | Recurring NFP report. Without flag, Signature clients are visible to non-Personal-Risk staff and pulled into Corp P&C marketing campaigns. S... |
| ★ NEW | In Progress | Roper | cross_function_align | Pause domain/DNS migration; align Mary, Marco, Brett before resuming marketing/I | Roper-paused 4/23 (src#1446). Cross-function with Tech. Domains are not client-facing -- no time sensitivity. Pause is precondition for down... |

### 03. Technology

| # | Status | Owner | Problem Type | Primary | Notes (excerpt) |
|---|---|---|---|---|---|
| row 33 | Complete | Roper | On Track | @NFP email addresses creation | Closed in baseline.... |
| row 34 | Complete | NFP Tech | On Track | Adjustments on legacy email system to avoid spam | Closed in baseline.... |
| row 35 | Complete | Marco Alta (NFP) | On Track | Technology Intro call with acquisition IT team | Closed at intro call (src 386).... |
| row 36 | Complete | Brandon Jackson + Tracy M | On Track | Cybersecurity Environment Assessment / Security Scan | NFP IT delivery model worked cleanly — Brandon Jackson + Tracy McClain owned scan + credentials handoff end-to-end (src 89, 414, 415, 420, 4... |
| row 37 | In Progress | NFP Tech (FortiClient: NF | On Track | Cybersecurity Environment Remediation (FortiClient + Ninjio) | FortiClient rollout 04/22 (src 506, 543); Ninjio episode delivered 04/20 (src 551); ongoing remediation cadence (src 660).... |
| row 38 | Complete | NFP Tech | On Track | Ninjio Launch | Closed in baseline.... |
| row 39 | Complete | Roper | On Track | Ninjio Training Period | Closed in baseline; ongoing episodes (src 551).... |
| row 40 | Complete | Roper | On Track | Ninjio Training Completed | Closed in baseline.... |
| row 41 | Not Started | NFP Tech | Sequencing | Email System Migration (TBC) | TBC; sequenced after DNS.... |
| row 42 | Not Started | NFP Tech | Sequencing | Email domain change to @nfp.com (TBC) | TBC.... |
| row 43 | Not Started | NFP Tech | Sequencing | Email Migration Hypercare | TBC.... |
| row 44 | Not Started | NFP Tech | Sequencing | Conduct Office Integration (TBC) | TBC.... |
| row 45 | Not Started | NFP Tech | Sequencing | Hypercare | TBC.... |
| row 46 | Not Started | NFP Tech | On Track | Post-IT Integration Training (Acadame) | TBC.... |
| row 47 | Complete | NFP Tech | On Track | Phone Migration | Closed in baseline.... |
| row 48 | In Progress | Roper / Keith Clemons (NF | On Track | "Day in the life" sessions | Keith Clemons blocked Tue 04/21 11am Teams session w/ recording (src 652). Day-in-the-life follow-up Airtable deep dive logged 04/21 (src 34... |
| row 49 | In Progress | Roper / Courtney Kendrick | On Track | Application Deep Dive — Airtable | Day-in-the-life follow-up scheduled, Airtable deep dive on agenda (src 349, 652).... |
| row 50 | Not Started | Roper (waiting) | Sequencing | Application Deep Dive — Claude AI | Claude AI deep-dive deferred behind Epic + DNS workstreams; not blocked, queued by Roper.... |
| row 82 | In Progress | Mark Rieder / Katherine M | On Track | AI Strategy deep dive + Gaya pilot | AI strategy + technology roadmap discussed on 04/01 NFP team meeting (src 356).... |
| row 83 | In Progress | Josh Zacher → Roper | On Track | CanopyConnect credentials | Discovery covered on 03/27 NFP team meeting; Roper noted pricing favorable (src 341).... |
| row 86 | In Progress | John Seckner (NFP) / Rope | Sequencing | DNS/Registrar migration + domain admin | Roper paused 04/23 due to email-outage risk during client work crunch (src 494, 511, 520, 593). Right call — staged async work continues; Tr... |
| row 89 | Not Started | Roper | On Track | Copilot license | No new evidence this cycle.... |
| row 96 | In Progress | NFP Tech (Mary Ondrasek,  | Sequencing/Stuck | Epic smoke testing + go-live (KC1 branch) | KC1 branch live 04/16 BUT downloads NOT enabled — manual workflow only (src 615). Activity & Policy Type codes tied to Sam Brown / Nolan, bl... |
| row 101 | Waiting | NFP Tech | Sequencing | Email system migration to @nfp.com | Sequenced behind DNS migration pause and Epic hypercare.... |
| row 102 | Waiting | NFP Tech | Sequencing | Office integration (conduct) | Sequenced w/ email migration.... |
| ★ NEW | In Progress | NFP HRIS / Workday team | On Track | Workday HCM go-live June 29 (HRIS migration, cross-function w/ HR) | Corporate-wide rollout announced 04/14 (src 193); reinforced on Central Region team meeting 04/23 (src 352). Cross-function w/ HR — Roper as... |
| ★ NEW | In Progress | Roper / Lisa | Time-Critical | Agency Cybersecurity (NY DFS 23 NYCRR 500) annual renewal | Annual compliance filing due 04/15/2026 per Lisa via Idaho/licenses email (src 116). NFP IT delivers underlying controls (Brandon/Tracy stac... |

### 04. Finance

| # | Status | Owner | Problem Type | Primary | Notes (excerpt) |
|---|---|---|---|---|---|
| row 51 | Complete | Mary Bamford | Resolved | Workday Company (GL) Creation | Workday GL company set up at NFP. Baseline marked Done; one stray reference [email#56] confirms Mary Bamford treats GL as in place. No subse... |
| row 52 | Complete | Mary Bamford | Resolved | GL Mapping | Baseline marked Done 4/14. No new evidence in clustering pass contradicts. Carry forward.... |
| row 53 | Stuck | Roper | Ownership Vacuum | Closing balance sheet review and upload | QB reconciliation undo + closing BS still open after 4/14. Mary Bamford repeatedly chasing same items through 4/24 [email#60][email#133][ema... |
| row 54 | Stuck | Mary Bamford | Ownership Vacuum | Month end and finance & accounting processes onboarding | Month-end close drags. March close used estimates per 4/10 transcript [transcript#310]. Bamford repeatedly demands more from Roper rather th... |
| row 55 | Stuck | Roper | Ownership Vacuum | Upload month 1 closing activity | Blocked by QB reconciliation undo (baseline row 53). Bamford asking through mid-April [email#159][email#160] but no resolution path landed.... |
| row 56 | Stuck | Roper | Ownership Vacuum | Upload month 2 closing activity | March close used estimates per 4/10 [transcript#310]; Bamford still chasing March bank statement / source docs through 4/24 [email#130][emai... |
| row 57 | Open | Logan Christianson | Sequencing | Coupa / Accounts Payable Onboarding | Logan Christianson at NFP genuinely owns the Coupa side [email#156][email#194]. Waiting on technical preconditions (Coupa go-live + supplier... |
| row 58 | Open | Ryan Mediate | Sequencing | Opening balance sheet & working capital true-up calculation | Ryan Mediate at NFP M&A genuinely owns and is moving the WC true-up [email#6][email#21][email#33][email#34][email#35][email#38][email#40]. B... |
| row 59 | Stuck | Roper | Ownership Vacuum | AmEx statement — 3/20 payment for Mary Bamford | Bamford originally asked 4/6; baseline captured 4/14. She is still re-asking through 4/15+ [email#161][email#167][email#172][email#198][emai... |
| row 60 | Stuck | Roper | Ownership Vacuum | Expense descriptions — Acumen KS $1,250 + OgleTree Deakins $170.10 | 4/6 ask, baseline captured 4/14, Bamford re-asking through 4/24 [email#161][email#172][email#198][email#200]. Now embedded in 4/24 SharePoin... |
| row 61 | Stuck | Roper | Ownership Vacuum | Deposit support — carrier statements for March | 4/6 ask still alive 4/14+ [email#60][email#63][email#79][email#198][email#199][email#274][email#291]. Bamford coordinator role; Roper does t... |
| ★ NEW | Stuck | Rajulla Nadar | Sequencing | Landmark Bank portal access provisioning for NFP Treasury | 16 emails Mar–Apr coordinated by Rajulla Nadar (NFP Treasury) [email#178][email#182][email#185][email#188][email#190][email#195][email#197][... |
| ★ NEW | Open | Jackie Searles | Sequencing | AmEx card issuance & Concur T&E onboarding (program) | 5 emails Jackie Searles owns from NFP HR [email#93][email#96][email#97][email#101][email#112]. 4/10 HR ops meeting confirmed Concur+AmEx lau... |
| ★ NEW | Open | Roper | Ownership Vacuum | Bamford 4/24 SharePoint source-doc demand list — 15 specific transactions by 5/1 | 15 line-item asks pulled from 4/24 SharePoint screenshots (sources 358–372). Bamford is demanding upload of receipts/invoices for each trans... |
| ★ NEW | Active | Roper | Active | Bank balance reporting to NFP Treasury (monthly recurring) | 3 emails [email#169][email#170][email#171]; Rajulla Nadar requests month-end Landmark balance. Recurring obligation through 6-year SPI shell... |
| ★ NEW | Open | Rajulla Nadar | Sequencing | Add NFP authorized signers to Landmark operating account | 2 emails [email#47][email#67][email#68]. Rajulla Nadar coordinating signer additions. Real progress; gated on Landmark paperwork.... |
| ★ NEW | Open | unassigned | Ownership Vacuum | Concur T&E onboarding for Roper specifically | 1 email [email#155]. Owner unclear — Jackie Searles owns program (milestone C) but Roper-specific access not yet confirmed.... |
| ★ NEW | Active | Roper | Ownership Vacuum | Agency entity license renewals during 6-year SPI shell-life (46 entity licenses  | 46 SPI entity licenses must stay active through 6-year tail so NFP can roll Books of Record. Per 4/10 Mary Mullen 1:1 [transcript#310] and 2... |

### 05. Treasury

| # | Status | Owner | Problem Type | Primary | Notes (excerpt) |
|---|---|---|---|---|---|
| row 62 | Complete | Ryan Mediate |  | Banking Assessment | Pre-close banking assessment / wire mechanics complete. $25k cap on Landmark legacy account confirmed [src 6, 34]; balance snapshots provide... |
| row 63 | Complete | Keara Rodriguez |  | Creation of Wells Fargo Accounts (if needed) | Not needed per Keara recap (baseline notes_apr14). No new evidence in clustering pass.... |
| row 64 | Open | Roper DeGarmo | ownership_vacuum | Closing selected legacy bank accounts | Per baseline 4/10: one legacy account remains, slated to close as Wells Fargo transition progresses. No clustering evidence advanced this in... |
| row 65 | Complete | Rajulla Nadar |  | Addition of NFP signatory representative on legacy account (if applicable) | NFP Accounting intros opened the workstream [src 46]; NFP Treasury formally requested adding Caleb Noel + others as signers on Landmark [src... |
| row 66 | Open | unassigned | ownership_vacuum | Migration to Wells Fargo / NFP Banking Platform (TBC) | No clustering evidence in reconcile window. Migration to NFP banking platform remains TBC; in the interim Roper continues to operate Landmar... |
| ★ NEW | Complete | Danielle Williams |  | Open new SPI business checking at Landmark post-close (Roper + Rachel + Danielle | Post-close Roper + Rachel opened a separate Landmark business checking with Danielle Williams; Nick Border handled docs; Rachel + Roper prov... |
| ★ NEW | Stuck | Rajulla Nadar | ownership_vacuum | NFP Treasury portal access to Landmark for Rajulla/Donna/Jessly | OWNERSHIP VACUUM. Baseline 65 closed (signers added) but NFP Treasury still has no portal access weeks later — Roper is operating the bank f... |
| ★ NEW | Open | Roper DeGarmo | ownership_vacuum | Monthly bank statement + commission delivery to Mary Bamford / NFP accounting | OWNERSHIP VACUUM. Recurring close cycle Roper still operates as books/cash-source for NFP. February month-end: Mary Bamford asks for outstan... |
| ★ NEW | Stuck | Logan Christianson | nfp_slow | SPI vendor onboarding into Aon Coupa supplier system | Logan Christianson (NFP) launched Coupa setup 3/18 to route SPI vendor expenses through Coupa rather than personal/operating account [src 11... |

### 07. Risk Management

| # | Status | Owner | Problem Type | Primary | Notes (excerpt) |
|---|---|---|---|---|---|
| row 67 | Complete | NFP Corporate Risk Mgmt | resolved | Addition of coverage under NFP/Aon Insurance Program | Done at close (per Apr 14 baseline). No new evidence in this pass.... |
| row 68 | Complete | Riana Sherwood | resolved | Procurement of ERP's for E&O | 6-year ERP bound and paid ($15,233 to KAIA). Christopher Sam (NFP Corporate Risk Mgmt) authorized binding [evidence #1361]; Riana Sherwood d... |
| ★ NEW | Open | Roper DeGarmo | dark_variant_adjacen | Determine agency license retention requirement under E&O retroactive coverage /  | Roper raised to Lisa whether agency licenses must be maintained given the asset purchase structure + SPI not writing new business + 6-year E... |
| ★ NEW | Stuck | Roper DeGarmo | dark_variant_adjacen | Operational E&O exposure from manual post-close service workflow (no AMS, no ser | Roper to Caleb: 'just trying to make sure we don't drop any balls that result in E&O' — describes post-close state as 'shut off our agency m... |

### 08. Carrier Management

| # | Status | Owner | Problem Type | Primary | Notes (excerpt) |
|---|---|---|---|---|---|
| row 69 | Complete | Sam Brown | None | SIA communication with local contacts | Closed 2/19. SIA->local NFP handoff completed pre-cluster window.... |
| row 70 | Complete | Sam Brown | None | Initial Market Notification to NFP Contacts | Closed 3/3. Sam Brown circulated initial notice; subsequent threads (s439,s1110) confirm carrier-side acks.... |
| row 71 | In Progress | Roper | Coordination | Full Market Notification Initiation | Owner=Roper per baseline. Active threads w/ Sam Brown + Tess (s122, s124) on carrier-by-carrier coverage; Sue/Susan Clifford team pulled in ... |
| row 72 | In Progress | Roper | Coordination | Ongoing Market Notification and consolidation | Heavy live activity (Mar-Apr): Melody Thammavong driving carrier code follow-ups (s545,s887,s888,s1041,s1065,s1066), Bryan Kissinger (s1074,... |
| row 88 | Not Started | Roper (waiting) | Decision Pending | Berkley One code decision | Still waiting on Berkley One decision. Brad Millican active on Chubb code in parallel (s1075-s1082,s1092). Kate Conneely engaged on Chubb si... |
| ★ NEW | Complete | Teresa Wharton | None | AIG > PCS One auto downloads live 2/27/26 | Tess confirmed (s1219) AIG download path is live as of 2/27/26 — first carrier in the post-acquisition stack to clear codes-tied + downloads... |
| ★ NEW | Open | Brad Millican | Decision Pending | Chubb agent code decision for Signature book (subcode under 64195 Chicago vs sep | Brad Millican leading the decision (s1075,s1077,s1078,s1080,s1082); Roper engaged (s1076); Kate Conneely supporting (s1118,s1119,s1320). Sub... |
| ★ NEW | In Progress | Nancy Cronin | Process Gap | Epic KC1 branch live, carrier downloads NOT enabled (manual processing) | KC1 branch went live 4/17 (s615) but downloads remain off pending codes-tied for each carrier. Concrete restatement of the gap that's tied t... |
| ★ NEW | Open | Amy Hill | Process Gap | PURE/MetLife/Hagerty Epic policy entry rules — download suspense root cause for  | Amy Hill flagged (s1206) PURE/MetLife/Hagerty entry-rule guidance is the root cause of PURE download suspense. Direct precondition for downs... |
| ★ NEW | Open | Susan Clifford | Process Gap | !ALT / Download Suspense — chronic downstream failure once codes ARE tied | Susan Clifford owns the suspense queue (s991). Even when codes-tied closes, transactions land in !ALT and need manual triage. AI-agent triag... |
| ★ NEW | Open | Andrea McDonald | Coordination | PRC Service Center integration with Epic for PCG Central Region | Andrea McDonald team handles carrier downloads/processing once service center pickup is live (s1124). Service center integration is the prec... |
| ★ NEW | Complete | Roper | None | Aon Edge flood — agency code 1006772 provisioned (private flood quoting) | Roper provisioned w/ Aon Edge code 1006772 (s759) — net-new market access via Aon-side affiliation post-acquisition. Quoting capability live... |
| ★ NEW | Open | Teresa Wharton | Process Gap | Universal Property AtlasBridge MFA — carrier access security upgrade | Tess flagged Universal Property MFA requirement on AtlasBridge (s714). Operational task to maintain access; minor.... |
| ★ NEW | Open | Teresa Wharton | Compliance | NFP cross-carrier signature/document retention policy | Tess issued compliance directive (s805) for retention across all carriers. Needs translation into Signature workflow + Epic doc-management c... |
| ★ NEW | Open | Mary Mullen | Ownership Vacuum | Chubb/PCG DNR + NY hurricane deductible bulletin distribution | Mary Mullen routes carrier UW bulletins (s563) — DNRs and NY hurricane deductible updates. Recurring pattern: bulletins arrive Mary->team bu... |
| ★ NEW | Open | Mary Mullen | Ownership Vacuum | AIG Collector Auto Re-Classification — Roper not on distribution list (blind spo | Mary fwd'd notice 3/20 (s1026) to Tess only; Roper got it 4/7 (s783) AFTER Tess emailed Mary explicitly (s942/s924) requesting it. Pattern: ... |
| ★ NEW | Open | Unknown (NFP carrier mgmt | Ownership Vacuum | BOR/CORG proactive-agent gap — carrier-side signaling not surfacing to receiving | s327 surfaced a BOR/CORG case where carrier-side broker-of-record change did not surface to receiving agent. Same family as milestones J/K: ... |

### 09. Licensing & Registrations

| # | Status | Owner | Problem Type | Primary | Notes (excerpt) |
|---|---|---|---|---|---|
| ★ NEW | Stuck | Roper | Ownership Vacuum (Da | Agency entity license renewals during 6-year SPI shell-life — NFP needs them act | WEDGE FINDING / DARK-VARIANT OWNERSHIP VACUUM. NFP requires SPI's 46-state agency entity licenses to remain active for the 6-year shell-life... |
| ★ NEW | Stuck | Unassigned | Ownership Vacuum | Roper KS Surplus Lines license renewal due 5/1/2026 — unrecognized May renewal s | OWNERSHIP VACUUM. Kansas Surplus Lines License renewal notice (NPN 4903465) for Roper, due 05/01/2026, was sent to roper.degarmo@nfp.com on ... |
| ★ NEW | Active | Lisa Black + RegEd | None (Working) | Individual producer license renewals via NFP/RegEd — May Background Information  | ACTIVE / WORKING COUNTER-EXAMPLE. NFP Licensing 04/23 broadcast (id 1414) instructs producers with May renewals to complete the BI questionn... |

### 10. Region/Sales/Ops

| # | Status | Owner | Problem Type | Primary | Notes (excerpt) |
|---|---|---|---|---|---|
| row 76 | Active | Mary Mullen | recurring_hygiene | Regional Sales Updates — Central Region (Mary Mullen) | Mary Mullen (96 mentions) anchors Central Region cadence. 99 linked items including biweekly Central Region Leader Calls and KTF threads. Br... |
| row 80 | In Progress | Roper | in_flight | Integration — Send ranked list to Keara Connelly | Keara Connelly is integration PM. 37 linked items spanning Integration Review cadence and Roper deliverables.... |
| row 81 | Not Started | Roper | sequencing | Tess full-time conversation with Brett Woodward | Roper-owned conversation pending with Brett Woodward.... |
| row 84 | Not Started | Roper | recurring_hygiene | Goals in UltiPro | HR system entry — 10/20/30 SMART goal drafted per UltiPro topic file.... |
| row 85 | Not Started | Roper | cross_function_align | NB premium goal for EPIC | Awaiting clarity from Mary on EPIC NB goal format.... |
| row 87 | Waiting | Roper | risk_pause | Life insurance policy list + commission | Roper waiting on internal life data before delivery.... |
| row 90 | Complete | Roper | resolved | P&C Town Hall — April 20 | Town Hall date Apr 20 — past as of 4/26 reconcile.... |
| row 94 | Stuck | Susan Clifford | Ownership Vacuum | Susan Clifford — ALT report / AI agent | Susan Clifford waiting on sample data to advance ALT monthly rollup AI agent.... |
| ★ NEW | Complete | Roper | resolved | NFP Personal Risk Summit — Terranea Apr 13-16 | Summit collapsed from 52 cluster items; mostly contextual/calendar entries. Discrete follow-ups tracked independently below.... |
| ★ NEW | Open | Brett Woodward | in_flight | TGV insurance whitepaper — Brett Woodward collaboration | Brett brought Roper into Isabel Sjodin's whitepaper effort; intro call Apr 13. 8 linked threads.... |
| ★ NEW | Open | Roper | in_flight | Goldman Ayco lead — Swans / celebrity renter (Jeff DeMaio crossover) | Active April 21-22 thread. Jeff DeMaio bridge from Goldman Ayco into NFP after 2026-02-17 acquisition. 7 linked items.... |
| ★ NEW | Open | Tess Presnal | cross_function_align | AIG Collector Auto Re-Classification — Roper not on dist list (cross-ref to Carr | Distribution list gap — Roper missed AIG Collector Auto re-class memo. Primary milestone lives in Carrier Mgmt; this is a Region/Sales cross... |
| ★ NEW | Complete | Roper | resolved | Press Release & Client Communication — acquisition announcement (cross-ref Marke | Acquisition press/client comm completed. Cross-reference only; primary in Marketing function. 4 items.... |
| ★ NEW | Open | Roper | in_flight | AI evangelism with NFP leadership (Mark Rieder, Katherine Minami) | Roper-driven sales/strategy. Mark Rieder (NFP CHRO) + Katherine Minami engagement. Per diagnostic lens: note but don't over-elevate. 4 items... |
| ★ NEW | Open | Roper | in_flight | Gil Lai NY intro list — Beyer/Bancker pipeline | Roper-driven sales pipeline via Gil Lai. Michael Beyer/Bancker is large untapped commercial. Note but don't over-elevate per diagnostic lens... |
| ★ NEW | Open | Roper | in_flight | Day in the Life Reviews — NFP shadowing Signature workflows | NFP shadowing Signature workflows — Mar 27 session accepted. 3 items.... |


---

## 7. Smoking Gun Emails (Full Text)

Five load-bearing email bodies embedded in full so you don't need the database to read them. Each has a brief explanation of why it's smoking gun.

### Mary Bamford 04/24 — RE: Document request and Quickbooks (red-line response, 15 source-doc demands by 5/1)

**Date:** 2026-04-24 16:56:30+00
**Subject:** RE: Document request and Quickbooks
**Gmail ID:** 19dc06bfc916c066

```
Hi Roper,

Please see my responses in Red below and screenshots to assist you.  Feel free to call me on Teams if you would like to further discuss.

Thank you,

Mary Bamford
She/Her/Hers
Assistant Vice President
West Region Accounting, Mergers & Acquisitions
NFP, an Aon Company
2300 Contra Costa Blvd | Suite 600 | Pleasant Hill, CA 94523
P: 925.279.4992 | F: 925.956.7601 | mary.bamford@nfp.com<mailto:mary.bamford@nfp.com> | NFP.com


From: Roper DeGarmo <roper@signatureadvisor.com>
Sent: Tuesday, April 21, 2026 10:30 AM
To: Mary Bamford <mary.bamford@nfp.com>; Mary Mullen <mary.mullen@nfp.com>
Subject: RE: Document request and Quickbooks

ATTENTION - EXTERNAL EMAIL - The sender of this email is EXTERNAL to our email system. Do not click links or open attachments unless you recognize the sender and know the content is safe.
Hi Mary... it would be extremely helpful if you could be specific about what you need uploaded. I want to get you everything, but "the items I've requested thus far" spans a lot of conversations and I want to make sure nothing falls through the cracks.

Here's my best guess at the full list. Can you confirm, correct, or add to it?

✅ = Done | 🔲 = Open | ❓ = Need clarification

Documents to upload to SharePoint:

  *   ✅ March Landmark bank statement (already sent via email 4/6, need to re-upload to SharePoint?) NO, this is Done. I’ve saved to SharePoint.

  *   🔲 April Landmark bank statement. Please upload by 5/1
🔲 Am Ex statements related to payment in Feb $4,119.53 and March $5066.92 Please upload to [​Folder icon]  American Express Stmts<https://nfp.sharepoint.com/:f:/r/sites/SignaturePersonal/Shared%20Documents/American%20Express%20Stmts?csf=1&web=1&e=y0MoCu>

  *   🔲 April AmEx statement Please upload a statement if a payment was made in April. I don’t have access to the bank account to know if a payment was made in April

  *   ❓ Commission statements (March and April, but I need your help here, see below) I don’t have access to April’s bank activity until I receive the Landmark statement.  For March please upload support for the following deposits:
[cid:image002.png@01DCD3CE.968DEE80]

  *   🔲 Vendor invoices paid since acquisition (Feb 2026 forward)
[cid:image003.png@01DCD3CF.0280AAB0]
[cid:image005.png@01DCD3CF.B6AB1A70]
[cid:image004.png@01DCD3CF.53548010]

Support for checks cleared post acquisition
The Cincinnati Insurance $760.99
First Citizen $3254.08
OgleTree $2381.40


  *   ❓ Carrier deposit support/statements Same as Commission statements above

QBO items (Brooke is working on this):

  *   🔲 Undo the 2/17/26 Feb bank reconciliation (Account 1003 Landmark National Bank)-Done

  *   🔲 Grant you full admin access to QBO

Expense descriptions (from your 4/6 email):

  *   ✅ Acumen Kansas City $1,250, leadership and peer advisory forum Please upload invoice

  *   ✅ OgleTree Deakins $170.10, legal services related to acquisition please upload invoice

Commission statements, a transparency moment: I need you to tell me exactly which carriers you need statements from. Some carriers send statements electronically, some go to our PO box, and some go to a Detroit Mail Processing Center. See deposit info above for March.  Will need support for an April deposits as well

Prior to the acquisition, I had a team member in the Philippines who handled the intake process for all of that, converting, filing, and routing to the right people. That role was eliminated as part of the transition, and nobody has been covering it since. So it's very likely there are statements sitting in the PO box or at my home address 5402 Birch that haven't been opened, scanned, or filed.

I'm not trying to make excuses. I just want you to know why some of this may take a meaningful time to pull together. If you can tell me which carriers and which months, maybe I can reach out to the former employee and see if she remembers where they came from and when she saw them.

Let me know your thoughts.

Roper

---
Roper C. DeGarmo
Vice President Private Client Group
NFP, an Aon company | NFP.com<https://t.shortwave.com/links/v1/1y3WvESP_T_eTb4gky6xD-yhhGfqffMAlzHvcG08LFGzfQpCPNOW63ndKdXNntV5FHaiNM7irt_RkAIe07Gnzjy4AnOZsdpxIA7u8S8tXpIpQ-Qb5PjQwEVfQv0n602FZG3Mst5rE-Mm1_AjQ-DISNjCkYGg_6ogrP1HJPuaSFM>
Office: 913-904-1881
Cell: 913-210-9054
linkd.in/RoperDeGarmo<https://t.shortwave.com/links/v1/m6RS31xjChuB2n4EBcZjTSQuSJTajfGVd5xsy-EEtrGSpRh53WR9zoVzgMr93rGpSPdQ4Z9dIKGnXujnkBiHPs4c_o70Cc7C1sqMypkp1ae4GJyOupRokgHxOPgYPrPJvy8ymHKQ5UGfth0rv_AO2zaCnd-ln_6upKzyTuSLEeM>


On Tue Apr 21, 2026, 05:14 PM GMT, Mary Bamford<mailto:mary.bamford@nfp.com> wrote:
Hi Roper,

Please start uploading the items I’ve requested thus far.

Thank you,

Mary Bamford
She/Her/Hers
Assistant Vice President
West Region Accounting, Mergers & Acquisitions
NFP, an Aon Company
2300 Contra Costa Blvd | Suite 600 | Pleasant Hill, CA 94523
P: 925.279.4992 | F: 925.956.7601 | mary.bamford@nfp.com<mailto:mary.bamford@nfp.com> | NFP.com


From: Roper DeGarmo <roper@signatureadvisor.com<mailto:roper@signatureadvisor.com>>
Sent: Tuesday, April 21, 2026 9:57 AM
To: Mary Mullen <mary.mullen@nfp.com<mailto:mary.mullen@nfp.com>>; Mary Bamford <mary.bamford@nfp.com<mailto:mary.bamford@nfp.com>>; Brooke McKenzie <Brooke.McKenzie@RubinBrown.Com<mailto:Brooke.McKenzie@RubinBrown.Com>>
Subject: Re: Document request and Quickbooks

ATTENTION - EXTERNAL EMAIL - The sender of this email is EXTERNAL to our email system. Do not click links or open attachments unless you recognize the sender and know the content is safe.
Hi Mary & Mary

I'm looping in @Brooke McKenzie<mailto:Brooke.McKenzie@RubinBrown.Com>

I've authorized her get you anything you need... including full admin rights to QBO.

If you'll just walk her through what you need, she'll have it to you very quickly.

I also now have your secure upload portal:

Signature Personal Insurance → NFP Share Point<https://t.shortwave.com/links/v1/6_GQ60uwDuuYu5Lb7nlYot6l459EsV2MWq2mRI2kF8eD__uA_zk1TxguLuIZ1kmOKyVVNQCSfZTw4myWqvsyzopEG4YLINqeLQimEIJsmhqY86hZA0QR9kiBqVN-sBgbVYfPY-ik2YPWDkqujiwdALFoQMYD0NdKdm7CbIRVJuo>

I'm happy to give you the full archive of commissions, bank, and credit card statements if that's helpful or you can send me a check list of what you need and we'll work through it ASAP.

@Brooke McKenzie<mailto:Brooke.McKenzie@RubinBrown.Com> Let me know if you need anything else from me.

Regards

Roper

---
Roper C. DeGarmo
Vice President Private Client Group
NFP, an Aon company | NFP.com<https://t.shortwave.com/links/v1/2JYsd3_9spLyozAzWu0ivk_NtWa-HiQnJUqnpSncCC_NdURppo7ySV2ZcvYjRIofVA5io3enem79UgPpDvnUqWYWbx796EgUTuR7gllR1_7OCzxzNKUZb0JQ4uAlNymNuETWbn7FPaVq6Rsj8KQA8pNZmhJim0YT5InIMCXoe-4>
Office: 913-904-1881
Cell: 913-210-9054
linkd.in/RoperDeGarmo<https://t.shortwave.com/links/v1/PVN-iuiVpjTlOA096D5pBXaK8P1C7kyvZkDBktDDmQAgdf_Mp4A8hL3st_pA-axEvT326iyLSfOEFamANPdaD6rjMp3oNNGt1oPyz8SI-wKnlufHyd0bUmgcALbZTutc4Tbyde1ZJEdABxnsrNX--5i4I5nwbNyzsd0jHXWN4r0>

On Tue Apr 21, 2026, 03:57 PM GMT, Mary Bamford<mailto:mary.bamford@nfp.com> wrote:
Hi Roper,

I created a Sharepoint folder for you to upload documents.   You should have already received an invitation email.  At your earliest opportunity this week, please upload the March and April commission statements, American Express statements, and any vendor invoices paid since acquisition.  Let me know if you have any issues with accessing the folders.

As for RubinBrown, will you share Brooke’s info as I’m sure my Quickbooks request can be cleared up w/ a 5-minute call.

Thank you,

Mary Bamford
She/Her/Hers
Assistant Vice President
West Region Accounting, Mergers & Acquisitions
NFP, an Aon Company
2300 Contra Costa Blvd | Suite 600 | Pleasant Hill, CA 94523
P: 925.279.4992 | F: 925.956.7601 | mary.bamford@nfp.com<mailto:mary.bamford@nfp.com> | NFP.com


From: Roper DeGarmo <roper@signatureadvisor.com<mailto:roper@signatureadvisor.com>>
Sent: Tuesday, April 21, 2026 8:15 AM
To: Mary Mullen <mary.mullen@nfp.com<mailto:mary.mullen@nfp.com>>
Cc: Mary Bamford <mary.bamford@nfp.com<mailto:mary.bamford@nfp.com>>
Subject: RE: Month end close

ATTENTION - EXTERNAL EMAIL - The sender of this email is EXTERNAL to our email system. Do not click links or open attachments unless you recognize the sender and know the content is safe.
Good morning Mary & Mary.

I've engaged RubinBrown to work on the access issue first and have approved Brooke to interact directly with NFP on my behalf. She's better equipped to troubleshoot the QBO permissions, then I'll put the documents you need into Microsoft OneDrive once that's ready.

Once Brooke has new credentials sorted and we have clarity on what's still blocked, I'll circle back. If a Teams call is still needed after that, happy to find time before Wednesday noon.

Thank you for your patience.

R
```

**Why it matters:** This is the email behind the 4 PNG screenshots. Bamford's red-line response to Roper's checklist enumerates 15 specific transactions she's asking Roper to upload to SharePoint by 5/1: 8 March deposits (American Bankers, Cincinnati, PURE EDI, PURERISKMG, Progressive, PUREPROGRAMS, AIG Private Client, Mobile Deposit) + 7 vendor invoices (Equip Financing, 2x Xoom, Acumen, OgleTree, Chubb, Tarsus). Several of these are duplicates of her 4/06 ask Roper already captured at row 60. The recurring nature of the demand IS the diagnostic.

### Mary Mullen 04/24 5:59pm — RE: Weekly 1:1: Integration recap

**Date:** 2026-04-24 22:59:53+00
**Subject:** RE: Weekly 1:1: picking a standing slot
**Gmail ID:** 19dc1b8b1224e098

```
Hi Roper,

As a summary from the Integration Recap call today as well as urgent items needed. I also believe Keara will be sending a recap); and perhaps Crystal/Tess was also able to update you. Items in red are responses or items needed.
M&A Open Items – High Priority

  *   Mary Bamford will be looking for the April Landmark bank statement. Please upload by 5/1
     *   There are several other items for which she is looking, but the April statement seems to be the most urgent. The next item below ties into some of her request.
  *   Mail: You mentioned that nobody has been covering the mail since the acquisition. (“So it's very likely there are statements sitting in the PO box or at my home address 5402 Birch that haven't been opened, scanned, or filed.”)
     *   If you are comfortable sending the batches of unopened mail from the PO Box (you’ll need to ask the PO Box vendor to package and mail) as well as the items at your house that haven’t been unopened and are work related, we can ask our PRSC team to scan and get in order.
        *   I will provide the proper address upon request
Service center support prior to Epic being able to transact business (not after Epic and download allow us to transact business) Even when downloads start, there will be weeks of clean up and training to get crystal up to speed and the client work won't stop for training. I have been working with Crystal to see if we can be added to your carrier portals now to see about processing changes for you while we wait for the codes to be tied together. In addition, Julie will follow-up Monday morning with Sam Brown re carrier management (namely AIG and PURE) since we don’t have responses from them on codes being tied together which needs to happen before download can occur.
Claims department support. Hail season is stacking open claims and we have no bandwidth. Can we get claims support so that this can be taken off our plate. I will check with Crystal on Monday to see how many claims (estimated) might be open on your desk right now. Justine’s team is willing to handle some of the claims follow-up in the interim (we spoke earlier), though your team will still need to file the claims. I’m also curious about your current claims procedure – how often do you follow-up and how involved are you with the adjusters throughout the process?
A "stop doing" list. Our Epic training revealed we are doing dramatically more processing than we will need to once Epic transacts (e.g., sending renewal notices that carriers already send). Help us identify the redundant work so we can drop it now. You can drop any sending of documents already provided directly from the carrier to the client. examples of this include sending any/all new/endorsements/renewals issued by admitted carriers (e.g. AIG, PURE, etc). As we discussed yesterday, this can be stopped now so efforts can be re-directed elsewhere.
Coupa: Mary Bamford will request 18 mons of expenses from QuickBooks so we can scrub and indicate the vendors who need to be set up in our recurring payment system Coupa. Once we have this list, we will need to gather W9 and ACH info from them. I scrubbed the 3 month list already and was able to narrow it down pretty easily. I think we’ll catch a few more on the deepened list, but it shouldn’t be thousands of vendors, likely around 50, if not under.

  *   A call has been scheduled for Monday. Please attend, or let the organizer know if you cannot attend and we will reschedule to include you.
Tess: I’m excited to see how her license testing goes this weekend. Having her fully licensed will allow her to be more engaged with clients and help to free Crystal up. We should definitely plan to discuss how we expand her role so that she’s taking work off of other plates.
I look forward to our call with Brett on Monday afternoon. Have a good weekend.



Best,

Mary


Mary Mullen, CAPI, CPRIA, ACPRIA
She/Her/Hers
Senior Vice President, Central Region Leader
Personal Risk
NFP, an Aon company
CA License #OF15715
500 West Madison Street | 32nd Floor | Chicago, Illinois 60661
P: 312.704.7000 | M: 312.493.2922 | F: 312.277.0025 | mary.mullen@nfp.com<mailto:mary.mullen@nfp.com> | NFP.com

Insurance services provided through NFP Property & Casualty Services, Inc., doing business in California as NFP Property & Casualty Insurance Services, Inc. License #0F15715.

From: Roper DeGarmo <roper@signatureadvisor.com>
Sent: Thursday, April 23, 2026 12:05 PM
To: Keara Connelly <keara.connelly@nfp.com>; John Seckner <john.seckner@nfp.com>
Cc: Mary Mullen <mary.mullen@nfp.com>; Courtney Kendrick <courtney.kendrick@nfp.com>; Michael Deberry <michael.deberry@nfp.com>; Graham Bateman <graham.bateman@nfp.com>; Keith Clemons <keith.clemons@nfp.com>; Bob Johnston <bob.johnston@nfp.com>
Subject: RE: Weekly 1:1: picking a standing slot

ATTENTION - EXTERNAL EMAIL - The sender of this email is EXTERNAL to our email system. Do not click links or open attachments unless you recognize the sender and know the content is safe.
Hi Keara, John, and Mary. A few items for each of you below.

Keara

Thanks for taking my call today. Wanted to get what we discussed in writing so we're all on the same page.


  *   You're going to let John know the domain/DNS migration is paused for now. Those domains are not client-facing and there's no time sensitivity.

  *   You're going to touch base with Mary and Marco, then set up a call with the three or four of us (me, you, Mary, Marco, and possibly Brett) to align on an integration path that doesn't keep creating E&O exposure on client work.

  *   I'm going to skip tomorrow's integration call so you can lead it and deliver the message directly to the team: we are at a critical point on operations with client work.

  *   The key thing I need you to carry into that conversation: we are NOT live on Epic. Epic is turned on, but there is no live policy data, no download, no claims support, no policy support, and no one on my team knows how to use it yet. That misconception is driving a lot of the timeline assumptions across the board.

John

I have the DNS audit/report put together and ready to hand over when the time is right, but I can't meet today at noon. Per my conversation with Keara, the domain migration is being paused. The reason: my virtual CIO flagged real risk of taking Signature Advisor's Google Workspace email offline mid-migration, and we are already behind on client work because the Philippines Team was both our "service center" and our Agency Management System. Ironically, removing humans from my work flow broke what we build over many many years. I can not take he risk of email outage until we have Outlook cutover, service center restoration, and client-work catch-up need to land first. I'll send the DNS package when we're ready to execute, not before.

Mary

First, genuine thanks for dropping Thor's hammer on the PURE programs earlier this week. We would have had an uninsured property for a PURE member without that intervention.

Second, can we add three items to today's central zone agenda? Each one could take meaningful load off me and Crystal right now.


  *   Service center support prior to Epic being able to transact business (not after Epic and download allow us to transact business) Even when downloads start, there will be weeks of clean up and training to get crystal up to speed and the client work won't stop for training.

  *   Claims department support. Hail season is stacking open claims and we have no bandwidth. Can we get claims support so that this can be taken off our plate.

  *   A "stop doing" list. Our Epic training revealed we are doing dramatically more processing than we will need to once Epic transacts (e.g., sending renewal notices that carriers already send). Help us identify the redundant work so we can drop it now.

Happy to discuss any of this further. Appreciate everyone's patience as we sort the sequencing.

...Roper


---
Roper C. DeGarmo
Vice President Private Client Group
NFP, an Aon company | NFP.com<https://t.shortwave.com/links/v1/NJ4IKikLKBDyVTwCceg8JzVxWqr6rPU2asNPwmAH5PIOpdkfCGJS8jAsBhxL8IiEh4qYwEpuWIGOqhhST-vm_-BOCTRKebgyHTwOOVWmNE3N-0_yeItFmF8oidPoGE0K48SKUInCw_24RTYNcEfpDb1AkXSP3bQpc8PhtSCAFV8>
Office: 913-904-1881
Cell: 913-210-9054
linkd.in/RoperDeGarmo<https://t.shortwave.com/links/v1/e15bfUaqqB-YO9qDyps2MGmwjKQ1X7Q_VV11eGKuJvBvZ5NIKY_cVkz5h5O9pwk516lRkCYACdIz-0QPD1hPKC1eWmzLknfXcaeEXFR5qilIOHYjOcqArkFc-01zia8JtZwxpvdMH1X0nc_VBaML7I7oOe3X7oBBnzRF7fuIEmY>


On Tue Apr 21, 2026, 09:33 PM GMT, Roper DeGarmo<mailto:Roper@signatureadvisor.com> wrote:
Hey John, I'm pretty sure we can do this in off hours asynchronously, leaving office hours for client work.

I think I already have a draft DNS export report, but I want to spend a bit more time with your email to make sure you have everything you need. My plan is to move my personal domains
```

**Why it matters:** Mullen's recap of the integration call. We audited it line-by-line earlier today (sequencing-vs-ownership-vacuum analysis). 6 distinct items: April Landmark by 5/1, mail backlog (PRSC scan offered conditional on Roper packaging), service center / carrier portal access (status update only), claims help (Justine team, scoped), stop-doing list (admitted carrier docs greenlight), Coupa scrubbing (asks Roper to operate QB). The 'stop doing' item we initially read as a clean win but corrected: Mullen doesn't see the QC cycle the PDFs serve. The Coupa ask is the load-bearing tell — NFP is asking Roper to operate QB.

### Roper 04/23 12:05pm — RE: Weekly 1:1 (the original ask that triggered Mullen's response)

**Date:** 2026-04-23 17:04:49+00
**Subject:** RE: Weekly 1:1: picking a standing slot
**Gmail ID:** 19dbb4d4308644d9

```
Hi Keara, John, and Mary. A few items for each of you below.

Keara

Thanks for taking my call today. Wanted to get what we discussed in writing so we're all on the same page.

- You're going to let John know the domain/DNS migration is paused for now. Those domains are not client-facing and there's no time sensitivity.
- You're going to touch base with Mary and Marco, then set up a call with the three or four of us (me, you, Mary, Marco, and possibly Brett) to align on an integration path that doesn't keep creating E&O exposure on client work.
- I'm going to skip tomorrow's integration call so you can lead it and deliver the message directly to the team: we are at a critical point on operations with client work.
- The key thing I need you to carry into that conversation: we are NOT live on Epic. Epic is turned on, but there is no live policy data, no download, no claims support, no policy support, and no one on my team knows how to use it yet. That misconception is driving a lot of the timeline assumptions across the board.

John

I have the DNS audit/report put together and ready to hand over when the time is right, but I can't meet today at noon. Per my conversation with Keara, the domain migration is being paused. The reason: my virtual CIO flagged real risk of taking Signature Advisor's Google Workspace email offline mid-migration, and we are already behind on client work because the Philippines Team was both our "service center" and our Agency Management System. Ironically, removing humans from my work flow broke what we build over many many years. I can not take he risk of email outage until we have Outlook cutover, service center restoration, and client-work catch-up need to land first. I'll send the DNS package when we're ready to execute, not before.

Mary

First, genuine thanks for dropping Thor's hammer on the PURE programs earlier this week. We would have had an uninsured property for a PURE member without that intervention.

Second, can we add three items to today's central zone agenda? Each one could take meaningful load off me and Crystal right now.

- Service center support prior to Epic being able to transact business (not after Epic and download allow us to transact business) Even when downloads start, there will be weeks of clean up and training to get crystal up to speed and the client work won't stop for training.
- Claims department support. Hail season is stacking open claims and we have no bandwidth. Can we get claims support so that this can be taken off our plate.
- A "stop doing" list. Our Epic training revealed we are doing dramatically more processing than we will need to once Epic transacts (e.g., sending renewal notices that carriers already send). Help us identify the redundant work so we can drop it now.

Happy to discuss any of this further. Appreciate everyone's patience as we sort the sequencing.

...Roper



---
Roper C. DeGarmo
Vice President Private Client Group
NFP, an Aon company | NFP.com <http://NFP.com>
Office: 913-904-1881
Cell: 913-210-9054
linkd.in/RoperDeGarmo <http://linkd.in/RoperDeGarmo>

On Tue Apr 21, 2026, 09:33 PM GMT, Roper DeGarmo <mailto:Roper@signatureadvisor.com> wrote:
> Hey John, I'm pretty sure we can do this in off hours asynchronously, leaving office hours for client work.
>
> I think I already have a draft DNS export report, but I want to spend a bit more time with your email to make sure you have everything you need. My plan is to move my personal domains out of the current Hover.com <http://Hover.com> account into a new one and hand you the keys to the old account.
>
> One note on GWS... we can't assume it's configured correctly just because it's working. I've been my own domain manager for years, and before AI that meant reading the FAQ for every little change. A few years back I set up a new domain correctly and it actually broke my email because GWS had been configured in a way that accommodated a previous misconfiguration. In other words, I know it's technically possible to move things around and keep them running, but it's not a risk I want to take if we're just waiting to deprecate GWS and move to Outlook anyway. Make sense?
>
> We'll get there. Thx for the detailed email 🙏
>
> Roper
>
> On Tue Apr 21, 2026, 06:21 PM GMT, John Seckner <mailto:john.seckner@nfp.com> wrote:
>> Roper,
>> At this time, I only need an export of your DNS settings so we can stage the following domains in the NFP registrar and review them in advance:
>> - TrustSPI.com
>> - SignatureAdviser.com
>> - SignatureAdvisor.com
>> This will allow me to analyze your existing DNS configuration to confirm everything is correct and help us identify any services that may not yet be documented.
>> At least 30 days prior to the Google Workspace cutover, these domains will need to be transferred so we can manage DNS during the transition. I’ll need full administrative control at that point to update DNS—specifically to change MX records so email is routed to Microsoft instead of Google on the night of cutover. This is also a security requirement, as NFP must have exclusive control over DNS for domains it manages.
>> To help put you at ease: transferring a domain from one registrar to another does not cause email or website downtime. The transfer itself does not modify DNS records; changes only occur when we intentionally update them during cutover.
>> For Thursday’s meeting, the goal would simply be to export your DNS records from Hover into an Excel format so I can review them and stage the equivalent records in NFP’s GoDaddy tenant. No changes would be made during that session.
>> Thank you
>> John Seckner
>> Integration Engineer
>> Technology
>> NFP, an Aon Company
>> P: 585-895-7363 | John.Seckner@nfp.com <mailto:John.Seckner@nfp.com>
>> From: Roper DeGarmo <roper@signatureadvisor.com>
>> Sent: Tuesday, April 21, 2026 1:15 PM
>> To: Keara Connelly <keara.connelly@nfp.com>; John Seckner <john.seckner@nfp.com>
>> Cc: Mary Mullen <mary.mullen@nfp.com>
>> Subject: Re: Weekly 1:1: picking a standing slot
>> ATTENTION - EXTERNAL EMAIL - The sender of this email is EXTERNAL to our email system. Do not click links or open attachments unless you recognize the sender and know the content is safe.
>> Let's do "Thurs: 10:30a-11a" ...
>> I have an 11 AM that day, but this is me asking @John Seckner <mailto:john.seckner@nfp.com> if we really need to meet if my preference is to just take down the two web pages we have at:
>> SignaturePersonalInsurance.com <https://t.shortwave.com/links/v1/Umzw47fUttFnt54X57ah5XvWVnKHX46W3ycEvnwhBq8c2f8z124JMFsbXM0Hm3CR59JKD4PlA8oP7oXgqCZ7wYT7bqAYeu5ZVRmTQmaM62U2kWn79YhjrQeYo_IH2QU3iIvt1qJe3-s2D4I-bO_qjqXnqWqZ2FiOfiWTfhWwqAA> (TrustSPI.com <https://t.shortwave.com/links/v1/iosbf-a0diE1XQwYlyetDOtKU527JeaLdG1hYiQvurMkd3mpDs2XSAkpoHSNMXHaUrLjsvIq0kkUb3kb3-fFrFz6I0yzGsXngg_J8BMCtjuUjTGPsLHyryIhetfNYuADgSpU2OK3FzohGqyTaqrwnFAdwScMFxfr8SKBW0G0rvE> redirects here)
>> SignatureAdvisor.com <https://t.shortwave.com/links/v1/n7ajHQi4qOpUO3K9AExXWlAvqN0R9GlIVY_whKavuNTL7oUbwi5i4gZ1E9D1xNVbA9Cc8BN4XccjsBwYRZRL5cUiCoCQbzusDfPM8qgijMXqLZWRhkIhJ8fUgmXHyiqsRouVL2c4Y_CI9QL1kNUVc1YVpn2Af5CCfmk7pHLaTZY>
>> There is no reason to port those... they can just be redirected to the NFP team page once it's live. And if you give me time, I can simply migrate my personal domains out of the current  Hover.com <https://t.shortwave.com/links/v1/YvPj12aSIFyqW7ajHRQfcVZVfdG_IajqV4cM62XzSM4l8DBt29x6IkEZd6Ps8fit-Zv95zH4h0rmOVCZjOLZhuZcp6J6SJ9jbCqzenzXxt_DKbln3KCXQLO7fgikkrVS0-7mlo3A-9TKasfQPFzTz9U0FGAUcXSjBEcwlUXDsTQ> Account and give you the keys. I don't want to move or change anything on them until we are out of Google Work Space because I don't want to risk messing up our emails, that would probably kill me if we had to trouble shoot something that mission critical. What do you think @John Seckner <mailto:john.seckner@nfp.com> can we push this until after Epic is truly active and the NFP Operations Service Team can start helping with our client work?
>> Thx all.
>> Roper
>> ---
>> Roper C. DeGarmo
>> Vice President Private Client Group
>> NFP, an Aon company |  NFP.com <https://t.shortwave.com/links/v1/QUpgR4uK7ZXbtdJ2at9JRHeJriQIbp5EJ6xMlQAqOuB2ySj0OerY1LYWezB-892F-mmqDBWfkcjnUP3dIYLhftOwHud38pl_AllAnnTyr_a_NEVBYS8HMTrdjMl3BGy8iXyaH4Mf3D1EPKW-IFlmHCRjDw0mBUMhY_MyGnyVxhg>
>> Office: 913-904-1881
>> Cell: 913-210-9054
>> linkd.in/RoperDeGarmo <https://t.shortwave.com/links/v1/Qf915WM_inipBSfBGRnYyNL5KfK63iJW7ErqRXEjI97jccWP2zcDRyEennBIe-HEFDg1wYhiqee4s6qSKfHc5YyyjVG41SvdskUMmHVrplL0UbLjcjPR7hqdEoyBcalo8o__shkLje5Tej6wkY3SEhCMw2FzQWVnXXPB-_zYtRA>
>> On Mon Apr 20, 2026, 03:44 PM GMT,  Keara Connelly <mailto:keara.connelly@nfp.com> wrote:
>>> Hi Roper
>>> Sounds good. I can match the following:
>>> Tues: 10:30a-11:30a ET
>>> Thurs: 10:30a-11a, 1p-2p ET
>>> Thanks!
>>> Keara Connelly
>>> M&A Integration Management
>>> NFP, an Aon Company
>>> 200 Park Ave | Suite 3202 | New York, NY 10166
>>> P: 703.342. 7190 |
```

**Why it matters:** Roper's email to Keara, John, Mary that triggered Mullen's recap. Three asks: (1) service center support before Epic transactions, (2) claims department support, (3) stop-doing list. Plus DNS migration pause to John Seckner. The integration-call skip and explicit naming of E&O exposure on client work.

### Travis 04/25 8:29am — Re: Weekly 1:1 (the Plan A vs Plan B fork)

**Date:** 2026-04-25 13:29:30+00
**Subject:** Re: Weekly 1:1: picking a standing slot
**Gmail ID:** 19dc4d4f4207069c

```
Curious how this email landed on you.  This feels very very encouraging to me to the point that it makes we wonder if we hold off on that other email that inserts me more directly.  I’m certainly still open to that but if this email from Mary feels like a little momentum to you then let’s keep that train going without disrupting and I can help triage and organize on the backside.   If you don’t feel that way then we can go with Plan B, or Plan C…
__________________
Travis Carpenter

On Apr 24, 2026, at 6:59 PM, Roper DeGarmo <Roper@signatureadvisor.com> wrote:

﻿FYI. Did not read

On Fri Apr 24, 2026, 10:59 PM GMT, Mary Mullen wrote:



Hi Roper,

 

As a summary from the Integration Recap call today as well as urgent items needed. I also believe Keara will be sending a recap); and perhaps Crystal/Tess was also able to update you. Items in red are responses or items needed.

M&A Open Items – High Priority



Mary Bamford will be looking for the April Landmark bank statement. 
Please upload by 5/1


There are several other items for which she is looking, but the April statement seems to be the most urgent. The next item below ties into some of her request.

Mail:
You mentioned that nobody has been covering the mail since the acquisition. (“So it's very likely there are statements sitting in the PO box or at my home address 5402 Birch that haven't been opened, scanned, or filed.”)


If you are comfortable sending the batches of unopened mail from the PO Box 
(you’ll need to ask the PO Box vendor to package and mail) as well as the items at your house that haven’t been unopened and are work related, we can ask our PRSC team to scan and get in order.

I will provide the proper address upon request



Service center support prior to Epic being able to transact business (not after Epic and download allow us to transact business) Even when downloads start, there will be
weeks of clean up and training to get crystal up to speed and the client work won't stop for training.
I have been working with Crystal to see if we can be added to your carrier portals now to see about processing changes for you while we wait for the codes to be tied together. In addition, Julie will follow-up Monday morning with Sam
Brown re carrier management (namely AIG and PURE) since we don’t have responses from them on codes being tied together which needs to happen before download can occur.

Claims department support. Hail season is stacking open claims and we have no bandwidth. Can we get claims support so that this can be taken off our plate.
I will check with Crystal on Monday to see how many claims (estimated) might be open on your desk right now. Justine’s team is willing to handle some of the claims follow-up in the interim (we spoke earlier), though your team will still
need to file the claims. I’m also curious about your current claims procedure – how often do you follow-up and how involved are you with the adjusters throughout the process?

A "stop doing" list. Our Epic training revealed we are doing dramatically more processing than we will need to once Epic transacts (e.g., sending renewal notices that carriers
already send). Help us identify the redundant work so we can drop it now. 
You can drop any sending of documents already provided directly from the carrier to the client. examples of this include sending any/all new/endorsements/renewals issued by admitted carriers (e.g. AIG, PURE, etc). As we discussed yesterday, this can be stopped
now so efforts can be re-directed elsewhere.

Coupa: Mary Bamford will request 18 mons of expenses from QuickBooks so we can scrub and indicate the vendors who need
to be set up in our recurring payment system Coupa. Once we have this list, we will need to gather W9 and ACH info from them. I scrubbed the 3 month list already and was able to narrow it down pretty easily. I think we’ll catch a few more on the deepened list,
but it shouldn’t be thousands of vendors, likely around 50, if not under.



A call has been scheduled for Monday. Please attend, or let the organizer know if you cannot attend and we will reschedule to include you.

Tess:
I’m excited to see how her license testing goes this weekend. Having her fully licensed will allow her to be more engaged with clients and help to free Crystal up. We should definitely plan to discuss how we expand her role
so that she’s taking work off of other plates.

I look forward to our call with Brett on Monday afternoon. Have a good weekend.

 

 

 

Best,

 

Mary

 


 

Mary Mullen, CAPI, CPRIA, ACPRIA

She/Her/Hers

Senior Vice President, Central Region Leader


Personal Risk

NFP, an Aon company


CA License #OF15715

500 West Madison Street | 32nd Floor | Chicago, Illinois 60661

P: 312.704.7000 | M: 312.493.2922 | F: 312.277.0025 |
mary.mullen@nfp.com | NFP.com

 

Insurance services provided through NFP Property & Casualty Services, Inc., doing business in California as NFP Property & Casualty
Insurance Services, Inc. License #0F15715. 



 



From: Roper DeGarmo <roper@signatureadvisor.com>


Sent: Thursday, April 23, 2026 12:05 PM

To: Keara Connelly <keara.connelly@nfp.com>; John Seckner <john.seckner@nfp.com>

Cc: Mary Mullen <mary.mullen@nfp.com>; Courtney Kendrick <courtney.kendrick@nfp.com>; Michael Deberry <michael.deberry@nfp.com>; Graham Bateman <graham.bateman@nfp.com>; Keith Clemons <keith.clemons@nfp.com>; Bob Johnston <bob.johnston@nfp.com>

Subject: RE: Weekly 1:1: picking a standing slot





 






ATTENTION - EXTERNAL EMAIL - The sender of this email is EXTERNAL to our email system. Do not click links or open attachments unless you
recognize the sender and know the content is safe.











Hi Keara, John, and Mary. A few items for each of you below.



 


Keara



 


Thanks for taking my call today. Wanted to get what we discussed in writing so we're all on the same page.



 




You're going to let John know the domain/DNS migration is paused for now. Those domains are not client-facing and there's no time sensitivity.







You're going to touch base with Mary and Marco, then set up a call with the three or four of us (me, you, Mary, Marco, and possibly Brett) to align on an integration path that doesn't keep creating E&O exposure on client work.






I'm going to skip tomorrow's integration call so you can lead it and deliver the message directly to the team: we are at a critical point on operations with client work.






The key thing I need you to carry into that conversation: we are NOT live on Epic. Epic is turned on, but there is no live policy data, no download, no claims support, no policy support, and no one on my team knows how to use it yet. That misconception
is driving a lot of the timeline assumptions across the board.



 


John



 


I have the DNS audit/report put together and ready to hand over when the time is right, but I can't meet today at noon. Per my conversation with Keara, the domain migration is being paused. The reason: my virtual CIO flagged real risk of
taking Signature Advisor's Google Workspace email offline mid-migration, and we are already behind on client work because the Philippines Team was both our "service center" and our Agency Management System. Ironically, removing humans from my work flow broke
what we build over many many years. I can not take he risk of email outage until we have Outlook cutover, service center restoration, and client-work catch-up need to land first. I'll send the DNS package when we're ready to execute, not before.



 


Mary



 


First, genuine thanks for dropping Thor's hammer on the PURE programs earlier this week. We would have had an uninsured property for a PURE member without that intervention.



 


Second, can we add three items to today's central zone agenda? Each one could take meaningful load off me and Crystal right now.



 




Service center support prior to Epic being able to transact business (not after Epic and download allow us to transact business) Even when downloads start, there will be weeks of clean up and training to get crystal up to speed and the client work won't
stop for training. 






Claims department support. Hail season is stacking open claims and we have no bandwidth. Can we get claims support so that this can be taken off our plate.






A "stop doing" list. Our Epic training revealed we are doing dramatically more processing than we will need to once Epic transacts (e.g., sending renewal notices that carriers already send). Help us identify the redundant work so we can drop it now.



 


Happy to discuss any of this further. Appreciate everyone's patience as we sort the sequencing.



 


...Roper










---




Roper C. DeGarmo




Vice President Private Client Group 




NFP, an Aon company | 
NFP.com




Office: 913-904-1881




```

**Why it matters:** Travis's reply to Roper's forwarded Mullen recap. Asks the strategic fork: hold Travis's Plan B email or fire it. This is what triggered the audit.

### Mary Bamford 03/30 — Ruben Brown Inquiry (the original 'why isn't NFP doing accounting' thread)

**Date:** 2026-03-30 22:44:34+00
**Subject:** RE: Ruben Brown Inquiry
**Gmail ID:** 19d40eba79ab0773

```
Hi Roper,

On Friday's integration call you told me to reach out to Rubin Brown.  Will you provide some more insight to the outstanding items preventing Quickbooks entries so perhaps I can assist w/ a work around process so the to meet our deadline?

Thank you,

Mary Bamford
She/Her/Hers
Assistant Vice President
West Region Accounting, Mergers & Acquisitions
NFP, an Aon Company
2300 Contra Costa Blvd | Suite 600 | Pleasant Hill, CA 94523
P: 925.279.4992 | F: 925.956.7601 | mary.bamford@nfp.com<mailto:mary.bamford@nfp.com> | NFP.com


From: Roper DeGarmo <roper@signatureadvisor.com>
Sent: Monday, March 30, 2026 3:25 PM
To: Mary Bamford <mary.bamford@nfp.com>
Subject: Ruben Brown Inquiry

ATTENTION - EXTERNAL EMAIL - The sender of this email is EXTERNAL to our email system. Do not click links or open attachments unless you recognize the sender and know the content is safe.
Hi Mary,

Jenny forwarded me a copy of this. Going forward, could you run these through me first?

They're waiting on me for some other questions, and it seems very unlikely we'll hit this deadline.

I'll review and report back but wanted to let you know there are more moving parts than this.

Regards,

Roper

---
Roper C. DeGarmo
Vice President Private Client Group
NFP, an Aon company | NFP.com<https://t.shortwave.com/links/v1/HlYNtHxbzOjGNH13CnbdKCKgEiqTZQGUNwt0DvabLA8hC1MweYMS3Jt00jVx_JwT3sj5GEfkROSqGyQxM26DE9_oJP5NnofPPnZr1yo9gfuck2UYHssuLnImEt24zQQGnQmsptZfIRy5QAmeBoWqZVryEjRDwTh3Tp57veOK2Mw>
Office: 913-904-1881
Cell: 913-210-9054
linkd.in/RoperDeGarmo<https://t.shortwave.com/links/v1/oBisA-VNLPb9mqz3xG2S4m5Bn5podNiKxTooyVF9vwMzSnQEqxBr7D-gpFJc3GGUyrZZlNns-ecULF3W6cN1YzZ8sztiE2CkWxx0Skde_cH4mq95uJF0o5DTFbPBr-qa9W_SgOrhPUxRmqkq6-pJz7Zs_8AJqIxwbAoZVuazxoQ>

This e-mail may contain information that is privileged, confidential or protected under state or federal law. If you are not an intended recipient of this email, please delete it, notify the sender immediately, and do not copy, use or disseminate any information in the e-mail. Any tax advice in this email may not be used to avoid any penalties imposed under U.S. tax laws. E-mail sent to or from this e-mail address may be monitored, reviewed and archived.
```

**Why it matters:** The earlier Bamford-Roper accounting exchange where Roper first questions whether QB-operator-Roper is the right model. Sets up the entire Bamford pattern.


---

## 8. Smoking Gun Transcripts (Full Text)

Recordings 190 (04/10) and 120 (02/27) chunks 8-9 / 85-86 are already embedded in Section 5. This section adds three more full transcripts that materially shape the diagnostic.

### Acumen peer session — 04/17 (Aon-bought-NFP-for-the-data outsider read)

**Date:** 2026-04-17
**Source:** soundcore-anker
**Anka ID:** 264
**Title:** Acumen peer session with hail damage client aside
**Duration:** 3559.4734s

**Excerpt (first 12 chunks):**

```
[chunk 0] Speaker 0: Record this. How are you? Hey. I'm good. How are doing? Why are you drinking Celsius?

Speaker 1: Because it it it's orange. So it's like orange juice, so this is healthy

Speaker 1: for the day.

Speaker 0: Told This was I told you you tricked me on that. Right?

Speaker 0: No. How did I trick you? When we met, you raved about them,

Speaker 0: and I thought, holy shit. If Wonder Kid is drinking those and they're they must be healthy. So I went and started drinking them. And I realized I was like, well, shit. This is just a monster you

Speaker 1: It's all relative. Yeah. It's heal

[chunk 1] Speaker 0: might involve include include the fact that I prefer not to be able to see the people I'm

Speaker 0: communicating to.

Speaker 1: It's so no. It's actually funny from a

Speaker 1: I don't love

Speaker 1: like, if truly, like, spending, like, one on one time with somebody, I would rather do phone calls than, like, a Zoom call. Yeah. FaceTime's a little different, but

Speaker 1: when I generally speaking, when people are on a phone, you have a 100% of their attention. Sometimes Zoom,

Speaker 0: you can drift to That's interesting. Light. Right? Yeah. That's really you're right. 

[chunk 2] Speaker 0: so alright. So

Speaker 0: let's let's just triage

Speaker 0: and

Speaker 0: yeah. I'm I'm your puppet, man. I'm I'm in. You

Speaker 0: I

Speaker 0: I got to laughing last night on the plane. I took a gummy. That helped.

Speaker 0: But,

Speaker 0: I I started flashing back to the two percent of the conversation with Mary that

Speaker 0: I wasn't fully aware of what I was saying. And in retrospect, I'm like, wow. That was fucking stupid.

Speaker 0: So so do you want my guesses as to the low points?

Speaker 1: Please.

Speaker 0: I got a life changing amount of money that I h

[chunk 3] Speaker 0: an actual cry for help.

Speaker 0: What happens is I slip off of the nice part of it and start, you know,

Speaker 0: demanding justice.

Speaker 0: And Yeah. It's the wrong audience. So I I

Speaker 0: can see all that,

Speaker 0: and I have

Speaker 0: very

Speaker 0: clear

Speaker 0: examples of

Speaker 0: when I think there are only

Speaker 0: limited options.

Speaker 0: It's it's a lot to do with my mindset right now. I just can't I can't see them all right now, and I'm trusting you to help me see more options.

Speaker 0: You know my priorities and you know the people I

[chunk 4] Speaker 0: that's enough word for word, and

Speaker 0: so the the term matters to me.

Speaker 1: Yeah. For sure it does. And, you know, what you're feeling or what I interpret your feeling is

Speaker 1: and what I would have wanted you to say to Mary, it's some version of, like, hey. Instead of, like, this, don't push me. Like, I can't that's not good for me is, hey. You'll get the best out of me when my priorities are clear Yeah. Which is what you wanted. Like and so that you want the best of Roper versus,

Speaker 1: hey. If you do this, you're gonna get the worst of Roper. Like, this is 

[chunk 5] Speaker 1: Yeah. So but, you know, something we could talk about later just just because I know you want that. You don't wanna, like,

Speaker 1: you know, see red and.

Speaker 0: No. No. I don't. And

Speaker 0: that's, I've made progress in,

Speaker 0: couples therapy around that,

Speaker 0: because

Speaker 0: it is like, my reactivity

Speaker 0: reduces

Speaker 0: options. I start I triage down to some, you know, pretty black and white things. So I know that.

Speaker 0: Yeah. It

Speaker 0: would be good if we had a

Speaker 0: yeah. I don't know. That that's a big one for me, and an

[chunk 6] Speaker 0: It's gonna be hard on her, I'm afraid, but I I know

Speaker 0: I can't stand in the way anymore. Like, I gotta let them figure it out.

Speaker 0: So

Speaker 1: What's the worst that could happen?

Speaker 0: That they

Speaker 0: that

Speaker 0: they take Crystal

Speaker 0: to the max and she doesn't quit.

Speaker 0: Like, the worst that could happen is not that she steps away and says this isn't for me.

Speaker 0: The worst is that she continues to

Speaker 0: not take care of herself.

Speaker 0: Like, if you heard at the end there, she's clearly on the edge

Speaker 0: and

[chunk 7] Speaker 1: in front of you, like, what good work looks like from Mary to Crystal, what communication cadence is, what what whatever those things are that are important to Mary that Crystal hears them. And, you know, like, let Crystal respond and work through that. And and if you notice that she's given 50% of her truth or response in part to what Mary's want, like, you know, you can interject and help guide, but, like, suggest that everybody hears that.

Speaker 1: And then that won't be perfect

Speaker 1: at first. Right? Like, they'll they'll need to probably be a couple more of those every

[chunk 8] Speaker 0: it's really hard to as you hear from in Crystal's voice too, it's really hard to to believe

Speaker 0: that that's going to happen

Speaker 0: on the track record of how they've things have gone so far. So I just have a hard time trusting that she can execute on what she wants.

Speaker 1: That Mary can execute or they could That Mary can execute.

Speaker 0: I mean, the that's the good example is, like,

Speaker 0: she's setting up these meetings on Monday, and it's more noise because she doesn't know how to send invites to us because we're not in Teams. And

Speaker 0: instead of

[chunk 9] Speaker 0: and Crystal to say we need to start advocating for Crystal's role in this. And they both said, no. No. No. No. Let's just get to closing. And then we're two weeks before closing, and Crystal was looking for the exit

Speaker 0: because it was too much, literally. Like, she she had it maybe that's, like, background you should know is I I've told her she has a year severance with me, and

Speaker 0: it didn't it just wasn't set up in a way that she could hold on to it as a safety net. It became an either or.

Speaker 0: She had she started thinking I either need to exit and take a yea

[chunk 10] Speaker 0: that to see it. So there's the worst that could happen.

Speaker 1: Gotcha.

Speaker 1: Well, I I I think the good news is,

Speaker 1: like, I think you

Speaker 1: can, you know, set that up for success with Mary, like, the the integration stuff aside. So assuming that's done, buttoned up, we've got through all the minutiae of that BS,

Speaker 1: and it is packed away. And we're just on the day to day, what is life like in NFP

Speaker 1: for Crystal and your team with Mary.

Speaker 1: And

Speaker 1: if I was with Mary, I would say, okay. Like, what what do you need, and how of

[chunk 11] Speaker 0: is

Speaker 0: was understood

Speaker 0: that

Speaker 0: we were all sunshine and rainbows up until close,

Speaker 0: tactically.

Speaker 0: And

Speaker 0: so now that

Speaker 0: and the reality is like Mary sort of hinted at that, like she did say maybe you should have made promises that to test

Speaker 0: like

Speaker 0: and I was like,

Speaker 0: okay. Fuck you. You have no idea what we were doing and you weren't there to help. And

Speaker 0: so

Speaker 0: like, the fact that Mary is going to realize

Speaker 0: from a service

Speaker 0: standpoint,

Speaker 0: this i

```

**Why it matters:** Roper's peer-group conversation with another Acumen member who articulates the deal structure clearly: 'Aon bought NFP because they're so good. They fill a gap that Aon doesn't have, and we want them to keep the brand and stay exactly as they are.' Then the consequential read: at some point they 'just push Jason's team down on top of NFP and leave it all inside of the NFP shell.' Outsider perspective on what 'no integration' actually looks like long-term. Useful frame for what Brett's incentives are.

### Internal prep meeting 04/24 — Tess role + service center model

**Date:** 2026-04-24 10:03:40
**Source:** plaud-email
**Anka ID:** 343
**Title:** Internal prep meeting - David Kozin Florida hurricane deductible review (4/24 client meeting)
**Duration:** Nones

**Excerpt (first 12 chunks):**

```
[chunk 0] 00:00:00
So, like, I think that's what he's going to care about most mostly.
Um, you know, like when I looked at like everything, Like the one
thing that jumped out at me was obviously the hurricane deductible,
because basically that's like almost like. Your, I don't call it self
insurance, But like twenty percent is like to me, like seems like a
really high retention. Yeah. And, like you know, if that's four
hundred and fifty grand.
00:00:30
I think if we can tell David like what that means in the sense of,
premium dollars to lower that to ten fifteen five see what those
options are. Which yo

[chunk 1] page for point one. No question. Um. The Florida condo renovation and
the art appraisals and collection discounts. I mean. I think that's
more so just again, an action item like just asking David to provide.
Any information that you need to better underwrite? Um, yeah, the the
renovation one we probably have a.
00:02:25
To disclose, as you know, the contract will anticipate it. Will the
contract will say, you know, David's required to disclose any
renovations over a certain threshold? I don't know how much renovation
he did, but the value is so high. I suspect he was. Tipping into the
required

[chunk 2]  is the main for the unit. So like. It might not be
applicable here, but I would just stress that the key in the insurance
world is. Flow-based automatic water shutoff.
00:04:19
So the flow based, meaning there is some way for the system to monitor
the amount of water moving through the main, which is where we fall
down in condos. Is sometimes there is more than one source coming into
the unit, and you can't do it. And that's what I was going to say. I
just don't know, like at a single family home, yes, easy. You know, in
a condo association, I think that's going to be difficult. Um However,
I

[chunk 3] we're, we're playing with a couple dials on if.
00:06:08
If it really is flat, We're also going to look at lower deductibles
and see what that would look like. So the But what we've still been
seeing, and this was echoed by our new NFP. Cohort in LA at the sales
conferences; these carriers all essentially know each other's. I won't
say price, but they know where they want to write and where they
don't. And so, this still in the market of. If you get a renewal, it's
very likely to be the best option in the private client space.
Nobody's pricing themselves to like be try to steal each other's
cu

[chunk 4] 08:03
So that's what I am. That's what I am thinking. It's like he's got
hurricane impact windows, so it's like. You know, Like if if it really
is gonna hit the fan in a sense of like a major, you know, storm. I am
sure he could even put up like shutters if he had to on top of the
hurricane. Yeah, impact glass, you know, to get himself like a better
protection. That that used to be an I mean his building doesn't
require any additional um. Protection. He's as secure as you can be.
Um, There used to be a provision for getting credit for a plan to
install panel, or you know the, you know, go boar

[chunk 5]  should be. Um, actually the what we're looking at
renewal right. If you just ran it, yeah, that should include all of
the renewals, including I think the Florida auto has renewed as well
for five twenty five. So um all of this year's renewals have renewed
now. That's what we were waiting for. So Josh I I couldn't remember
why. The numbers weren't right before, but that Florida auto is on a
different cycle and it should be. Okay, well, good. That tells us that
this year's renewal is approximately a nine point two percent
increase. Which is what we, yeah. So that's what I would have
expected. T

[chunk 6] Illinois? Yeah, because right now it's two point five. Uh, so it's a
combined limit. In Florida, so the the contents and and um additions
and all alterations. R, So the majority of what we're trying to pick
up in that two point two is just to get. All of the attached property
to the unit covered. We can look back at the inspection. Well, that's
what we're going to figure out at the inspection. Josh is we'll send
the inspector out and they'll try to give us two numbers. Well, they
only look at one.
00:12:53
They look at what would it cost to take this unit back to its current
state from probabl

[chunk 7] look at it all, but the idea is if he has a question, I, can we can
spin like flip right to the actual deck page and reference it. Yeah,
yeah. I mean, I think the deck pages more than enough for him. I think
it's more so just it's a it's it's less of a quantitative, It's a
qualitative discussion and then breaking down any qualitative issues
that are quantifiable. And you know, numbers stuff.
00:14:45
This is the quantitative report, and then our conversation is the
qualitative conversation about how he's protected. So, I do like
frankly. And I'll want to crystal just caught me this morning bec

[chunk 8]  that report because I think there
are some things in there. I'm not, I didn't check everything, but like
the contents for instance. Isn't matching up with the renewal, so I
think maybe you still have the old numbers in there for that. So just.
As a note, thus the giant draft. Yes, no doubt I need to show you
something, but like. It's not actually.
00:17:24
To just like throw all the policies at them either. So I no yeah that
we could work with. So yeah, well, our uh, Action items then are just
to quote the hurricane, everything else is pretty much in his court.
Yeah. And we'll keep it. Maybe 

[chunk 9] . That's what it
was, yeah. Every vehicle they own. Have you figured out? Actually,
here is the here is what you should be learning is.
00:19:18
The nine hundred pound gorilla gets credits that aren't available, and
so Sarah is doing everything she can to keep us. Report running
through her book like that. Downs fix is a thing that she'll get her
hands slapped for if they find it. But, she's willing to take the risk
to just make it work because I think also, she figured out that they
completely screwed us on that. And so she didn't really want to make
us deliver. Yeah. Yeah, yeah. I wrote her 

[chunk 10]  heart like, I know.
Yeah. Yeah. I wanna uh keep you shielded a little bit. Um, but I have
a meeting scheduled with Mary and Brett on Monday. That is what I'll
tell you. So, about Tess? No, about Mary. When Mary thinks. Oh, about
Mary. Okay. Yeah. Okay. Well, so I just as a head. Well, I think what
Mary thinks about all of us. I get the feeling she. For some reason,
Has the impression that either I am not doing the right things or I am
not working efficiently. Or so I just get that vibe from her. That. I
am not doing my job the way I should. Is what I got like, just stop
doing that. Basically,

[chunk 11]  she can't understand
why they feel like they're too heavy. And I don't know any other way
to ask for help, so we're just yeah, we're out of runway. Yeah. I will
voice just a small worry that I've had kind of all along, but um. I
don't know where discussions are with when Tess is going to be able to
be full time, but like part of me, This niggling worry inside of me is
worried that they're like you don't really need Tess and she's part
time anyway. I am not niggling; that is direct. You think that's real?
No, that is. That they feel that? Yes. Really? That we don't need her.
00:23:56
Um, and u

```

**Why it matters:** Roper-Crystal-Tess working session. Discusses Tess role expansion, service center model, what NFP can/can't take. Foundation for the Tess full-time conversation in baseline.

### Travis coaching call — Mary QuickBooks admin saga (recording 333)

**Date:** 2026-04-23
**Source:** soundcore-anker
**Title:** Hoffstaufer door-ding auto claim and acquisition update

**Excerpt (first 8 chunks):**

```
[chunk 0] Speaker 0: Today is Thursday, April 23 at 10:40AM.

Speaker 0: I'm gonna call Hoffstaufer

Speaker 0: back.

Speaker 0: It's spelled h o f f s t a u f f e r. Phone number is (617)

Speaker 0: 407-2632.

Speaker 0: Dial (617)

Speaker 0: 407-2632.

Speaker 0: Hello? Hey, Hoff. This is Roper DeGarmo. How are you today?

Speaker 0: Good. How are you, Roper? I'm doing well. Sorry to get back to you yesterday. I saw

Speaker 0: my team asked me about your account, and then I realized

Speaker 0: it looked like I missed a call. So

Speaker 0: it sounds like you had a a little door ding.

Speaker 1: 

[chunk 1] Speaker 0: may or may not be valuable to you. That that they're telling me you've got couple of glass claims already. And although, obviously, none of this is your fault.

Speaker 0: And if you ask a

Speaker 0: underwriter who is

Speaker 0: regulated

Speaker 0: by the state, they will tell you these

Speaker 0: types of claims don't affect pricing,

Speaker 0: but I can tell you from deep experience, they absolutely

Speaker 0: affect your ability to move carriers.

Speaker 0: And

Speaker 0: not that we plan on doing that. I just wanted to put that on this conversation on the table before 

[chunk 2] Speaker 0: in that world that you ever wanna talk about, we can go all anywhere you wanna go. So I just wanted to share the news, and you'll we'll probably send out an email in a week or two or a cup month or two probably.

Speaker 0: Great. So I'm happy to for that, for my clients and my team, and, we'll get this going for you.

Speaker 1: Great. Thank you, Robert. Thanks, Hoff. Take care. You too. Bye bye. Bye bye.



```

**Why it matters:** Roper-Travis processing the Bamford QuickBooks admin handoff in real-time. Source for the explicit owner=Mary Bamford evidence in Finance reconcile. Captures Travis's coaching frame in the moment.


---

## 9. The Brett Play (Monday 3pm)

### Opening

> "Brett, I want to walk you through what I'm seeing on integration so we can decide together what to do about it. I'm not here to complain. I'm here to surface a structural problem early so we can fix it before it compounds."

### The sequencing thesis (lead with what's working)

> "On the client-work side, I trust the sequencing. Codes tied, downloads flowing, service center picking up cases — I see that path. Sam Brown is pushing AIG/PURE for code-tying — AIG/PCS auto-downloads went live 2/27. Mary Mullen got me service-center support and claims-team help via Justine. Coupa is being properly scoped. AmEx and Concur are operating — Jackie Searles owns. Workday GL is created and mapped. Brandon Jackson and Tracy McClain delivered email security cleanly. That's all real. I want to acknowledge it before I raise the harder question."

### The names ask

> "On the back-office side, I need names. I rebuilt the integration milestone view this weekend using every email, calendar event, and transcript touching NFP since 2/17. 137 milestones across 9 functions. 25 of them are tagged Ownership Vacuum — meaning either no NFP person owns them or NFP is asking me to own them. I appear as Owner on 27 percent of the integration milestones, most of which should be NFP."

> "Specific examples I need names on:"
> 
> - "**Mail.** PRSC scan was offered if I package and ship the PO Box backlog. But who owns ongoing mail handling at NFP for the SPI entity? When new mail arrives at the PO Box or 5402 Birch, who is the right person to send it to?"
> - "**QuickBooks.** Mary Bamford has accounting firm access since 2/25. She's still asking me to upload source documents for transactions she can pull from QBO directly. The 4/24 SharePoint demand was 15 line items, several of which were duplicates of her 4/06 ask. Who at NFP actually operates the books for the SPI entity going forward?"
> - "**Licensing.** Lisa Black told me on 03/04 that NFP/RegEd will not handle agency licenses because asset purchase. Sam Brown told me on 04/10 that broker-of-record transitions only happen at policy renewal. So 46 SPI agency entity licenses have to stay active for the rolling renewal cycle plus the 6-year E&O tail. NFP needs them active. NFP refused to absorb them. I'd have to hire a third party. That's not asset purchase scope. That's an operational obligation NFP needs but isn't paying to maintain. Who is the right person at NFP to take this conversation to?"
> - "**Carrier intel.** AIG announced the Collector Auto reclassification in March. Mary Mullen forwarded the notice to Stephanie Brock (another producer) but not to my code. Tess only got it on 4/7 after explicitly emailing Mary to ask. Same pattern on Chubb DNR + NY hurricane bulletins. Who is responsible for ensuring carrier communications reach my code proactively?"

### The decision tree

| Brett response | Read | Action |
|---|---|---|
| Names specific people / owns the QuickBooks question / commits to a back-office takeover plan with dates | Sequencing problem with real momentum to solve | Plan A confirmed. Travis stays in wings. Roper continues. |
| Vague "we'll figure it out" / pushes to Mary or Keara / treats it as producer-comfort | Structural problem; NFP doesn't have the back-office absorption model | Travis Plan B email goes Tuesday morning |
| Aggressive / defensive / "you knew what you signed up for" | Worse than structural; NFP doesn't intend to do the handoff | Plan C decisions about compensation/role/exit |

### What NOT to lead with

- The 27% Roper-as-owner number. Save for the closing if Brett is engaged.
- The Bamford pattern by name. Stay above the personality layer; talk about the QuickBooks ownership question structurally.
- The 6-year shell timeframe. Mention it once if Brett pushes back on agency licenses being SIG's responsibility forever.

### What to have ready in your back pocket

- The xlsx milestone view. Hard copy or screen-share if Brett asks "show me."
- The agency-license timeline (Section 5). Cleanest single example.
- The names list. If Brett asks "who do you want me to talk to?" — answer is Mary Bamford, Lisa Black, Rajulla Nadar, Sam Brown specifically.

---

## 10. What I Want From You

1. **Pressure-test the trichotomy.** Sequencing, Ownership Vacuum, Dark Variant — accurate, or am I being generous to NFP somewhere? Or harsh?

2. **Stress test the Brett opening.** Does "I'm here to surface a structural problem early" land as principled, or is it leadership-speak Brett will see through?

3. **The names ask.** Right wedge, or should I lead with the agency-license example since it's the cleanest case?

4. **Plan B trigger criteria.** "Vague / defers / treats as producer-comfort" → fire your direct email Tuesday. Right line, or too sensitive / not sensitive enough?

5. **The 6-year E&O coupling.** I think the agency-license + back-office burden is materially undervalued in the deal we signed. Do you read it that way, or is this normal acquisition friction?

6. **What happens if Brett says "we don't have anyone for that yet, but we're working on it"?** Is that Plan A (sequencing, give time), or Plan B (vacuum, escalate)? The line between those two interpretations is where I most want your read.

7. **Is the 27% number too aggressive to put on the table?** It's accurate but it sounds adversarial. Lead with it, save it, or skip it entirely?


---

## 11. Appendix: Data Sources & Methodology

### Repositories
- `~/repos/nfp-integration/` — the active integration repo
  - `Signature Integration Milestone View — Roper Update 2026-04-26.xlsx` — refreshed milestone view (output)
  - `Signature Integration Milestone View — Roper Update 2026-04-14.xlsx` — prior baseline
  - `diagnostic.db` — working SQLite (1,573 source items, 137 milestones, ~700 evidence rows)
  - `scripts/` — extract + cluster + reconcile + xlsx generation pipeline
  - `DIAGNOSTIC-PLAN-2026-04-26.md` — technical plan (reviewed by Willison patterns + Codex technical check)
  - `TRAVIS-BRIEFING-2026-04-26.md` — this document

### Source databases
- `~/Documents/Palmer-Export/emails.db` — 702,500 messages, FTS5 indexed, current through 2026-04-26 20:15 UTC
- `~/Documents/Transcripts/anka.db` — 378 recordings (84 NFP-tagged), FTS5 + vector search
- Google Calendar via MCP (74 NFP-related events extracted to JSONL)
- Bamford 04/24 screenshots OCR'd via Claude vision

### Pipeline
1. **Extract** — keyword-prefiltered source items into `source_items` table (1,573 rows after dedup)
2. **Cluster** — 8 parallel Claude Sonnet 4.5 subagents, one per Function, classified each source item as `linked` / `new_milestone` / `noise` against baseline. ~1,880 cluster decisions.
3. **Reconcile** — 9 parallel Claude subagents (one per Function, including Finance pilot), produced final Status / Owner / Owner Basis / Owner Confidence / Notes / Problem Type / Next Action per milestone. Wrote `current_milestones` (137 rows) and `milestone_evidence` (~700 rows).
4. **Eval** — quality checks before xlsx generation.
5. **Generate** — xlsx via openpyxl, briefing via this Python script.

### Eval criteria (every output milestone row checked against)
- Has Function (matches one of the 9 canonical categories)
- Owner is named NFP person OR explicit "unassigned" with rationale
- Status reflects most recent evidence date, not last update
- At least one row in milestone_evidence cites this milestone_key
- Problem Type assigned
- Next Action exists or row is closed
- If new row: backed by ≥2 evidence items
- If Owner blank/unassigned, that blank is itself the diagnostic (note must call it out)

### Suppressions applied
- Pre-acquisition payroll wires for Crystal & Tess ($22,262.30 + $7,731.14): Roper-personal bonus payments, out of NFP acquisition scope.
- Roper Personal/SPI 2025 tax return + Q1 estimates: Roper-personal LLC management work, out of NFP scope.

### Methodology decisions worth flagging
- **Bamford pattern:** when cluster agents tagged owner=Mary Bamford with explicit basis, we audited the underlying email. If Bamford's "ownership" was *demanding from Roper* (asking for documents she should have access to), reconcile retagged owner as Roper with Ownership Vacuum problem type. Bamford is the demand source, not the delivery owner.
- **Counter-example tracking:** explicitly logged delivery-owner positives (Brandon Jackson, Tracy McClain, Riana Sherwood, Christopher Sam, Jackie Searles, Andria Griffin, Alma Ko, Lisa Black for individual licenses) so the briefing wouldn't read as one-sided.
- **Multi-link allowed:** a single source item can link to up to 3 baseline milestones if it touches multiple. This is why 1,573 source items produced 1,880 cluster decisions.

### Costs
- LLM cluster + reconcile pass: ~9 parallel subagents × ~150K tokens each = ~1.4M tokens. Cost approximately $40-60 depending on Claude pricing.
- Wall clock: ~3 hours from project kickoff (corrected Stage 0) to xlsx + briefing.

### Known limitations
- Email schema (Palmer) lacks separate from/to/cc columns. We FTS-matched `@nfp.com` substring, which catches headers in body_text. False positive rate ~10-30% on noise items (handled by cluster pass).
- Transcript attribution fuzzy on team meetings (multi-speaker, often unidentified).
- Airtable extraction was not completed in this run; manual MCP queries used for spot-checks.
- Bamford-side SharePoint folder contents not directly inspected; relied on Bamford's own enumeration of asks.
- NFP-side Outlook calendar invites only visible via accepted/declined events on Google Calendar.

### Reproducibility
- All scripts in `~/repos/nfp-integration/scripts/`
- Each is idempotent (UPSERT on stable keys: gmail_message_id for emails, anka_id for transcripts, milestone_key for milestones)
- `diagnostic.db` is gitignored; schema and audit log are committed
- Re-run as new evidence lands: `00-discovery.sh` → `1*-extract.sh` → `25-prefilter.sh` (TODO) → `30-cluster.sh` → `40-reconcile.sh` → `60-generate-xlsx.sh`

### Acknowledgments
- Methodology shaped by Willison CIO patterns (sqlite-utils + llm CLI + Datasette stack, eval-before-publish, Templates over Documentation)
- Technical plan hardened by Codex review (FTS over LIKE, milestone_evidence join table over comma-separated, MCP precompute step, owner-attribution 3-field model, csv-diff stable keys)
- Roper provided structural lens (sequencing vs ownership vacuum vs dark variant; agency-license dark-variant identification)

---

*End of briefing. Roper available for live discussion. Questions, corrections, and pushback all welcome.*
