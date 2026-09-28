# Fixed Topic Scoring Model

Total: 100 points.

## Search Demand — 0-20

Use verified SEO data when available. Otherwise use clearly labeled proxy evidence such as repeated queries across source families, Trends direction, PAA presence, recurring customer questions, and repeated community discussion.

Do not invent search volume. In proxy mode, explain uncertainty and normally avoid scores above 15 without strong multi-source evidence.

## Buyer Intent — 0-25

- 0-5: curiosity or general history
- 6-12: awareness and education
- 13-18: problem solving or category comparison
- 19-22: product, supplier, price, or compliance evaluation
- 23-25: strong sourcing, quotation, purchase, or vendor-selection intent

## Product Relevance — 0-20

Measure how directly the topic connects to the offered product, specifications, use cases, differentiation, and target customer.

## Commercial Value — 0-20

Measure whether the topic can support qualification, product-page connection, inquiry generation, sales enablement, risk reduction, or purchase progress.

## Content Opportunity — 0-10

Consider evidence availability, competitor content gaps, unique expertise, ability to add original proof, and difficulty. Use verified Keyword Difficulty only when a real provider supplies it.

## Freshness — 0-5

Score timing from current regulation, launches, seasonality, news, rising discussion, or a recent change. Evergreen topics can still score, but should not receive artificial freshness points.

## Status bands

- 0-59: Reject
- 60-74: Backlog
- 75-84: Research
- 85-100: Priority Research

## Required score output

Return:

- six subscores
- six short reasons
- total
- exact status
- confidence
- `search_demand_basis`: verified or proxy
- SEO provider and query date, or null
- search volume, Keyword Difficulty, CPC, and currency, or null

Validate arithmetic before saving.
