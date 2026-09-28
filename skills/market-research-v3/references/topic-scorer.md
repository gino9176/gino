# Topic Scorer

## Objective

Score Topic Scout records consistently and decide which topics enter research.

## Procedure

1. Read a canonical topic record and all supporting evidence.
2. Confirm target customer, country, search intent, buyer stage, and product connection.
3. Load verified SEO metrics when a connected source exists.
4. Keep `search_volume`, `keyword_difficulty`, and `cpc` null when unavailable.
5. Score all six criteria using `scoring.md`.
6. Add the six subscores and assign the exact status band.
7. Write a one-sentence reason for every subscore.
8. Update the Topic Database without overwriting workflow ownership fields.

## SEO data boundary

AI judgment is not SEO measurement.

When Ahrefs, Semrush, DataForSEO, or another verified provider is connected, store:

- provider
- query date
- country and language database
- search volume
- Keyword Difficulty
- CPC and currency
- trend period when available

When no provider is connected:

- set numeric SEO fields to null
- set `search_demand_basis` to `proxy`
- explain the proxy signals
- never manufacture a plausible-looking number

## Queue rule

- Reject: retain for audit but do not research.
- Backlog: retain for future review.
- Research: send to the normal research queue.
- Priority Research: send to the top of the research queue.

A high-traffic educational topic can still rank poorly when buyer intent and commercial value are weak. A narrower supplier-evaluation topic can rank highly when it strongly matches the product and buyer stage.
