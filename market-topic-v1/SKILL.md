---
name: market-topic-v1
description: Discover, cluster, deduplicate, score, rank, and structure evidence-backed industry blog topics with separate Trend and Evergreen engines. Use for daily or weekly industry/news scanning, monthly knowledge audits, B2B topic discovery, content-gap discovery, buyer-question discovery, Topic Scout or Topic Scorer work, cannibalization checks, Topic Intelligence Graph maintenance, Feishu topic-queue output, or implementation through Claude Code, Codex, OpenClaw, and n8n. Stop at scored topic recommendations; do not create a Research Pack, SEO brief, article, visuals, or publication.
---

# Market Topic V1

Convert industry intelligence into traceable, scored blog-topic recommendations:

`Sources -> Signals -> Events / Knowledge Gaps -> Topic Concepts -> Governance -> Scores -> Rankings -> Human Review`

Operate two independent engines:

- **Trend Engine:** detect time-sensitive changes, events, questions, and buyer concerns.
- **Evergreen Engine:** detect durable knowledge, purchasing, technical, application, comparison, and FAQ gaps.

## Boundary

End at `Topic Score` and a structured handoff candidate. Treat Researcher as a separate skill.

Never:

- create a Research Pack, SEO brief, article, visual, social post, or publication;
- promote a topic to `HANDED_TO_RESEARCHER` without human approval;
- treat article count, views, Trends index, PAA, or discussion volume as sales evidence;
- invent search volume, keyword difficulty, CPC, traffic, market size, growth, prices, regulations, or company facts;
- move research, governance, or scoring logic into n8n. Use n8n only for scheduling, transport, retries, storage, and notifications.

## Load the operating resources

Read these files before execution:

1. `references/workflow.md` — run modes, complete sequence, lifecycle, error handling, and quality gates.
2. `references/source-strategy.md` — seven source functions, trust tiers, query planning, and evidence rules.
3. `references/topic-generator.md` — knowledge map, buyer journey, topic types, angle library, and title rules.
4. `references/governance.md` — fingerprinting, deduplication, cannibalization, graph relationships, and memory.
5. `references/scoring.md` — Trend, Blog Value, Priority, boosts, penalties, bands, and rankings.

Read conditionally:

- Read `references/feishu.md` before creating, mapping, or updating Feishu Bitable records.
- Read `references/orchestration.md` when implementing or running the skill through Claude Code, Codex, OpenClaw, or n8n.

Use these machine-readable resources:

- `schemas/input.schema.json` — normalized job configuration.
- `schemas/output.schema.json` — complete run output contract.
- `templates/config.example.yaml` — reusable starter configuration.
- `templates/result.example.json` — minimal valid output fixture.
- `scripts/calculate_scores.py` — deterministic score totals, bands, and special queues.
- `scripts/validate_output.py` — structural and arithmetic validation without external packages.

## Input

Accept YAML, JSON, a Feishu record, or a natural-language brief. Normalize to `schemas/input.schema.json`.

Require:

- `industry`
- `product`

Ask only when missing target market, target customer, or buyer role would materially change the result. Otherwise infer conservatively and record every inference in `run.assumptions`.

Apply the business-objective priority in this exact order:

1. Potential-customer interest
2. Commercial conversion relevance
3. Expertise / EEAT value
4. SEO opportunity
5. Trend speed
6. Social shareability

Do not let traffic or virality override buyer and commercial relevance.

## Run modes

- `daily`: scan the last 72 hours, compare equivalent prior windows, and prioritize Breaking/Trending signals.
- `weekly`: combine seven-day trend evidence with 14-90-day emerging patterns, Evergreen gaps, competitor gaps, and cannibalization cleanup.
- `monthly`: run a light Knowledge Audit; expand the map, rescore old topics, archive declining items, and inspect pillar/supporting gaps.

Support `focused` and `deep` scan depth. Treat collection volumes as ceilings, never quotas. Never fabricate or pad results.

## Execution

Follow this order without skipping governance:

1. Validate and normalize the input.
2. Load available Signals, Events, Topics, Knowledge Map, published content, approved topics, research queue, and rejected/archive memory.
3. Build a source plan for the requested market and languages.
4. Run Trend Engine and Evergreen Engine independently when required by the run mode.
5. Normalize, clean, and classify raw signals.
6. Cluster articles into events; treat articles as evidence and events as Topic Generator inputs.
7. Identify Evergreen knowledge gaps.
8. Generate Topic Concepts before titles.
9. Create Topic Fingerprints and compare every topic with all available topic memory.
10. Assign duplicate and cannibalization status.
11. Score Trend, Blog Value, base Priority, boosts, penalties, and Final Priority.
12. Generate a restrained suggested title only after governance and scoring.
13. Build three category rankings and Overall Top 10.
14. Validate the output, then write authorized Feishu records or return JSON and CSV-ready tables.

## Evidence requirements

- Use live search for current events, SERPs, regulations, company activity, and competitor coverage.
- Preserve original URL, publisher, publication date, event date, first-seen time, language, and market.
- Separate `FACT`, `SIGNAL`, `INFERENCE`, and `HYPOTHESIS`.
- Prefer primary sources for legal, regulatory, statistical, technical, safety, and company claims.
- Retain independent secondary sources as corroborating evidence.
- Use community and creator sources to discover concerns and language, not to establish hard facts.
- Keep unavailable SEO metrics `null`; never estimate them silently.

## Output

Return:

1. valid JSON matching `schemas/output.schema.json`;
2. a concise summary in the user's language;
3. rankings for:
   - Breaking / Trending Top 5
   - Buyer / Commercial Top 5
   - Evergreen Top 5
   - Overall Top 10
4. coverage gaps, assumptions, partial-run status, and errors;
5. reproducible component scores and all applied boost/penalty rules.

Use stable IDs:

- `signal_id`: stable hash or deterministic key for one canonical source item;
- `event_id`: stable key for one clustered real-world event;
- `knowledge_id`: stable key for one Knowledge Map node;
- `topic_id`: stable key derived from the Topic Fingerprint.

Preserve lineage:

`Source -> Signal -> Event / Knowledge Gap -> Angle -> Audience -> Intent -> Topic Concept -> Score -> Suggested Title`

## Deterministic checks

After generating a result:

1. Run `scripts/calculate_scores.py` for any topic whose totals were not calculated deterministically.
2. Run:

   `python3 scripts/validate_output.py result.json`

3. Fix every `ERROR` before delivery.
4. Disclose remaining `WARNING` items as coverage limitations.

The scripts verify arithmetic and structure; they do not replace evidence judgment, source verification, semantic deduplication, or human approval.

## Completion gate

Do not finish until:

- the requested engines ran for the selected mode;
- every topic has customer, role, buyer stage, intent, angle, market, rationale, and lineage;
- every event has a canonical source and usable evidence;
- topics were generated from events or knowledge gaps, not copied article headlines;
- all available topic-memory stores were checked;
- scoring arithmetic and bands are reproducible;
- missing metrics remain `null`;
- rejected and merged topics retain reasons;
- Feishu writes, when requested, are verified without overwriting human-owned fields;
- no downstream Researcher or writing work was performed.
