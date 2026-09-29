# Confidence and quality rules

Use rules and hard gates. Scores explain judgments; they do not create evidence.

## Source score: 0-100

| Component | Max | Evaluate |
|---|---:|---|
| Authority | 30 | competence and responsibility for the subject |
| Directness | 20 | direct support for the exact claim |
| Methodology | 15 | transparent method, sample, definitions, or data provenance |
| Scope match | 15 | definition, geography, period, population |
| Freshness | 10 | validity for the current question |
| Independence | 10 | independence from other evidence chains |

Record every component. A score of 80 or more is strong, 65-79 usable, 50-64 limited, below 50 normally context-only or rejected.

Never average away a fatal scope mismatch. A wrong geography, definition, or superseded rule can make a source unusable regardless of total score.

## Claim confidence

Use exactly:

- "high": direct, scope-matched evidence from at least one strong primary source, or two meaningfully independent strong sources; no unresolved material contradiction;
- "medium": credible support exists but one material limitation remains, or corroboration is weaker; use qualified wording;
- "low": plausible but indirect, narrow, old, method-limited, or based mainly on market voice; use only as background or hypothesis;
- "unverified": reliable support is absent or a critical contradiction remains; prohibit factual use.

Writer mapping:

| Confidence | writer_usage |
|---|---|
| high | direct |
| medium | qualified |
| low | background_only |
| unverified | prohibited |

An inference must list "based_on_claim_ids". Its confidence cannot exceed the weakest indispensable supporting claim without an explicit justification.

## Corroboration

Use:

- "strong": independent evidence chains agree and scope matches;
- "moderate": support agrees but independence or scope is partially limited;
- "weak": mostly derivative or indirect support;
- "none": one usable evidence chain only;
- "conflicting": material sources disagree.

Quantity alone never increases corroboration.

## Coverage score

Weight Research Questions:

- critical = 5
- important = 3
- optional = 1

Coverage factor:

- covered = 1
- partial = 0.5
- gap = 0
- not_applicable = exclude from denominator

Calculate:

"coverage_score = 100 * sum(weight * factor) / sum(applicable weights)"

Also report category coverage separately.

Default gate:

- critical coverage = 100%;
- important coverage >= 80%;
- optional coverage = best effort.

## Research confidence: 0-100

| Component | Weight |
|---|---:|
| Critical and important RQ coverage | 30 |
| Verified Claim confidence | 25 |
| Source quality and scope match | 20 |
| Primary-source coverage | 10 |
| Contradiction resolution | 10 |
| Temporal validity | 5 |

Classify:

- 90-100: very_high
- 80-89: high
- 65-79: moderate
- 50-64: weak
- below 50: insufficient

Return component scores and rationale.

## Hard gates

Set "writer_ready" to false when any applies:

- critical RQ is partial or gap;
- critical claim is unverified;
- unresolved critical contradiction exists;
- material definition, geography, or temporal mismatch exists;
- core news event is only rumored, anonymous, or social;
- material topic premise error exists;
- core evidence is not traceable;
- schema validation fails.

A passing confidence total cannot override a failed hard gate.

## Status mapping

- "READY": all gates pass and limitations are not material.
- "READY_WITH_LIMITATIONS": all critical gates pass; important but non-blocking limitations are disclosed.
- "NOT_READY": any hard gate fails.

Do not manipulate scores to obtain a desired status.
