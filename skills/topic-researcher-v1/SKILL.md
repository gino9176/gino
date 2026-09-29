---
name: topic-researcher-v1
description: Transform an approved industry blog Topic Card into an evidence-first, traceable Research Pack with research questions, primary-source discovery, claim verification, contradictions, market voice, content gaps, confidence gates, SEO and Writer handoffs. Use after topic selection or Topic Scoring, for news, evergreen, mixed, regulation, market, buyer-education, comparison, or industry research. Also use when SEO Planner, Writer, or Editor returns a research or fact-check request. Do not use for topic discovery, topic scoring, keyword strategy, article writing, editing, or publishing.
---

# Topic Researcher V1

Build the evidence layer between an approved topic and downstream content production.

Core authority boundary:

- Topic Skill decides what to write.
- Topic Researcher decides what the available evidence supports.
- SEO Planner decides how to structure the content for search.
- Writer decides how to express approved facts.
- Editor checks the final content against the evidence.

Treat this skill as the Single Source of Evidence Truth for the content workflow.

## Scope

Do:

- consume an approved Topic Card without rescoring it;
- generate and prioritize Research Questions;
- search for authoritative, primary, secondary, opposing, community, and competitor evidence;
- extract normalized Evidence Units and Verified Claims;
- separate fact, inference, opinion, and market voice;
- check definitions, geography, time scope, source independence, and freshness;
- expose contradictions, rejected sources, gaps, limitations, and topic premise errors;
- calculate coverage and confidence with hard gates;
- emit one canonical Research Object as JSON and Markdown;
- emit SEO Handoff and Writer Handoff objects;
- respond to downstream Research Requests.

Do not:

- discover, select, score, or rescore topics;
- determine keyword strategy or create an SEO outline;
- write, rewrite, edit, or publish an article;
- silently change the approved topic;
- treat model memory, search snippets, or repeated derivative pages as evidence;
- invent facts, citations, quotes, numbers, dates, or conclusions.

## Load bundled resources

Before a research run, read:

- [research-modes.md](references/research-modes.md) to apply budgets, mandatory steps, escalation, and stop conditions;
- [source-hierarchy.md](references/source-hierarchy.md) to classify and select sources;
- [confidence-rules.md](references/confidence-rules.md) to calculate source, claim, coverage, and research confidence;
- [freshness-policy.md](references/freshness-policy.md) to determine temporal validity.

Read [failure-handling.md](references/failure-handling.md) when a source fails, evidence is missing, claims conflict, a premise is wrong, or the run may be partial.

Read [runtime-adapters.md](references/runtime-adapters.md) when deploying or orchestrating this skill in Claude Code, Codex, OpenClaw, or n8n.

Use [config.example.yaml](config.example.yaml) as a portable default configuration. Let an explicit user or workflow configuration override it.

## Input contract

Accept JSON, YAML, a Feishu record, or a natural-language brief. Normalize the input before research and validate the normalized object against [topic-card.schema.json](schemas/topic-card.schema.json).

The canonical Topic Card contains:

~~~json
{
  "topic_id": "T-YYYYMMDD-001",
  "topic": "Approved topic concept",
  "primary_keyword": "primary query",
  "topic_type": "news",
  "target_markets": ["Germany"],
  "output_language": "en",
  "target_customer": "E-bike brands",
  "search_intent": "VERIFY",
  "source_trigger": {
    "event_id": "EV-001",
    "knowledge_gap_id": null,
    "signal_ids": ["SIG-001"],
    "primary_source_url": null
  },
  "topic_score": 84,
  "score_reason": ["Strong buyer relevance"],
  "research_priority": "high",
  "research_mode": "standard",
  "upstream": {}
}
~~~

Default "research_mode" to "standard" only when absent.

Consume "topic_score" and "score_reason" as context. Never change them or calculate a replacement score.

### Normalize market-topic-v1 output

When input comes from "market-topic-v1":

- map "topic_concept" to "topic";
- use "suggested_title" only as context, never as the factual premise;
- map "target_market" to "target_markets";
- preserve "target_customer", "primary_role", "secondary_role", "buyer_stage", "search_intent", "primary_keyword", and "secondary_keywords" in "upstream";
- map "event_id", "knowledge_gap_id", "signal_ids", and "lineage" into "source_trigger" or "upstream";
- map "NEWS" and "NEWS_ANALYSIS" to "news";
- map durable buyer, technical, commercial, FAQ, and evergreen concepts to "evergreen";
- use "mixed" when both a current event and durable knowledge question are essential;
- preserve the upstream score object; do not reinterpret it as research confidence.

If required data is missing and materially changes the research, return an input error rather than guessing. Conservative, non-material assumptions must appear in "metadata.assumptions".

## Topic premise protection

Do not directly modify an approved topic.

When the premise is false, too broad, ambiguous, outdated, or unsupported, set "topic_issue" and return "NOT_READY" when the issue affects a critical question.

~~~json
{
  "topic_issue": true,
  "issue_type": "premise_error",
  "original_premise": "Why Region X banned Product Y",
  "verified_reality": "The authority published a proposal, not a ban.",
  "recommended_revision": "What Region X's proposed Product Y rule could mean",
  "impact": "The original framing would overstate the official action."
}
~~~

## Execution workflow

Execute in this order:

1. Normalize and validate the Topic Card.
2. Select Quick, Standard, or Deep mode.
3. Load any prior Research Object and test every reused object for definition, geography, and freshness.
4. Generate Research Questions before browsing.
5. Assign each question "critical", "important", or "optional".
6. Expand queries by terminology, language, authority, opposition, report title, and file type.
7. Discover the organizations most qualified to answer each critical question.
8. Search primary evidence first, then independent secondary evidence.
9. Extract sources, Evidence Units, data points, definitions, and provisional claims.
10. Normalize definitions, geography, periods, units, populations, and source lineage.
11. Verify claims and identify derivative or duplicate evidence chains.
12. Run contradiction search for every material conclusion in Standard and Deep modes.
13. Collect clustered Voice of Market signals without treating them as verified facts.
14. Scan SERP and competitor coverage only after the factual evidence base exists.
15. Identify content gaps without creating an SEO outline.
16. Evaluate coverage and run the recovery ladder for unresolved important questions.
17. Apply confidence rules and hard quality gates.
18. Assign "READY", "READY_WITH_LIMITATIONS", or "NOT_READY".
19. Validate the canonical object against [research-pack.schema.json](schemas/research-pack.schema.json).
20. Emit "research_pack.json", "research_report.md", SEO Handoff, and Writer Handoff from the same object.

Never browse randomly before Research Questions exist.

## Research Questions

Adapt questions to the topic instead of applying a fixed checklist.

For news, normally establish:

- what happened, when, where, and who announced it;
- the exact status: confirmed, developing, disputed, or unverified;
- what changed and what did not;
- the official wording, effective date, next step, and affected parties;
- material context, impact, counterevidence, and remaining uncertainty.

For evergreen research, normally establish:

- definition, mechanism, use case, and boundaries;
- buyer, evaluator, specification, decision, and risk questions;
- recurring mistakes, objections, alternatives, and practical implications;
- authoritative data, durable evidence, and common market language.

Use stable IDs: "RQ01", "RQ02", and so on. Record priority, status, confidence, claim IDs, and gap impact.

## Search and authority strategy

Search in layers:

1. official, regulatory, standards, statistics, filings, original research, original datasets, and company primary material;
2. strong independent media, research organizations, professional databases, and specialist publications;
3. commercial, supplier, distributor, competitor, and trade content;
4. community, forum, social, video, review, and customer discussion.

Match the source to the claim. A forum can support a repeated-pain-point finding but cannot verify a regulation.

Use multilingual queries when local terminology or local authorities matter. Preserve the original term and add a labeled translation.

Distinguish answer search from authority discovery. Once the competent authority or original publisher is known, prioritize its material over summaries.

## Evidence model

Treat the Claim-Evidence relationship, not the webpage, as the core research unit.

Use stable IDs:

- Topic: "T-YYYYMMDD-001"
- Research Question: "RQ01"
- Claim: "C01"
- Evidence: "E01"
- Source: "S01"
- Definition: "D01"
- Data Point: "DP01"
- Contradiction: "X01"
- Gap: "G01"

Validate standalone Evidence Units against [evidence-unit.schema.json](schemas/evidence-unit.schema.json).

Each important claim must link to one or more Evidence IDs. Each Evidence Unit must link to a Source ID and at least one Research Question.

Separate:

- "fact": directly supported descriptive statement;
- "inference": a bounded conclusion linked to supporting Claim IDs;
- "opinion": an attributed judgment;
- "market_voice": a clustered report of what participants say or ask.

Never turn an inference into a fact. Never use unattributed opinion as fact.

For numbers, always preserve value, unit, period, geography, population, definition, and Source ID.

## Verification checks

Before combining or comparing evidence, check:

- definition match;
- geography match;
- period and publication date;
- current, historical, background, or superseded status;
- primary versus derivative lineage;
- methodology and sample;
- whether sources are meaningfully independent.

Three articles that repeat one original report count as one evidence chain.

Search snippets may help discovery. They do not qualify as evidence until the underlying source is opened and evaluated.

## Contradictions and challenge search

For Standard and Deep runs, actively search against each major conclusion using decline, failure, criticism, dispute, exception, delay, cancellation, correction, and alternative explanations.

Do not silently choose between conflicting sources. Create a contradiction object containing both positions, the material difference, likely causes, resolution status, and Writer guidance.

An unresolved critical contradiction blocks Writer Ready.

## Voice of Market and competitor coverage

Cluster repeated questions, complaints, terminology, objections, decision factors, and misconceptions from community or customer sources.

Label the result "market_voice" and include this warning in the Research Pack:

"Market Voice describes repeated participant language; it is not verified factual evidence."

After factual research, scan the top relevant SERP results and deeply review the most relevant competitor pages within the selected mode budget. Record angles, questions, evidence quality, omissions, outdated claims, and opportunities.

Identify content gaps. Do not create headings or a content outline.

## Coverage, recovery, and stopping

Measure coverage by Research Questions, not source count.

Use the recovery ladder when evidence is missing:

"original query -> rewrite -> synonym -> formal term -> local-language term -> authority query -> original report title -> PDF -> domain search -> citation tracing -> Evidence Gap"

Stop when:

- all critical questions are covered;
- important-question coverage meets the mode threshold;
- primary evidence and material claims are sufficient;
- definition, geography, and freshness checks pass;
- required contradiction search is complete;
- more searching has low decision value.

Do not search merely to reach a source quota.

## Status and gates

Return exactly one status:

- "READY": all hard gates pass and no material limitation prevents normal use.
- "READY_WITH_LIMITATIONS": critical gates pass, but disclosed non-critical gaps or limitations remain.
- "NOT_READY": a critical gap, unresolved critical contradiction, material premise error, unverified core news event, invalid definition, or schema failure remains.

A high average score never overrides a failed critical gate.

Writer Ready requires:

- 100% critical-question coverage;
- no unresolved critical contradiction;
- no unverified critical claim;
- acceptable definition, geography, and freshness;
- traceable core evidence;
- valid Research Pack structure.

## Canonical output

Create one Research Object. Render both outputs from it:

- "research_pack.json" for automation, databases, Feishu, and downstream skills;
- "research_report.md" for human review, using [research-report.md](templates/research-report.md).

Do not independently generate two conclusions.

The JSON must conform to [research-pack.schema.json](schemas/research-pack.schema.json). Use "null" for unknown values; never insert invented values to satisfy the schema.

## Handoffs and feedback

Generate machine-readable SEO and Writer handoffs and validate them against [handoff.schema.json](schemas/handoff.schema.json).

SEO Handoff may include verified terminology, definitions, subtopics, competitor coverage, buyer questions, market voice, strong data IDs, content gaps, and evidence limitations. It must not contain an SEO outline.

Writer Handoff may include safe Claim IDs, cautious Claim IDs, prohibited Claim IDs, strongest data IDs, must-cite Source IDs, definitions, counterarguments, pain points, gaps, and limitations.

Downstream systems must not silently research around this skill. Accept feedback messages:

- "RESEARCH_REQUEST"
- "TOPIC_REVISION_REQUEST"
- "SEO_REVISION_REQUEST"
- "FACT_CHECK_REQUEST"

Update the Research Pack while preserving IDs and audit history. Do not replace an earlier claim silently; mark it superseded and link the replacement.

## Audit trail

Preserve a lightweight audit trail:

- research mode and dates;
- Research Questions and status;
- sources considered, used, and rejected;
- rejection reasons;
- reused and revalidated objects;
- evidence gaps and contradictions;
- coverage and confidence;
- schema validation and final status.

Do not store every low-value query unless the caller explicitly requests a full trace.

## Hard rules

1. Do not select or score topics.
2. Do not write the final article.
3. Begin with Research Questions.
4. Prefer primary evidence over derivative content.
5. Optimize evidence quality, not source volume.
6. Trace every important claim to evidence.
7. Keep fact, inference, opinion, and market voice separate.
8. Treat snippets as discovery aids, not evidence.
9. Never treat model knowledge as evidence.
10. Never convert absence of evidence into evidence.
11. Never resolve conflicts silently.
12. Never let duplicate sources increase confidence.
13. Block Writer Ready when a critical gap remains.
14. Expose uncertainty.
15. Never fabricate a citation, source, quote, number, date, or research result.
16. Do not bypass paywalls, access controls, robots restrictions, or unavailable APIs.
17. Preserve the user's requested output language while retaining useful source-language terms.
18. Use absolute dates for time-sensitive claims.
19. Keep reused evidence subject to freshness and scope checks.
20. Let hard gates override scores.

## V1 boundary

Do not build a full knowledge graph, advanced entity graph, article generator, complex machine-learning score, publishing system, keyword strategy engine, topic scorer, or industry ontology.

Optimize for:

"Evidence > Volume; Primary Source > Repetition; Traceability > Apparent Certainty; Explicit Uncertainty > Hallucinated Completeness; Coverage > Source Count."
