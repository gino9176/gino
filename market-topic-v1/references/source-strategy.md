# Source Strategy

## Seven source functions

| Type | Typical sources | Use |
|---|---|---|
| `OFFICIAL_PRIMARY` | government, regulators, standards bodies, associations, company announcements, official statistics, patents | verify material facts |
| `INDUSTRY_MEDIA` | trade media, specialist publications, research institutions | discover and contextualize trends |
| `SEARCH_DEMAND` | web search, Trends, PAA, autocomplete, related searches, SERP | discover demand and questions |
| `COMMUNITY_VOICE` | Reddit, Quora, forums, LinkedIn discussions, specialist groups | find pain, objections, and buyer language |
| `VIDEO_CREATOR` | YouTube, podcasts, webinars, industry creators | find propagated topics and demonstrations |
| `COMPETITOR_INTELLIGENCE` | competitor blogs, news, resources, FAQ, case studies, video, social | detect coverage, positioning, and gaps |
| `EVERGREEN_KNOWLEDGE` | glossaries, standards indexes, manuals, training, buying guides, product taxonomies | map expected industry knowledge |

## Trust tiers

- `A`: official or primary source.
- `B`: authoritative media or research source.
- `C`: specialist, industry, competitor, or identifiable expert source.
- `D`: community, comment, forum, or social source.

Trust and topic value are independent. Tier A can prove what happened. Tier D can reveal what buyers fear or ask. Tier D cannot establish regulations, technical limits, market size, company claims, or safety facts.

## Query planning

Build query groups from:

- product, category, technical name, synonym, and substitute;
- target country, city, region, and local-language vocabulary;
- target customer and buyer role;
- buying stages `LEARN` through `AFTERSALES`;
- event types and regulation/standard names;
- problem, failure, comparison, cost, supplier, specification, and RFQ modifiers;
- own website and named competitors.

Run source-specific queries. Do not use one generic query for every source.

## Signal record

Capture:

- title and concise summary;
- source name, type, tier, and canonical URL;
- publication date, event date, and first-seen time;
- country, language, entities, and keywords;
- evidence class: `FACT`, `SIGNAL`, `INFERENCE`, or `HYPOTHESIS`;
- raw relevance and authority assessment;
- extraction or access limitation.

## Cleaning

- Canonicalize URLs and remove tracking parameters where safe.
- Deduplicate exact URLs and syndicated copies.
- Count independent domains, not article count.
- Preserve several sources when they independently corroborate one event.
- Prefer the original company, regulator, association, dataset, or standard source.
- Mark a source unavailable instead of inventing its content.

## Hot-signal test

Treat an item as potentially hot when at least one is supported:

- meaningful velocity increase;
- material authoritative announcement;
- search-demand growth;
- convergence across source categories;
- unusually high target-buyer relevance.

News presence alone is not a trend.

## Event clustering

Combine semantic similarity, named entities, event type, time window, and keywords. Store `cluster_confidence` from 0 to 1. If ambiguous, keep records separate and request review.

Use one primary event type:

`REGULATION_POLICY`, `STANDARD`, `MARKET_SALES`, `PRICE_COST`, `PRODUCT_LAUNCH`, `TECHNOLOGY`, `COMPANY_MA`, `FACTORY_INVESTMENT`, `SUPPLY_CHAIN`, `CUSTOMER_BEHAVIOR`, `SAFETY_RECALL`, `COMPETITION`, `TRADE_TARIFF`, `ENVIRONMENT`, `OTHER`.

An event must retain one canonical name, summary, first seen, latest meaningful update, last seen, counts, entities, countries, primary source, evidence sources, and prior/current-window mention counts.

## SEO evidence

When an authenticated Ahrefs, Semrush, DataForSEO, or equivalent result exists, store its exact values, provider, market, language, and date.

Otherwise:

- set search volume, keyword difficulty, and CPC to `null`;
- label qualitative demand assessment as `proxy`;
- never convert Trends index, PAA presence, autocomplete, or result count into exact volume.
