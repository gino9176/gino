---
name: market-topic-v1
description: Discover, cluster, deduplicate, score, rank, and structure evidence-backed industry blog topics with separate Trend and Evergreen engines. Use for daily or weekly industry/news scanning, monthly knowledge audits, B2B topic discovery, content-gap discovery, buyer-question discovery, Topic Scout or Topic Scorer work, cannibalization checks, Topic Intelligence Graph maintenance, or Feishu topic-queue output. Stop at scored topic recommendations; do not create a Research Pack, SEO brief, article, visuals, or publication.
---

# Market Topic V1

Build an industry-intelligence-to-blog-topic pipeline:

`Sources -> Signals -> Events / Knowledge Gaps -> Topic Concepts -> Governance -> Scores -> Rankings -> Human Review`

Operate two engines in parallel:

- **Trend Engine:** detect time-sensitive events, changes, questions, and buyer concerns.
- **Evergreen Engine:** detect durable knowledge, purchasing, technical, application, comparison, and FAQ gaps.

## Scope boundary

End at `Topic Score` and a structured handoff candidate. Researcher is a separate skill.

Do not:

- produce a Research Pack, content brief, article, social post, visual, or WordPress draft;
- promote a topic to `HANDED_TO_RESEARCHER` without human approval;
- treat an article, view count, Trends index, PAA result, or social discussion as sales evidence;
- invent search volume, keyword difficulty, CPC, traffic, market size, growth, prices, regulations, or company facts;
- move scoring or research logic into n8n. Let n8n schedule this skill, pass configuration, and store returned JSON.

## Input contract

Accept YAML, JSON, a Feishu record, or a natural-language brief. Normalize it to:

```yaml
industry: required
product: required
target_market:
  primary: []
  secondary: []
target_customer: []
customer_roles: []
business_model: B2B
website: null
competitors: []
languages: []
run_mode: daily        # daily | weekly | monthly
scan_depth: focused    # focused | deep
feishu_destination: null
seo_provider: null
```

Require `industry` and `product`. Require target market, customer, and roles when missing values would materially change topic quality; otherwise infer conservatively and record each inference in `run.assumptions`. Limit each topic to one primary and at most one secondary role.

Apply the business objective priority in this exact order:

1. Potential-customer interest
2. Commercial conversion relevance
3. Expertise / EEAT value
4. SEO opportunity
5. Trend speed
6. Social shareability

Do not let traffic or virality override buyer and commercial relevance.

## Run modes

### Daily

Scan for `BREAKING`, `TRENDING`, major company moves, policy or regulation changes, launches, safety issues, and suddenly repeated buyer questions.

- Primary lookback: last 72 hours
- Compare with prior equivalent windows for velocity
- Focused ceiling: about 200-350 raw signals, not a quota
- Return: Trending Top 5, Commercial Top 5, Evergreen Top 5, Overall Top 10

### Weekly

Combine the last seven days of trend evidence with emerging trends, Evergreen scanning, knowledge gaps, competitor gaps, search opportunities, and cannibalization cleanup.

- Consider emerging patterns from the last 14-90 days
- Focused ceiling: about 500-1,000 raw signals, not a quota
- Do not merely rerun the Daily search over seven days
- Return the same four ranked lists with weekly reasoning

### Monthly

Run a light `Knowledge Audit`; do not perform another large news crawl.

- expand and review the Industry Knowledge Map;
- clean the Topic Intelligence Graph;
- rescore old topics when evidence changed;
- archive declining or expired topics;
- inspect published-content, competitor-cluster, and pillar/supporting gaps.

When `scan_depth: deep`, widen queries and sources, but preserve all evidence, deduplication, and quality gates. Never pad a result to meet a volume target.

## Source framework

Classify every source by intelligence function:

| Source type | Examples | Primary use |
|---|---|---|
| `OFFICIAL_PRIMARY` | government, regulators, standards bodies, associations, company announcements, statistics, patents | verify what happened |
| `INDUSTRY_MEDIA` | trade media, specialist publications, research institutions | trends and context |
| `SEARCH_DEMAND` | Search, Trends, PAA, autocomplete, related searches, SERP | demand and question discovery |
| `COMMUNITY_VOICE` | Reddit, Quora, forums, LinkedIn discussions, specialist groups | pain points and buyer language |
| `VIDEO_CREATOR` | YouTube, podcasts, webinars, industry creators | propagated topics and technical questions |
| `COMPETITOR_INTELLIGENCE` | competitor blogs, news, resources, FAQ, case studies, video, social | coverage and content gaps |
| `EVERGREEN_KNOWLEDGE` | glossaries, standards indexes, manuals, training, buying guides, product taxonomies | expected industry knowledge |

Assign trust tier independently from topic value:

- `A`: official or primary source
- `B`: authoritative media or research source
- `C`: specialist, industry, competitor, or expert source
- `D`: community, comment, forum, or social source

Use Tier A to establish facts and Tier D to discover concerns. A low-trust source may contain a valuable buyer signal, but it cannot verify a regulatory, technical, statistical, or company claim.

## Evidence rules

- Use live search for current events and current SERP or competitor observations.
- Preserve the original URL, publisher, publication date, event date, first-seen time, language, and market.
- Separate `FACT`, `SIGNAL`, `INFERENCE`, and `HYPOTHESIS`.
- Prefer a primary source as `primary_source`; retain independent reports as evidence.
- Treat articles as evidence. Feed the clustered event, not each article, to Topic Generator.
- If exact SEO metrics are unavailable from the configured provider, set them to `null`; use an explicitly labeled proxy score only.
- Do not convert missing evidence into confident prose or numeric values.

## Core workflow

Execute in this order:

1. Normalize configuration and report assumptions.
2. Load existing Signals, Events, Topics, Knowledge Map, published content, approved topics, research queue, and rejected/archive memory when available.
3. Run Trend Engine and Evergreen Engine independently.
4. Normalize and clean signals; remove spam, irrelevant items, and exact URL duplicates.
5. Cluster trend signals into events and calculate Trend Score.
6. Identify Evergreen knowledge gaps.
7. Generate Topic Concepts before titles.
8. Create a Topic Fingerprint and compare it with topic memory.
9. Assign duplicate/cannibalization status before final ranking.
10. Calculate Blog Value, base Priority, boosts, penalties, and Final Priority.
11. Generate a restrained suggested title only after the concept survives governance.
12. Build rankings, upsert Feishu when authorized, and return the output contract.

## Trend Engine

### Hot-signal test

Treat a signal or event as potentially hot when at least one is true:

- mention velocity rises materially;
- an authoritative source publishes a material change;
- search demand grows;
- independent source categories converge;
- the issue has unusually high target-buyer relevance.

Do not equate presence in news with a trend.

### Event classification

Use one primary event type:

`REGULATION_POLICY`, `STANDARD`, `MARKET_SALES`, `PRICE_COST`, `PRODUCT_LAUNCH`, `TECHNOLOGY`, `COMPANY_MA`, `FACTORY_INVESTMENT`, `SUPPLY_CHAIN`, `CUSTOMER_BEHAVIOR`, `SAFETY_RECALL`, `COMPETITION`, `TRADE_TARIFF`, `ENVIRONMENT`, `OTHER`.

Use event status:

- `BREAKING`: normally 0-72 hours
- `TRENDING`: normally 3-14 days
- `EMERGING`: normally 14-90 days or an older issue with fresh acceleration
- `STABLE`: sustained without meaningful growth
- `DECLINING`: momentum or relevance is falling
- `ARCHIVED`: no longer actionable

Classify by evidence, not age alone.

### Event clustering

Cluster with all of: semantic similarity, named entities, event type, time window, and keywords. Store `cluster_confidence` from 0 to 1. When evidence is ambiguous, keep signals separate and mark them for review rather than over-merging.

An event retains:

- one canonical name and concise summary;
- first seen, latest meaningful update, and last seen;
- signal, independent-domain, and source-type counts;
- entities, countries, primary source, and evidence sources;
- prior-window and current-window mention counts.

## Evergreen Engine

Create the initial Industry Knowledge Map with AI, mark it `PROPOSED`, obtain human confirmation, then reuse and extend it during Monthly audits. Organize the map around the industry's own structure, normally including product, technology, components, applications, standards, buying, problems, and comparisons.

Find Evergreen Opportunities through all six routes:

1. Industry Knowledge Map gap
2. PAA, autocomplete, related-search, or durable search question
3. competitor coverage gap
4. repeated customer pain point
5. B2B buyer-journey gap
6. existing-content update opportunity

For Evergreen topics use `why_write`; use `why_now` only when a current change truly creates urgency. Do not force a Trend Score above the evidence.

## Topic Generator

Generate in this order:

`Event / Knowledge Gap -> Audience -> Buyer Stage -> Search Intent -> Angle -> Topic Concept -> Governance -> Score -> Suggested Title`

### Controlled vocabularies

Topic type:

`NEWS`, `NEWS_ANALYSIS`, `EVERGREEN_OPPORTUNITY`, `BUYER_QUESTION`, `COMMERCIAL_OPPORTUNITY`.

Content role:

`PILLAR`, `SUPPORTING`, `TREND`, `COMMERCIAL`, `TECHNICAL`, `COMPLIANCE`, `FAQ`.

Angle:

`EXPLAIN`, `IMPACT`, `ACTION`, `BUYING`, `COMPARISON`, `COST`, `RISK`, `COMPLIANCE`, `TECHNICAL`, `QUALITY`, `APPLICATION`, `TROUBLESHOOTING`, `TREND`, `CHECKLIST`, `FAQ`.

B2B buyer stage:

`LEARN`, `UNDERSTAND`, `EVALUATE`, `SELECT`, `SPECIFY`, `RFQ`, `ORDER`, `PRODUCTION`, `AFTERSALES`.

B2B search intent:

`LEARN`, `COMPARE`, `SOLVE`, `VERIFY`, `PLAN`, `SELECT_SUPPLIER`, `SPECIFY`, `PRICE`, `COMPLIANCE`, `RFQ`.

### Generation limits

- Normal signal or gap: 1-2 concepts
- Important event: 3-5 concepts
- Major regulation or industry change: 5-8 concepts
- Absolute event maximum: 10 concepts
- Important Evergreen cluster: 2-4 concepts
- Core pillar cluster maximum: 5 concepts

These are ceilings, never quotas. Select only applicable angles. Except for a truly major event, convert news into interpretation, buyer impact, and action instead of rewriting the announcement.

### Title rule

Generate the title last. Prefer `Problem + Audience`, `Question + Decision`, `Topic + Business Impact`, `Topic + Practical Action`, or `Comparison + Decision Context`.

Do not default to `Ultimate Guide`, `Everything You Need to Know`, `Top 10`, `Secret`, `Game-Changing`, `Revolutionary`, `Must-Know`, or `Best`. Use such wording only when the concept and evidence literally justify it.

## Topic governance

Compare every new concept with:

1. published content;
2. approved topics;
3. research queue;
4. rejected and archived topic memory.

Reject does not mean delete. Retain the decision and reason so the system does not repeatedly propose the same weak topic.

### Topic Fingerprint

Create a fingerprint from:

```json
{
  "core_entity": "...",
  "primary_problem": "...",
  "audience": "...",
  "buyer_stage": "...",
  "intent": "...",
  "angle": "...",
  "knowledge_node": "...",
  "keyword_cluster": ["..."]
}
```

### Overlap Score

Calculate 0-100:

| Component | Points |
|---|---:|
| Semantic similarity | 30 |
| Search-intent overlap | 25 |
| Keyword-cluster overlap | 20 |
| Knowledge-node overlap | 10 |
| Audience overlap | 5 |
| Buyer-stage overlap | 5 |
| Angle overlap | 5 |

Map the result:

- 90-100: `REJECT_DUPLICATE`
- 80-89: `MERGE` or `UPDATE_EXISTING`
- 65-79: `CANNIBALIZATION_RISK`
- 40-64: `RELATED`
- below 40: `NEW`

Do not auto-reject solely on numeric similarity when audience, intent, or angle creates a genuinely distinct job to be done. Explain that exception and send it to review.

Maintain graph relations: `related_to`, `supports`, `updates`, `competes_with`, `derived_from`, and `belongs_to`. Preserve full lineage:

`Source -> Signal -> Event / Knowledge Gap -> Angle -> Audience -> Intent -> Topic Concept -> Score -> Suggested Title`

## Scoring

Keep factual confidence separate from topic value.

### Trend Score — 100

| Component | Max | V1 rubric |
|---|---:|---|
| Recency | 15 | `<24h=15`, `1-3d=12`, `4-7d=9`, `8-14d=6`, `15-30d=3`, `>30d=0-2`; use latest meaningful update |
| Velocity | 20 | `>5x=20`, `3-5x=17`, `2-3x=14`, `1.5-2x=10`, `1-1.5x=5`, declining `=0`; mark zero-baseline acceleration `NEW_SPIKE` and justify manually |
| Independent source count | 10 | `1=2`, `2-3=4`, `4-6=6`, `7-15=8`, `15+=10`; deduplicate domains |
| Source authority | 15 | Tier A present `=15`; multiple Tier B `=12`; Tier C only `=7`; Tier D only `=3`; no usable evidence `=0` |
| Cross-platform signal | 15 | `1 type=2`, `2=5`, `3=8`, `4=11`, `5+=15` |
| Search growth | 15 | `>300%=15`, `150-300%=12`, `50-150%=9`, `10-50%=5`, stable `=2`, declining `=0`; unavailable `=null` and use zero in arithmetic |
| Market relevance | 10 | score target-market impact, not raw country count: none `=0`, outside target only `=2`, secondary market `=4`, one primary market `=6`, several targets `=8`, broad/direct target impact `=10` |

### Blog Value Score — 100

| Component | Max | Evaluate |
|---|---:|---|
| Buyer relevance | 25 | direct effect on target buyer's cost, compliance, supplier, lead time, risk, performance, or sales |
| Commercial relevance | 20 | proximity to RFQ, supplier, comparison, compliance, cost, specification, or purchase decisions |
| Expertise / EEAT value | 15 | ability to demonstrate credible technical, manufacturing, quality, regulatory, or operational expertise |
| Search opportunity | 15 | demand, growth, long-tail depth, PAA, intent clarity, and SERP weakness; do not invent SEO metrics |
| Product relevance | 10 | closeness to the configured product or service |
| Content gap | 10 | own-site, competitor, and SERP gap |
| Evergreen potential | 5 | durable value independent of the current event |

For each component, provide `score`, `max`, `evidence`, and a one-sentence rationale. Use the full range; do not cluster every topic near the middle.

### Priority Score

```text
base_priority = blog_value_score * 0.70 + trend_score * 0.30
final_priority = clamp(round(base_priority + total_boosts - total_penalties), 0, 100)
```

Allowed evidence-backed boosts:

- major regulation affecting target buyers: `+10`
- repeated buyer pain across channels: `+8`
- major competitor coverage with a clear own-site gap: `+5`
- new product or technology directly affecting the product roadmap: `+5`

Allowed penalties:

- duplicate topic: `-100`
- strong cannibalization: `-30`
- already published recently: `-40`
- weak source support: `-10`
- clickbait-only angle: `-15`
- low target-market relevance: `-20`
- outdated: `-20`
- no buyer relevance: `-30`

Record every applied rule. Do not add a boost or penalty merely to force a preferred rank.

Map final score:

- 90-100: `P0_IMMEDIATE`
- 80-89: `P1_HIGH_PRIORITY`
- 70-79: `P2_RECOMMENDED`
- 60-69: `P3_BACKLOG`
- below 60: `REJECT_ARCHIVE`

Special queues:

- `URGENT_REVIEW` when a news topic has Trend Score at least 85 and Blog Value at least 65, even if Final Priority is below 80.
- `EVERGREEN_PRIORITY` when Blog Value is at least 85 and Trend Score is below 30.

Never discard the underlying score band when adding a special queue.

## Ranking and lifecycle

Keep three independent rankings so one content class cannot crowd out the others:

- Breaking / Trending Top 5
- Buyer / Commercial Top 5
- Evergreen Top 5

Then calculate Overall Top 10 from eligible topics. Break ties in this order: higher Blog Value, higher Buyer Relevance, higher Commercial Relevance, stronger source support, then higher Trend Score.

Use topic lifecycle:

`DISCOVERED -> SCORED -> REVIEW -> APPROVED -> HANDED_TO_RESEARCHER`

Alternative terminal or side states: `MERGED`, `REJECTED`, `EXPIRED`. When a time-sensitive topic expires, assess whether it can be converted into a new Evergreen concept; do not silently change its lineage.

## Output contract

Return valid JSON plus a concise human-readable summary. Use `null`, not invented values.

```json
{
  "run": {"run_id": "...", "run_mode": "daily", "started_at": "...", "completed_at": "...", "configuration": {}, "assumptions": [], "coverage_gaps": [], "partial": false},
  "summary": {"raw_signals": 0, "valid_signals": 0, "events": 0, "generated_topics": 0, "qualified_topics": 0, "priority_topics": 0},
  "signals": [], "events": [], "knowledge_map": [], "topics": [],
  "rankings": {"trending_top_5": [], "commercial_top_5": [], "evergreen_top_5": [], "overall_top_10": []},
  "errors": []
}
```

Each Topic object must include:

```json
{
  "topic_id": "...",
  "topic_concept": "...", "suggested_title": "...",
  "topic_type": "EVERGREEN_OPPORTUNITY", "content_role": "COMMERCIAL", "angle": "BUYING",
  "industry_cluster": "...", "knowledge_node": "...",
  "target_customer": "...", "primary_role": "...", "secondary_role": null,
  "buyer_stage": "SELECT", "search_intent": "SELECT_SUPPLIER", "target_market": ["..."],
  "primary_keyword": "...", "secondary_keywords": [],
  "seo_metrics": {"search_volume": null, "keyword_difficulty": null, "cpc": null, "provider": null},
  "why_now": null, "why_write": "...",
  "event_id": null, "knowledge_gap_id": "...", "signal_ids": [],
  "fingerprint": {},
  "scores": {"trend": {"total": 0, "components": {}}, "blog_value": {"total": 0, "components": {}}, "base_priority": 0, "boosts": [], "penalties": [], "final_priority": 0, "band": "P3_BACKLOG", "special_queue": null},
  "duplicate_status": "NEW", "overlap_score": 0,
  "related_topic_ids": [], "pillar_topic_id": null,
  "lineage": {},
  "publish_window": null, "status": "SCORED"
}
```

## Feishu model

When a Feishu Bitable destination and access are available, inspect its schema before writing and use four tables only:

### `01 Signals`

`signal_id`, `title`, `summary`, `source_name`, `source_type`, `source_tier`, `source_url`, `published_at`, `event_date`, `first_seen_at`, `country`, `language`, `entities`, `keywords`, `authority_score`, `raw_relevance`, `event_id`, `status`.

Signal status: `NEW`, `VALID`, `DUPLICATE`, `NOISE`, `CLUSTERED`.

### `02 Events`

`event_id`, `event_name`, `event_summary`, `event_type`, `first_seen`, `latest_meaningful_update`, `last_seen`, `signal_count`, `source_count`, `source_type_count`, `countries`, `entities`, `primary_source`, `evidence_sources`, `event_status`, all Trend Score components, `trend_score`.

### `03 Topics`

Store the complete Topic object, including component scores, boosts, penalties, duplicate status, overlap score, relationships, queue, lifecycle status, and rejection reason.

### `04 Knowledge Map`

`knowledge_id`, `parent_id`, `level_1`, `level_2`, `level_3`, `knowledge_name`, `description`, `importance`, `buyer_relevance`, `target_roles`, `existing_content_count`, `approved_topic_count`, `competitor_coverage`, `search_demand`, `content_gap_score`, `last_scanned`, `status`.

Upsert with stable IDs. Create only new records, update changed machine-owned fields, and preserve human-owned fields such as owner, approval, editorial notes, and manual status. If Feishu is unavailable, return JSON and CSV-ready tables; do not claim they were written.

## Error handling

- Continue after one source fails; record source, error, impact, and retryability.
- Mark `run.partial: true` when a missing source category materially reduces coverage.
- If an authoritative claim has only weak evidence, keep it as an unverified signal and block confident scoring or title wording.
- If search-growth or SEO data is unavailable, use `null` and disclose the arithmetic treatment.
- Preserve original text and provide a labeled translation when sources use another language.
- Distinguish event date, data period, publication date, and discovery time.
- Do not bypass paywalls, access controls, robots restrictions, or unavailable APIs.
- If the topic database is unavailable, perform in-run comparison against supplied history and disclose the narrower deduplication scope.

## Quality gate

Before returning, verify:

- both Trend and Evergreen engines ran for Weekly; the requested engine ran for other modes;
- every topic has a buyer, role, stage, intent, angle, market, reason, and lineage;
- every factual event has a canonical source and usable evidence;
- signals are clustered before topic generation;
- Topic Concepts were generated before titles;
- every topic was compared with all available topic-memory stores;
- score components sum exactly to their totals and final arithmetic is reproducible;
- rankings follow eligibility rules and tie-break order;
- missing SEO metrics remain `null`;
- rejected and merged topics remain in memory with reasons;
- no Research Pack or downstream content was produced;
- Feishu writes, if any, were verified without overwriting human fields.

Use the user's language for the summary and preserve source-language terms where they improve search accuracy.
