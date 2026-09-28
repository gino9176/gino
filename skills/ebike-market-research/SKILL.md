---
name: ebike-market-research
description: >
  Research any physical or digital product and turn current multi-source evidence into a structured market study, trend signals, and 20-50 prioritized topics. Use when the user provides a product name, description, image, video, specification, category, or URL and asks for market research, product opportunity analysis, country or city selection, audience and channel research, industry news monitoring, competitor research, customer questions, SEO/content topics, trend discovery, or export to Feishu Topics. Despite the legacy name, this skill supports products beyond e-bikes.
---

# Product Market Research V2

Turn a product input into evidence-backed market intelligence and a prioritized topic backlog. Do not merely summarize search results.

## Load supporting files

- Read `references/source-strategy.md` before building queries or selecting sources.
- Read `references/sources.md` only when the product is an e-bike, bicycle, frame, or related component; treat it as an industry seed list rather than a closed source universe.
- Read `references/scoring.md` before ranking markets, signals, or topics.
- Read `references/feishu-topics.md` when the user wants Feishu output or a reusable Topics database.
- Use `templates/market-research-report.md` for a full market study.
- Use `templates/topic-backlog.md` for the 20-50 topic output.
- Use `templates/daily-report.md` for daily or weekly monitoring.
- Use `config.example.yaml` when the user wants a reusable configuration.

## Operating modes

Choose the smallest mode that satisfies the request:

1. `full-research`: product understanding, market attractiveness, people-product-place analysis, competitors, channels, regulations, opportunities, risks, and topics.
2. `topic-scout`: discover, deduplicate, cluster, score, and return 20-50 topics.
3. `trend-monitor`: scan recent news and weak signals, then produce an intelligence brief.
4. `market-deep-dive`: analyze one country, city, customer segment, channel, or competitor set.
5. `validation-plan`: convert uncertain conclusions into buyer interviews, landing pages, RFQs, ads, preorders, or other demand tests.

If the user does not specify a mode, use `full-research` and include a topic backlog.

## Input contract

Require only one product identifier:

- product name, description, image, video, specification, category, or product URL

Accept these optional inputs:

- target countries, regions, or cities
- B2B, B2C, or both
- target users, buyers, or customer types
- company offer, capabilities, price position, MOQ, lead time, and certifications
- sales channels
- known competitors or substitutes
- business objective
- date range and reporting cadence
- output language
- desired number of topics from 20 to 50
- Feishu destination or requested export format

Do not block when optional fields are missing. Infer provisional defaults, label each one `Assumption`, and identify which assumptions materially affect the conclusion.

## Workflow

### 1. Build the product brief

Determine:

- what the product is and is not
- category, components, materials, and substitutes
- primary and secondary use scenarios
- user, buyer, decision maker, influencer, and payer
- B2B/B2C business model and likely buying unit
- functional, emotional, financial, and compliance jobs
- likely price band and positioning
- constraints that change market fit

If an image or video is provided, distinguish visible facts from inference. Do not invent hidden specifications.

### 2. Apply People-Product-Place analysis

Analyze:

- `People`: users, buyers, decision makers, pain points, objections, purchase triggers, and unmet needs.
- `Product`: core value, alternatives, price band, differentiation, compatibility, lifecycle, and compliance.
- `Place`: countries, cities, climates, use settings, channels, platforms, distributors, and sales moments.

Return up to 10 evidence-backed results per requested dimension when enough evidence exists. Return fewer instead of padding weak results.

### 3. Generate a dynamic source map

Start with these source families, then discover product-specific and country-specific sources:

1. Google Search or another capable web search engine
2. Google Trends or an equivalent trend-data source
3. specialist industry media
4. competitor blogs, newsrooms, catalogs, filings, and product pages
5. Reddit and relevant forums
6. YouTube videos, channels, comments, and reviews
7. industry associations and standards bodies
8. regulation, policy, customs, statistics, and product-safety websites
9. customer questions in reviews, support pages, communities, and sales conversations
10. SERP People Also Ask, related searches, and autocomplete suggestions

Treat discovery platforms as signal sources, not automatically as proof. Prefer primary sources for regulations, statistics, specifications, and company claims.

### 4. Build the query matrix

Combine the normalized product vocabulary with:

- use case and problem
- buyer or user type
- country, city, and local-language synonym
- price, cost, review, comparison, alternative, and supplier intent
- regulation, standard, certification, tariff, recall, and safety intent
- trend, news, launch, growth, decline, shortage, inventory, and investment intent
- forum, Reddit, YouTube, FAQ, PAA, and complaint intent

Use local-language queries for priority markets. Record the exact queries that produced high-value evidence.

### 5. Run Trend Scout

Collect a broad candidate set before ranking:

- current news and policy changes
- repeated questions and complaints
- rising product terms and use cases
- competitor launches, pricing, partnerships, hiring, expansion, contraction, and sourcing signals
- channel changes and retailer activity
- new regulations, recalls, standards, and compliance deadlines
- product-review language and recurring objections
- geographic clusters and seasonal patterns

Capture for every item: title, source, URL, source type, publication date, event date, geography, entity, observed fact, inference, and query.

### 6. Normalize and deduplicate

Normalize casing, punctuation, dates, company aliases, product synonyms, tracking parameters, and syndicated headlines.

Deduplicate at three levels:

1. exact URL or canonical URL
2. same event reported by multiple sources
3. different wording with the same search intent or customer question

Create one canonical cluster. Retain the strongest primary source, one useful independent source, source count, and distinct evidence. Do not discard corroboration.

### 7. Separate facts, signals, and hypotheses

Label statements:

- `Fact`: directly supported by a cited source.
- `Signal`: a pattern or indicator supported by one or more observations.
- `Inference`: a reasoned interpretation.
- `Hypothesis`: an unverified proposition that requires testing.

Never convert search popularity, social discussion, or views directly into sales volume.

### 8. Score and rank

Apply the correct model in `references/scoring.md`:

- market attractiveness score
- intelligence signal score
- topic opportunity score

Keep confidence separate from importance. A commercially important but weakly evidenced item must show low confidence.

### 9. Select 20-50 topics

Return 30 topics by default. Balance the final set across:

- market education and category understanding
- pain points and jobs-to-be-done
- comparisons and alternatives
- purchase, supplier, and commercial intent
- regulations and risk
- trend and news response
- product use, installation, maintenance, and troubleshooting
- case studies, applications, and proof

Do not return 30 paraphrases of the same keyword. Group topics into clusters, identify one pillar topic, and map supporting topics to it.

For each topic include:

- canonical topic
- cluster and angle
- target person and market
- search or business intent
- funnel stage
- evidence and source URLs
- why now
- suggested format and channel
- topic score and confidence
- recommended next action

### 10. Produce the market study

Synthesize evidence into:

- product and use-case definition
- People-Product-Place map
- demand signals and market stage
- top countries and cities
- customer and buyer segments
- price bands and buying criteria
- online and offline channels
- competitors and substitutes
- regulatory and compliance constraints
- supply-chain considerations
- customer questions and pain points
- trends and weak signals
- opportunities, risks, and evidence gaps
- 30/60/90-day actions and validation experiments

Use ranges and explain methodology when reliable market-size data is unavailable. Never fabricate market size, sales, search volume, growth, regulation, or company facts.

### 11. Export to Feishu Topics

If Feishu access is available, inspect the destination schema before writing. Upsert by `Topic ID` or canonical topic key; do not create duplicates. Ask for the destination only when a write is requested and none is known.

If Feishu access is unavailable, return a Markdown table or CSV-ready structure using `references/feishu-topics.md`. Do not claim that data was written.

## Evidence rules

- Browse for all current market, trend, news, price, regulation, company, and recommendation claims.
- Use more than one source family for major conclusions.
- Distinguish event date from publication date.
- State the research window and cutoff date.
- Cite claims near the relevant text.
- Mark paywalls, unavailable metrics, and evidence gaps.
- Use Reddit, forums, comments, PAA, autocomplete, and YouTube as demand-language evidence unless corroborated.
- Prefer official sources for regulations, statistics, recalls, specifications, and corporate announcements.
- Preserve disagreement between sources instead of forcing false certainty.

## Quality gate

Before finalizing, verify:

- the product definition matches the input
- assumptions are visible
- each major claim has evidence
- dates are current and unambiguous
- duplicates and syndicated stories are merged
- facts and inference are separated
- topic clusters are genuinely distinct
- the 20-50 topics cover multiple intents and funnel stages
- recommendations connect to the user's objective
- missing data becomes a validation task, not an invented fact

## Output behavior

Use the user's language unless asked otherwise. Lead with the most decision-relevant conclusions. Keep raw source lists after the synthesis, not before it.
