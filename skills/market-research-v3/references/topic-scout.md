# Topic Scout

## Objective

Discover 20-50 distinct, evidence-backed topic opportunities for one product and market. Run once, daily, or weekly.

## Discovery sequence

1. Normalize the product vocabulary, synonyms, technical terms, substitutes, and local-language variants.
2. Build queries across category, problem, application, buyer, comparison, sourcing, price, regulation, risk, maintenance, and trend intent.
3. Scan all configured source families.
4. Capture the exact source URL, date, query, observed fact, and why it suggests a topic.
5. Normalize records and deduplicate.
6. Return 20-50 canonical topics in JSON.
7. Upsert the same records to Feishu when access is available.

## Source families

- Google Search or equivalent web search
- Google Trends or equivalent relative-interest data
- industry media
- competitor blogs and owned content
- Reddit and specialist forums
- YouTube videos, reviews, and comments
- associations and standards bodies
- regulation and policy sites
- FAQs, reviews, support pages, and customer questions
- SERP People Also Ask, related searches, and autocomplete

## Candidate capture

Record:

- candidate topic and keyword
- source family, publisher, URL, and observation date
- exact query or discovery path
- target customer, market, intent, and buyer stage
- observed evidence and reason
- product relevance and commercial connection
- duplicate fingerprint and related source URLs

## Deduplication

Deduplicate at three levels:

1. canonical URL and syndicated copies
2. multiple reports of the same underlying event
3. different wording with the same user intent and expected answer

Keep a separate regional or audience version only when the answer, regulation, buyer, or conversion path materially differs. Preserve corroborating URLs in `supporting_sources`.

## Topic balance

Avoid producing only informational topics. Balance:

- problems and jobs-to-be-done
- evaluation and comparison
- supplier and purchase intent
- regulation and compliance
- application, installation, maintenance, and troubleshooting
- trend and timely response
- product proof, case study, and risk reduction

## Signal limits

- Google Trends values are relative interest, not search volume.
- PAA and autocomplete are question-discovery signals, not demand volume.
- Reddit, forum, review, and YouTube activity reveal language and pain, not market size.
- Competitor claims require independent verification when used as facts.
