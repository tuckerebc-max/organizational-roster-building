---
name: organizational-roster-building
description: Define a sector and geography, identify a comprehensive and prominent universe of organizations, and build a current, evidence-backed roster with formal names, websites, missions, organization type, geography, prominence rationale, identifiers, and source URLs. Use when Codex must scan a market or field such as educational philanthropy, education technology, venture capital, private equity, associations, nonprofits, or public agencies; coordinate low-cost research subagents; process starting source lists or downloads; create resumable batches; or deliver auditable CSV/XLSX and narrative reports without guessing facts.
---

# Organizational Roster Building

Build a defensible organization universe quickly, then verify it systematically. Optimize for verified organizations per unit time, not exhaustive narrative about each candidate. Keep the sector, geography, date, inclusion rules, and output schema explicit so a later researcher can repeat or extend the scan.

## Default operating model: discover fast, verify in parallel

Use two distinct passes:

1. **Rapid discovery pass:** collect plausible in-scope organizations from starting sources and targeted authoritative discovery sources. Capture only a stable candidate ID, name as found, URL/domain, source, subcategory, geography, and a one-line inclusion reason.
2. **Verification pass:** independently verify the highest-priority candidates first, then work through the remaining candidates in parallel batches. Complete the canonical schema, source URLs, currentness, identity relationships, and confidence during this pass.

Measure progress as `verified included organizations / elapsed research time`, with secondary measures for candidate coverage, evidence completeness, and unresolved rate. Do not let a difficult candidate block a batch: move it to the exception queue and continue.

Prefer parallel, independent batch work with one standard prompt and one schema. Review at batch checkpoints, not item-by-item. Automatically accept records that pass validation; reserve coordinator attention for conflicts, low confidence, scope ambiguity, and high-impact omissions.

## Start with a research contract

Before browsing or downloading, write a short research contract containing:

- **Sector definition:** what counts, what does not, and relevant sub-sectors.
- **Geography:** country, states/regions, headquarters versus operating presence, and cross-border treatment.
- **Goal:** “complete a comprehensive and rigorous scan of prominent organizations in the defined sector and geography as of [date].” Do not claim absolute completeness; define the evidence-based stopping rule.
- **Prominence rule:** use a transparent combination of sector recognition, scale, market activity, institutional role, public visibility, or inclusion in authoritative directories. Never rank only by search-engine order.
- **Starting sources:** user-provided files/URLs plus a planned source map covering official registries, associations, regulators, funder/industry directories, and reputable sector publications.
- **Required fields:** minimum canonical schema and any sector-specific extensions.
- **Freshness window:** normally verify current identity and operating status within 12 months, or explain why an older source remains authoritative.
- **Deliverables:** canonical data, source ledger, coverage memo, unresolved-items log, and optional report.

If the contract is missing a material choice, make a conservative assumption and record it. Ask the user only when the choice would materially change the universe or permit a consequential external action. Do not pause ordinary research for optional preferences.

## Use the coordinator/subagent architecture

The coordinator should own the research contract, universe design, deduplication, schema, source policy, progress ledger, approvals, merge, and final audit. Subagents should perform bounded evidence collection, not redefine scope or merge records.

Use a low-cost coordinator to:

1. parse the contract, create a source map, and establish the approval envelope;
2. run a rapid discovery pass across all starting sources before deep verification;
3. normalize and conservatively deduplicate candidates using names, domains, parent/affiliate signals, and identifiers;
4. score candidates for verification priority using prominence, fit, source strength, and expected research effort;
5. partition candidates into stable batches, normally 20–40 organizations or a user-specified size;
6. dispatch independent, parallel research batches using the same structured prompt;
7. automatically validate, accept, and merge clean records at batch checkpoints;
8. route only exceptions, conflicts, low-confidence rows, and coverage gaps to coordinator review;
9. run coverage and completion checks and produce the final roster and evidence report.

Do not ask subagents to infer missing emails, legal entities, ownership, investment focus, or prominence. Use explicit null/status values such as `Not publicly located`, `Unclear`, `Not applicable`, `Inactive`, or `Candidate - needs review`.

## Coordinator prompt

Use this prompt as the base, replacing bracketed values:

> You are the coordinator for an organizational roster project.
>
> Sector: [sector definition]. Geography: [geography]. Research date: [YYYY-MM-DD]. Goal: [goal]. Prominence rule: [rule]. Required fields: [fields]. Starting sources: [files and URLs]. Freshness window: [window].
>
> First run a rapid discovery pass across the supplied sources and targeted authoritative sources. Create a candidate ledger quickly; capture only candidate key, name, URL/domain, discovery source, subcategory, geography, and inclusion rationale. Do not perform deep verification during discovery. Then normalize names/domains, identify likely parent/affiliate relationships, deduplicate conservatively, and assign verification priority. Do not silently exclude a plausible prominent organization; place uncertain cases in an exception queue.
>
> Split the candidate ledger into stable batches and dispatch independent research subagents without waiting for item-by-item review. Assign the exact candidate rows and the schema below. Require one structured record per organization, one or more supporting source URLs for every material claim, a confidence/status value, and concise notes explaining ambiguity. Subagents must use current public sources, prefer primary/official sources, never rely on snippets alone, never fabricate or infer facts, and return `Not publicly located` when a field cannot be verified. A difficult record must be marked for exception review rather than blocking the batch.
>
> At batch checkpoints, automatically validate required fields, URLs, duplicates, entity identity, currentness, and evidence coverage. Merge clean records immediately. Route only failed validation, conflicting identity, low-confidence, scope-ambiguous, and likely-missing-prominent organizations to the exception queue. Resolve conflicts using the newest authoritative evidence and retain the discarded/conflicting source in notes. At completion, report candidate counts, verified included organizations per hour, included/excluded/deferred counts, source coverage by source class, unresolved items, and limitations. Do not label the universe “complete” unless the documented stopping rule is satisfied.

## Subagent prompt

Give each subagent only its assigned batch, the contract, the schema, and the research protocol:

> Research the assigned organizations for the [sector] roster in [geography] as of [date]. Return exactly one record per assigned organization, preserving the supplied candidate key. Confirm the formal/current name, official website, organization type, headquarters/geography, quick mission or role summary, and any sector-specific fields. Capture the exact supporting URL for each material field or group of fields. Prefer the organization’s official site, government/regulatory filings, authoritative registries, and reputable institutional sources. Open sources rather than relying on search snippets.
>
> Distinguish legal name, brand/DBA, parent, fund, portfolio company, chapter, and affiliate. Do not merge similarly named entities without evidence. Do not guess emails, people, assets, fund size, ownership, status, or strategy. Use controlled null/status values and explain uncertainty. Return JSON or CSV matching the schema, plus a short batch evidence note.

## Canonical roster schema

Use these core columns unless the user supplies a compatible schema:

1. `Roster Record ID`
2. `Formal Organization Name`
3. `Public/Brand Name`
4. `Organization Type`
5. `Sector Subcategory`
6. `Official Website URL`
7. `Primary Geography`
8. `Other Relevant Geography`
9. `Quick Mission / Role`
10. `Prominence Tier`
11. `Prominence Rationale`
12. `Parent Organization`
13. `Affiliate / Fund / Brand Relationship`
14. `Legal or Regulatory Identifier`
15. `Operating Status`
16. `Founded Year`
17. `Key Sector-Specific Fields`
18. `Primary Evidence URL`
19. `Additional Evidence URLs`
20. `Evidence Checked Date`
21. `Confidence`
22. `Research Notes`

Use one row per organization, not one row per source. Use a separate source ledger when several pages support one record. Preserve exact names and titles from sources; normalize only in dedicated normalized fields. Store clean canonical URLs, not search-result URLs or tracking wrappers.

## Evidence and source rules

Prefer, in order: official organization pages and filings; government and regulator records; authoritative membership or accreditation directories; institutional partners and funders; reputable journalism and sector research. Use a secondary source to discover a candidate, then seek primary confirmation.

For nonprofits, verify legal identity and status through the relevant regulator or tax-exempt registry where material. For investment advisers and funds, distinguish adviser, management company, fund, and portfolio company; use regulatory disclosures where applicable. For public companies, use official filings and issuer pages. For every sector, adapt the source hierarchy rather than treating one database as a complete universe.

The IRS Tax Exempt Organization Search provides official status/filing data and bulk downloads, but its listing limitations mean it cannot alone establish a complete nonprofit universe. SEC IAPD provides adviser search, Form ADV, and downloadable adviser data; SEC EDGAR provides public filing search. Use these as verification layers when relevant, not as substitutes for sector discovery.

## Front-load approvals; avoid just-in-time interruptions

At kickoff, state one consolidated operating envelope covering public web research, reasonable downloads, local working files, parallel subagents, batch size, source-count or time budget, and output location. Record the envelope in `research_contract.md` and proceed independently within it. Do not ask again for routine actions already covered by the envelope.

Treat these as normally safe within the user-provided workspace, while still recording them in the project log:

- reading user-provided files;
- browsing public pages;
- downloading a reasonable number of public source files into a project-specific folder;
- creating manifests, ledgers, batches, CSV/XLSX, Markdown, or audit files in the workspace.

Pause only for actions outside the envelope: bulk downloads beyond the stated limit, paid or authenticated sources, contacting organizations, sending messages, creating external accounts, writing outside the workspace, or a material scope change. Never delete or overwrite source files or prior ledgers without explicit authorization; create a new version or batch folder instead.

## Exception queue and autonomous completion

Maintain `exception_queue.csv` with `Candidate ID`, exception type, evidence already checked, next best action, priority, and status. Allowed exception types include `IDENTITY CONFLICT`, `SCOPE UNCLEAR`, `CURRENTNESS CONFLICT`, `MISSING PRIMARY SOURCE`, `PROMINENCE UNCLEAR`, `DUPLICATE REVIEW`, and `SOURCE FAILURE`.

Process exceptions in priority order after clean batch records are merged. Use a bounded retry rule: one targeted second search and one alternative source class; then mark `NEEDS_REVIEW` with a concise explanation. Never spend unlimited time on one organization. Finish with a complete disposition for every candidate, even if the disposition is deferred or unresolved.

## Batching, resumability, and handoffs

Create:

- `research_contract.md`
- `candidate_ledger.csv`
- `source_ledger.csv`
- `batch_manifest.csv`
- one immutable input file per batch
- `progress.json` or `progress.csv`
- `unresolved_items.csv`

Preserve candidate order and stable IDs. Save after discovery and after every batch checkpoint. Record `NOT_STARTED`, `IN_PROGRESS`, `VALIDATED`, `NEEDS_REVIEW`, or `COMPLETE`. A resumed run must continue from the first incomplete batch without changing prior validated rows. Keep raw subagent returns separate from canonical merged data. Do not wait for all batches before saving progress.

## Audit and completion criteria

Do not publish a roster as complete until:

- every candidate has an inclusion, exclusion, or defer decision;
- the discovery pass is complete before the final verification pass is closed;
- every included organization has a unique stable key and resolved entity identity;
- every required field is populated or has an allowed status value;
- every material claim has at least one supporting source URL;
- currentness was checked as of the research date;
- duplicates, parent/affiliate relationships, and inactive entities were reviewed;
- source coverage spans the planned source classes;
- subagent outputs passed schema and URL validation;
- unresolved items and limitations are disclosed;
- counts in the report reconcile to the canonical data.

Report efficiency metrics: candidate count, included/verified count, elapsed time, batches completed, verified organizations per hour, exception count, and percentage of included rows with primary evidence.

Use `scripts/audit_roster.py` for deterministic checks on a CSV roster. Use `references/research-protocol.md` for the detailed evidence protocol and stopping rule, and `references/source-map-and-coverage.md` for source planning, prominence, and coverage assessment.
