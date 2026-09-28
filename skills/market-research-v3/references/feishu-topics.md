# Feishu Topic Database

Use a Feishu Bitable as the canonical topic database.

## Core fields

| Field | Type | Required |
|---|---|---:|
| Topic ID | Text | Yes |
| Topic | Text | Yes |
| Keyword | Text | Yes |
| Search Intent | Single select | Yes |
| Buyer Stage | Single select | Yes |
| Target Country | Multi-select | Yes |
| Target Customer | Multi-select | Yes |
| Product Relevance | Number | Yes |
| Commercial Intent | Number | Yes |
| Freshness | Number | Yes |
| Difficulty | Number | No |
| Difficulty Basis | Single select | Yes |
| Evidence Available | Checkbox | Yes |
| Source Type | Multi-select | Yes |
| Source URL | URL | Yes |
| Supporting Sources | Long text | No |
| Evidence Summary | Long text | Yes |
| Search Volume | Number | No |
| Keyword Difficulty | Number | No |
| CPC | Number | No |
| CPC Currency | Text | No |
| SEO Provider | Single select | No |
| SEO Query Date | Date | No |
| Search Demand Basis | Single select | Yes |
| Search Demand Score | Number | Yes |
| Buyer Intent Score | Number | Yes |
| Product Relevance Score | Number | Yes |
| Commercial Value Score | Number | Yes |
| Content Opportunity Score | Number | Yes |
| Freshness Score | Number | Yes |
| Total Score | Number | Yes |
| Score Explanation | Long text | Yes |
| Status | Single select | Yes |
| Confidence | Single select | Yes |
| Owner | Person | No |
| Research Pack URL | URL | No |
| Editorial Notes | Long text | No |
| First Seen | Date/time | Yes |
| Last Updated | Date/time | Yes |

## Controlled values

Search Intent: Informational, Comparison, Commercial, Transactional, Sourcing, Compliance, Troubleshooting.

Buyer Stage: Awareness, Problem Definition, Solution Evaluation, Supplier Evaluation, Purchase, Post-purchase.

Status: Reject, Backlog, Research, Priority Research, Researching, Research Complete, Content Queue, Published.

Search Demand Basis: Verified, Proxy.

Difficulty Basis: SEO Provider, AI Qualitative Proxy, Unknown.

## Topic ID and upsert

Build Topic ID from normalized product, market, target customer, and canonical intent. Before writing, search for the ID. Update evidence, scores, and dates when it exists; create only when absent.

Never overwrite Owner, Editorial Notes, or a downstream workflow Status without explicit instruction.

## Recommended views

- New Scout Results
- Priority Research: score 85-100
- Research Queue: score 75-84
- Backlog: score 60-74
- Rejected: below 60
- Missing SEO Data
- Low Confidence
- Research Complete

If Feishu access is unavailable, output the same fields as JSON and CSV-ready rows.
