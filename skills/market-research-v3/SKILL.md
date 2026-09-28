---
name: market-research-v3
description: >
  Run an evidence-first product market research pipeline with Topic Scout, Topic Scorer, and Researcher stages. Use when the user wants daily or weekly topic discovery, trend scanning, SEO/content opportunity scoring, a Feishu Topic Database, market or competitor research, a cited Research Pack, or research before producing B2B/B2C content. Accept any product, market, customer, competitor, image, specification, or URL. Enforce source-backed numbers and never invent search volume, keyword difficulty, CPC, market size, prices, growth rates, regulations, tariffs, certification requirements, sales, or company data.
---

# Market Research V3

Run this pipeline:

`Topic Scout -> Deduplicate -> Feishu Topic Database -> Topic Scorer -> Research Queue -> Researcher -> Research Pack`

Do not write an article during this skill unless the user explicitly asks. Produce research inputs that a separate writing workflow can trust.

## Load the right resources

- Read `references/topic-scout.md` before discovering topics.
- Read `references/topic-scorer.md` and `references/scoring.md` before scoring.
- Read `references/researcher.md` before preparing a Research Pack.
- Read `references/source-strategy.md` before building queries or judging sources.
- Read `references/feishu-topics.md` before creating or updating the Topic Database.
- Use `templates/topic-record.schema.json` for structured Scout output.
- Use `templates/research-pack.md` for topic research.
- Use `templates/topic-backlog.md` for a human-readable queue.
- Use `templates/market-research-report.md` only for a broader market study.
- Use `templates/daily-report.md` for recurring monitoring briefs.

## Required input

Require only a product identifier: product name, description, image, video, specification, category, or URL.

Accept optional:

- target country, city, and language
- target customer, buyer, user, and decision maker
- B2B/B2C model, offer, product pages, positioning, and business objective
- competitors, substitutes, channels, and known sources
- daily, weekly, one-time, or custom research window
- desired topic count from 20 to 50
- Feishu Bitable destination
- connected SEO provider: Ahrefs, Semrush, DataForSEO, or another verified source

Infer missing context only when it does not materially change the result. Mark every inference as `Assumption`.

## Stage 0 — Product and research brief

Define:

- product, category, synonyms, technical terms, and substitutes
- use cases and customer problems
- user, buyer, decision maker, payer, and buyer stage
- target markets and local-language vocabulary
- business objective and conversion path
- claims requiring authoritative evidence

If the product input is visual, separate visible facts from inferred specifications.

## Stage 1 — Topic Scout

Run daily or weekly discovery across:

1. Google Search or another capable web search engine
2. Google Trends or an equivalent trend source
3. industry media
4. competitor blogs, newsrooms, product pages, catalogs, and filings
5. Reddit and specialist forums
6. YouTube videos, channels, reviews, and comments
7. industry associations and standards bodies
8. regulation and policy websites
9. customer questions, reviews, support pages, and sales FAQs
10. SERP People Also Ask, related searches, and autocomplete

Collect broadly, normalize terminology, and deduplicate by canonical URL, underlying event, and search intent. Keep corroborating sources inside one topic record.

Return 20-50 distinct topics; default to 30. Output valid JSON matching `templates/topic-record.schema.json` and prepare the same records for Feishu.

Each topic must include at least:

- topic
- keyword
- source_type
- source_url
- reason
- target_customer
- country
- search_intent
- buyer_stage
- evidence summary

Do not confuse social attention, Trends indices, views, or PAA visibility with sales or exact search volume.

## Stage 2 — Feishu Topic Database

Use Feishu Bitable as the canonical topic queue when access is available.

Before writing:

1. inspect the table schema
2. map fields using `references/feishu-topics.md`
3. search by `Topic ID`
4. update changed records and create only new records
5. preserve owner, editorial notes, and workflow status

If Feishu is unavailable or no destination is supplied, return JSON plus a CSV-ready table. Do not claim that records were written.

## Stage 3 — Topic Scorer

Read candidates from the Topic Database or Scout JSON. Apply the fixed 100-point model in `references/scoring.md`:

- Search Demand: 20
- Buyer Intent: 25
- Product Relevance: 20
- Commercial Value: 20
- Content Opportunity: 10
- Freshness: 5

Map totals to exactly one status:

- below 60: Reject
- 60-74: Backlog
- 75-84: Research
- 85-100: Priority Research

AI score is not SEO search volume. If verified search volume, Keyword Difficulty, or CPC is unavailable, leave those fields null and label Search Demand as `proxy`. Never guess SEO metrics.

Explain every subscore in one concise sentence. Send only `Research` and `Priority Research` topics to the research queue unless the user overrides the rule.

## Stage 4 — Researcher

Use live web research and search tools. Do not answer from model memory when current evidence is required.

Research across:

- government and regulators
- EU or relevant supranational bodies
- industry associations and standards bodies
- research institutions and original datasets
- company websites, filings, manuals, and product documentation
- specialist industry media
- competitors
- Reddit, forums, reviews, and customer questions
- official statistics and customs data

Return a Research Pack, not a generic summary. Follow `templates/research-pack.md`.

Required sections:

- Key Findings
- Market Data
- Regulations and Standards
- Customer Problems and Questions
- Competitor Claims and Viewpoints
- Statistics
- Contradictory Evidence
- Short Quotes when useful
- Sources with URL, date, publisher, and confidence

## Non-negotiable numeric evidence gate

Do not admit a number into Key Findings, conclusions, or downstream writing unless the record includes:

- the exact number and unit
- geography and scope
- data year or measurement period
- publisher
- source URL
- publication date when available
- methodology or dataset note when material

Apply this gate especially to market size, price, growth, regulation, tariff, certification, sales, import/export, search volume, CPC, Keyword Difficulty, and company data.

If the source cannot be verified, set the field to null or place the claim in `Unverified / Excluded`. Do not silently convert it into prose.

## Evidence and contradiction rules

- Prefer primary sources for law, statistics, standards, specifications, recalls, and company claims.
- Use industry media for discovery and context.
- Use Reddit, forums, comments, reviews, PAA, and autocomplete for customer language and weak signals.
- Separate Fact, Signal, Inference, and Hypothesis.
- Distinguish event date, data year, and publication date.
- Preserve conflicting evidence and explain likely causes such as geography, definitions, sample, or period.
- Assign confidence independently from topic score.
- Cite factual claims near the relevant text.
- Quote briefly and prefer paraphrase.

## Quality gate

Before finalizing, verify:

- 20-50 topics are distinct after deduplication
- each topic has evidence and a canonical source URL
- each score adds to the recorded total
- status matches the exact score band
- SEO metrics are verified or null
- research topics match target customer, country, intent, and buyer stage
- every included number passes the numeric evidence gate
- regulations and standards come from authoritative sources
- contradictory evidence is visible
- Feishu upsert does not duplicate topics or overwrite workflow fields

Use the user's language unless requested otherwise.
