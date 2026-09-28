# Feishu Topics Schema

Use a Feishu Bitable when ongoing filtering, ownership, status, and review dates are needed. Use a Feishu document only for a static report.

## Recommended fields

| Field | Type | Required | Purpose |
|---|---|---:|---|
| Topic ID | Text | Yes | Stable key such as product-market-cluster-slug |
| Product | Text | Yes | Normalized product name |
| Topic | Text | Yes | Canonical topic title |
| Cluster | Single select | Yes | Pillar or thematic group |
| Angle | Text | No | Specific editorial or research angle |
| Audience | Multi-select | Yes | User, buyer, decision maker, channel partner |
| Country/City | Multi-select | No | Geographic scope |
| Language | Single select | No | Planned publishing language |
| Intent | Single select | Yes | Learn, compare, buy, source, comply, troubleshoot |
| Funnel Stage | Single select | Yes | Awareness, consideration, decision, retention |
| Source Families | Multi-select | Yes | Search, Trends, Media, Competitor, Reddit, YouTube, Association, Official, FAQ, PAA |
| Evidence Summary | Long text | Yes | Short factual basis |
| Primary URL | URL | Yes | Best evidence source |
| Supporting URLs | Long text | No | Other sources, one per line |
| Why Now | Long text | Yes | Trigger, timing, or momentum |
| Suggested Format | Single select | No | Article, landing page, video, FAQ, sales brief, report |
| Suggested Channel | Multi-select | No | Website, Google, LinkedIn, YouTube, email, sales |
| Topic Score | Number | Yes | 0-100 |
| Confidence | Single select | Yes | High, Medium, Low |
| Status | Single select | Yes | New, Review, Approved, In Progress, Published, Parked |
| Owner | Person | No | Responsible person |
| Review Date | Date | No | Next validation or production date |
| Created At | Date/time | Yes | First creation time |
| Updated At | Date/time | Yes | Last material update |
| Notes | Long text | No | Caveats and follow-up |

## Stable key and upsert

Build `Topic ID` from normalized product, target market, cluster, and canonical intent. Before writing:

1. Read the destination schema.
2. Search for matching Topic ID.
3. Update an existing record when the evidence or score changed.
4. Create a record only when no match exists.
5. Never erase owner, status, or editorial notes without explicit instruction.

## Minimal import columns

When the full schema is unavailable, export:

`Topic ID, Product, Topic, Cluster, Audience, Market, Intent, Funnel Stage, Evidence Summary, Primary URL, Why Now, Topic Score, Confidence, Status`

## Recommended views

- Top Opportunities: Topic Score descending, score at least 80
- By Product: grouped by Product and Cluster
- By Market: grouped by Country/City
- Commercial Intent: source, buy, compare, and comply intents
- Needs Review: low confidence or review date due
- Production Board: Kanban by Status

## Write safety

Preview the proposed field mapping and row count before a large first write. If only a report is requested, do not write to Feishu automatically.
