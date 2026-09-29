# Scoring

Keep evidence confidence separate from topic value. Store a rationale and evidence references for every component.

## Trend Score — 100

| Component | Max | V1 rubric |
|---|---:|---|
| Recency | 15 | <24h=15, 1-3d=12, 4-7d=9, 8-14d=6, 15-30d=3, >30d=0-2; use latest meaningful update |
| Velocity | 20 | >5x=20, 3-5x=17, 2-3x=14, 1.5-2x=10, 1-1.5x=5, declining=0; mark a zero-baseline surge NEW_SPIKE and justify |
| Independent source count | 10 | 1=2, 2-3=4, 4-6=6, 7-15=8, 15+=10; deduplicate domains |
| Source authority | 15 | Tier A present=15; multiple Tier B=12; Tier C only=7; Tier D only=3; no usable evidence=0 |
| Cross-platform signal | 15 | 1 type=2, 2=5, 3=8, 4=11, 5+=15 |
| Search growth | 15 | >300%=15, 150-300%=12, 50-150%=9, 10-50%=5, stable=2, declining=0; unavailable=null and zero in arithmetic |
| Market relevance | 10 | none=0, outside target only=2, secondary market=4, one primary market=6, several targets=8, broad/direct target impact=10 |

Store the seven component scores under **scores.trend.components**. Their numeric values must total **scores.trend.total**.

## Blog Value Score — 100

| Component | Max | Evaluate |
|---|---:|---|
| Buyer relevance | 25 | effect on buyer cost, compliance, supplier, lead time, risk, performance, or sales |
| Commercial relevance | 20 | proximity to RFQ, supplier, comparison, compliance, cost, specification, or purchase |
| Expertise / EEAT value | 15 | opportunity to demonstrate technical, manufacturing, quality, regulatory, or operational expertise |
| Search opportunity | 15 | demand, growth, long-tail depth, PAA, intent clarity, and SERP weakness |
| Product relevance | 10 | closeness to the configured offer |
| Content gap | 10 | own-site, competitor, and SERP gap |
| Evergreen potential | 5 | durable value independent of the event |

For each component store **score**, **max**, **evidence**, and a one-sentence rationale. Use the full range. Do not cluster every topic near the middle.

## Priority

~~~text
base_priority = round(blog_value_score * 0.70 + trend_score * 0.30, 2)
final_priority = clamp(round(base_priority + sum(boost values) + sum(penalty values)), 0, 100)
~~~

Penalty values are stored as negative numbers.

Allowed boosts:

- major regulation affecting target buyers: +10
- repeated buyer pain across channels: +8
- major competitor coverage with a clear own-site gap: +5
- new product or technology directly affecting the roadmap: +5

Allowed penalties:

- duplicate topic: -100
- strong cannibalization: -30
- already published recently: -40
- weak source support: -10
- clickbait-only angle: -15
- low target-market relevance: -20
- outdated: -20
- no buyer relevance: -30

Record **rule**, **value**, **reason**, and evidence for every adjustment. Never add an adjustment to force a preferred rank.

## Bands and special queues

- 90-100: **P0_IMMEDIATE**
- 80-89: **P1_HIGH_PRIORITY**
- 70-79: **P2_RECOMMENDED**
- 60-69: **P3_BACKLOG**
- below 60: **REJECT_ARCHIVE**

Special queues:

- **URGENT_REVIEW**: NEWS or NEWS_ANALYSIS with Trend at least 85 and Blog Value at least 65.
- **EVERGREEN_PRIORITY**: Blog Value at least 85 and Trend below 30.

Keep the underlying band when assigning a special queue.

## Rankings

Maintain:

- Breaking / Trending Top 5
- Buyer / Commercial Top 5
- Evergreen Top 5
- Overall Top 10

Break ties by higher Blog Value, Buyer Relevance, Commercial Relevance, source support, then Trend Score.

Exclude **REJECT_DUPLICATE**, **MERGED**, and **REJECT_ARCHIVE** from Overall Top 10 unless a human explicitly overrides.
