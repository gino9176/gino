# Workflow

## Run-mode matrix

| Mode | Trend Engine | Evergreen Engine | Main window | Output |
|---|---|---|---|---|
| `daily` | Required | Reuse current map; add only strong new gaps | 0-72 hours plus prior comparison window | 3 Top-5 lists + Overall Top 10 |
| `weekly` | Required | Required | 7-day recap plus 14-90-day emerging signals | 3 Top-5 lists + Overall Top 10 |
| `monthly` | Rescore only | Required audit | Existing database and current coverage | map expansion, cleanup, rescoring, gap list |

Focused collection ceilings:

- Daily: about 200-350 raw signals.
- Weekly: about 500-1,000 raw signals.
- Monthly: no broad news recrawl.

These are ceilings, not targets. Return fewer items when evidence is weak. `deep` increases coverage but not the output quotas.

## Execution stages

1. **Configure:** validate input, timezone, markets, languages, customer, roles, website, competitors, and access.
2. **Load memory:** retrieve Signals, Events, Topics, Knowledge Map, published content, approved queue, research queue, and rejected/archive history.
3. **Plan queries:** create queries by source function, product synonym, target market, local language, buyer role, and event type.
4. **Collect:** record raw results without scoring them as topics.
5. **Clean:** canonicalize URLs, normalize dates and entities, remove spam and exact duplicates.
6. **Cluster:** combine reports about the same event using semantic similarity, entities, event type, time window, and keywords.
7. **Map gaps:** compare expected industry knowledge with own content, competitor coverage, search questions, buyer journey, and customer pain.
8. **Generate concepts:** create audience- and intent-specific Topic Concepts; do not write titles yet.
9. **Govern:** fingerprint, compare, deduplicate, mark relationships, and preserve rejected memory.
10. **Score:** calculate Trend, Blog Value, Priority, boosts, penalties, bands, and special queues.
11. **Title:** generate one restrained suggested title for each surviving concept.
12. **Rank:** maintain Trending, Commercial, Evergreen, and Overall lists.
13. **Validate:** run deterministic validation and repair all errors.
14. **Persist:** upsert Feishu only when authorized; otherwise return JSON and CSV-ready tables.

## Event status

- `BREAKING`: normally 0-72 hours.
- `TRENDING`: normally 3-14 days.
- `EMERGING`: normally 14-90 days or an older issue with fresh acceleration.
- `STABLE`: sustained without meaningful growth.
- `DECLINING`: momentum or target relevance is falling.
- `ARCHIVED`: no longer actionable.

Use the latest meaningful update and observed momentum. Do not classify by age alone.

## Topic lifecycle

`DISCOVERED -> SCORED -> REVIEW -> APPROVED -> HANDED_TO_RESEARCHER`

Side or terminal states:

- `MERGED`
- `REJECTED`
- `EXPIRED`

When a time-sensitive topic expires, create a new Evergreen concept only when its framing and value genuinely change. Preserve the relationship and original lineage.

## Error handling

- Continue after one source fails; record source, error, impact, and retryability.
- Set `run.partial=true` when a missing category materially reduces coverage.
- Keep authoritative claims with weak evidence as unverified signals; block confident wording.
- Keep unavailable search-growth and SEO data `null`.
- Preserve original-language text and label translations.
- Distinguish event date, data period, publication date, and discovery time.
- Do not bypass paywalls, access controls, robots restrictions, or unavailable APIs.
- When topic memory is unavailable, disclose the narrower deduplication scope.

## Human-readable summary

Report:

- raw and valid signal counts;
- event count;
- generated, qualified, and priority-topic counts;
- the four rankings;
- important coverage gaps;
- partial-run warnings;
- items needing human review.

Do not expose hundreds of raw links as the primary result.
