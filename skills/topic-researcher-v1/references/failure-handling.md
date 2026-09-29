# Failure handling

Continue safely after ordinary source failures, but never hide reduced coverage.

## Search recovery ladder

Apply in order:

1. rewrite the exact question;
2. use synonyms and alternate phrasing;
3. use formal, legal, scientific, or industry terminology;
4. search in the relevant local language;
5. search the competent authority or organization;
6. search the cited report or dataset title;
7. search PDF and document formats;
8. search the authoritative domain;
9. trace citations from a credible secondary source;
10. record an Evidence Gap.

Stop when additional attempts have low expected decision value.

## Access failure

Do not bypass paywalls, authentication, robots restrictions, regional blocks, or unavailable APIs.

When the full source cannot be evaluated:

- mark it "unavailable";
- do not treat its snippet as evidence;
- search for the original public source or independent coverage;
- record the impact when the source was important.

## Missing evidence

Create an Evidence Gap with:

- stable Gap ID;
- Research Question ID;
- priority;
- gap type;
- recovery attempted;
- impact;
- status;
- recommended next action.

Gap types:

- "no_reliable_source"
- "primary_source_unavailable"
- "definition_unresolved"
- "geography_mismatch"
- "freshness_failure"
- "methodology_unclear"
- "conflict_unresolved"
- "access_failure"
- "other"

A critical open gap returns "NOT_READY".

## Conflicting evidence

Compare definition, geography, period, population, sample, method, preliminary/final status, and primary/derivative lineage.

If the difference is resolved, preserve the contradiction and resolution.

If unresolved:

- downgrade affected claims;
- provide neutral Writer guidance;
- block Writer Ready when critical.

## Premise error

Do not repair the topic silently. Return "topic_issue" with:

- issue type;
- original premise;
- verified reality;
- evidence IDs;
- recommended revision;
- impact.

Use issue types:

- "premise_error"
- "too_broad"
- "ambiguous"
- "outdated"
- "unsupported"

## Partial run

Set "metadata.partial" to true when a missing source category, failed provider, unavailable jurisdiction, or time limit materially reduces research coverage.

A partial run may be "READY_WITH_LIMITATIONS" only when all critical gates still pass. Otherwise use "NOT_READY".

## Schema or output failure

Do not coerce unknown values into invented content.

If validation fails:

1. repair structure without changing evidence meaning;
2. validate again;
3. if still invalid, return "NOT_READY";
4. disclose the validation errors in the audit trail.
