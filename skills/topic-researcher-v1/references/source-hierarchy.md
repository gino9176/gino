# Source hierarchy

Use source fitness, not prestige alone. Classify every source and record why it is appropriate for the claim.

## Tiers

| Tier | Typical sources | Best use |
|---|---|---|
| 1 | regulator, government, standards body, official statistics, filing, original dataset, peer-reviewed original research, company primary announcement | law, status, dates, official figures, original actions |
| 2 | strong independent media, research institute, established specialist publication, professional database | context, independent corroboration, synthesis |
| 3 | supplier, distributor, consultancy, competitor, commercial report, trade content | industry practice, commercial framing, leads to original evidence |
| 4 | forum, Reddit, social post, comment, review, creator content | market language, pain points, hypotheses, source leads |

A Tier 4 source may be highly useful for market voice. It is not sufficient for a legal, regulatory, technical, statistical, or company-status claim.

## Source score

Score each usable source from 0 to 100 using [confidence-rules.md](confidence-rules.md). Tier and score are related but not identical. A Tier 1 page outside the relevant definition or period can still be weak evidence for the claim.

## Claim-source fit

Ask:

1. Is this the original publisher or action owner?
2. Does it directly support the exact claim?
3. Does it use the same definition, geography, period, and population?
4. Is the methodology visible?
5. Is it current enough?
6. Is it independent from other corroborating sources?

## Provenance

Record "original_source_id" and "independence_group".

If several pages rely on the same report, filing, press release, dataset, or wire story, assign the same independence group. Do not count them as independent corroboration.

Trace secondary claims back to the original source when feasible. Retain the secondary page when it adds useful interpretation, but do not mislabel it as primary.

## Source status

Use:

- "used": supports a claim, definition, data point, contradiction, or market-voice cluster;
- "context_only": useful orientation but not claim evidence;
- "rejected": not reliable or relevant enough;
- "unavailable": the full source could not be evaluated.

Use rejection reasons:

- "duplicate_derivative"
- "unclear_methodology"
- "scope_mismatch"
- "outdated_or_superseded"
- "missing_attribution"
- "snippet_only"
- "paywalled_unverifiable"
- "access_failed"
- "promotional_without_support"
- "irrelevant"
- "other"

## Evidence capture

For each source preserve:

- title, publisher, URL, language;
- publication date, event date, retrieval date, and data period when applicable;
- source type, tier, score, geography, and independence group;
- concise evidence summary;
- a short exact quote only when materially useful;
- the IDs of supported Research Questions, Evidence Units, and Claims.

Do not store excessive copyrighted text. Prefer a faithful evidence summary plus a short quote.

## Trusted and negative source memory

A Trusted Source Registry may speed up authority discovery, but authority is topic-specific. Re-evaluate each claim.

Negative Source Memory may lower search priority for recurring aggregators, poor attribution, outdated material, or SEO-only pages. Do not blacklist a domain solely because one page was weak.
