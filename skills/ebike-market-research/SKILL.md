---
name: ebike-market-research
description: >
  Research and monitor the electric bicycle industry. Collect current news,
  market data, regulations, company activity, product launches, technology,
  supply-chain developments, pricing, investment and customer signals, then
  convert them into prioritized business intelligence, opportunities, risks
  and concrete next actions.
---

# E-bike Market Research

## Purpose

Turn current e-bike industry information into actionable market intelligence.

Do not merely summarize news. For each meaningful development, answer:

1. What happened?
2. When did it happen?
3. Which market, company, product or regulation is affected?
4. Why does it matter?
5. Is it an Opportunity, Risk or Watch signal?
6. What evidence supports the conclusion?
7. What should the user do next?

## Inputs

At minimum, accept:
- industry, product or research topic

Optional:
- target countries or regions
- target customer types
- monitored brands or competitors
- monitored suppliers
- products or technologies
- sales channels
- date range
- company strategy or business objective
- desired output: daily brief, weekly report, deep dive or alert

If inputs are incomplete, make reasonable research defaults and state them briefly.

## Research Scope

Scan these categories:

1. Industry trends
2. Market demand and sales
3. Regulation, standards and trade policy
4. Competitors and brands
5. Customer and retailer signals
6. Product launches and specifications
7. Motor, battery, drivetrain and frame technology
8. Supply chain, production and sourcing
9. Pricing, inventory and discounting
10. Distribution, retail, leasing and e-commerce
11. Investment, M&A, bankruptcy and restructuring
12. Consumer behavior and product safety
13. Exhibitions and industry events

## Source Priority

Use the source list in `references/sources.md`.

Prefer sources in this order:

### Tier A — Primary / official
- EU and national government sources
- regulations and standards bodies
- official statistics
- company press releases and financial reports
- official industry associations
- official product-safety databases

### Tier B — Specialist industry media
- established bicycle and e-bike trade publications
- specialist market-data publications

### Tier C — Secondary signals
- mainstream business media
- retailer news
- LinkedIn/company posts
- forums and Reddit

Use Tier C mainly for signal discovery. Verify important claims with Tier A or Tier B whenever possible.

## Freshness Rules

- For daily monitoring, prioritize developments from the last 24-72 hours.
- For weekly reports, prioritize the last 7 days.
- Distinguish publication date from event date.
- Do not call an old event "new" merely because a recent article mentions it.
- If a story is an update to an earlier event, explain what is actually new.
- Avoid repeating previously reported items unless there is a material change.

## Research Workflow

### Step 1 — Discover

Search across:
- industry media
- associations
- regulators
- market data
- company newsrooms
- suppliers
- exhibitions

Use multiple query variants, including:
- e-bike / ebike / electric bicycle / pedelec
- country names
- company names
- regulation names
- product categories
- motor, battery, drivetrain and frame keywords

### Step 2 — Extract

For each item, capture:
- headline
- source
- source type
- URL
- publication date
- event date
- country/region
- companies
- products
- technologies
- regulation/standard
- key factual claims
- supporting evidence

### Step 3 — Deduplicate

Merge stories that describe the same underlying event.

Keep the strongest original/primary source and optionally one high-quality independent source.

### Step 4 — Classify

Assign one or more tags:

- Market
- Demand
- Regulation
- Trade
- Competitor
- Customer
- Product
- Technology
- Motor
- Battery
- Frame
- SupplyChain
- Pricing
- Inventory
- Retail
- Leasing
- Investment
- M&A
- Bankruptcy
- ProductSafety
- Event

### Step 5 — Determine Signal

Classify each important item as:

- Opportunity
- Risk
- Watch

Multiple labels are allowed when justified.

### Step 6 — Analyze Business Meaning

For every high-value item, explain:

- What happened
- Why it matters
- Market implication
- Customer implication
- Competitive implication
- Supply-chain implication
- Product implication
- Confidence level
- Recommended next action

Do not invent customer demand or causality. Separate observed facts from inference.

### Step 7 — Score

Use the scoring model in `references/scoring.md`.

Return a score from 0-100.

Priority bands:

- 80-100: Critical / must review
- 60-79: Important
- 40-59: Monitor
- 0-39: Background

### Step 8 — Detect Trends

Compare current findings with historical findings when available.

Look for:
- increasing topic frequency
- repeated company activity
- repeated product patterns
- price changes
- inventory normalization
- geographic shifts
- regulatory momentum
- recurring customer pain points
- new technologies
- supplier substitutions

Do not declare a trend from one article.

Create a Trend record when at least 3 reasonably independent signals point to the same development.

Trend record:
- trend name
- first seen
- latest evidence
- evidence count
- affected markets
- affected companies
- signal strength
- business implication
- next action

### Step 9 — Detect Weak Signals

Track:
- rapidly increasing keywords
- new product terms
- new suppliers
- suddenly active brands
- new country clusters
- repeated regulatory language
- repeated complaints or safety issues

Label them as Emerging Signal until evidence is strong enough to call a trend.

## Daily Output

Return no more than 10 high-value items by default.

Structure:

# E-bike Industry Intelligence — YYYY-MM-DD

## Top 3 Developments

For each:
- headline
- score
- signal: Opportunity / Risk / Watch
- what happened
- why it matters
- business implication
- next action
- sources

## Opportunity Radar

List concrete opportunities discovered today.

## Risk Radar

List concrete risks that may affect demand, compliance, pricing, production or customers.

## Customer & Competitor Signals

Highlight company-level buying, expansion, restructuring, product, hiring or sourcing signals.

## Regulation & Safety

Highlight regulatory, standards, trade, battery, product-safety and recall developments.

## Emerging Trends

Only include trends supported by multiple signals.

## Watchlist

Items worth monitoring but not yet actionable.

## Weekly Output

A weekly report should synthesize, not merely concatenate daily reports.

Include:
- 5 most important developments
- trend changes
- opportunity map
- risk map
- competitor activity
- customer signals
- regulation changes
- market data changes
- recommended actions for next week

## Action Conversion

When a signal may create a commercial opportunity, convert it into a possible action such as:

- add company to prospect list
- research purchasing/product/sourcing contacts
- monitor a product launch
- compare product specifications
- review frame or component compatibility
- prepare an outreach angle
- create market-specific content
- adjust pricing assumptions
- investigate supplier alternatives
- review compliance documents
- monitor a regulation
- schedule follow-up research

Do not automatically claim that a company is a qualified sales lead. Mark unverified leads as "Potential Lead" until evidence of fit exists.

## Evidence Standard

- Cite sources for factual claims.
- Prefer primary sources for regulations, statistics and company announcements.
- Cross-check major market claims.
- Note paywalls or incomplete data.
- State uncertainty explicitly.
- Never fabricate market size, sales volume, company revenue or regulations.

## Output Language

Use the user's language unless requested otherwise.

Keep company names, regulation names and technical terms in their official language where helpful.
