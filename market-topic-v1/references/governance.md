# Topic Governance

## Memory stores

Compare every new Topic Concept with:

1. published content;
2. approved topics;
3. research queue;
4. rejected and archived topic memory.

Reject does not mean delete. Retain the topic, score, timestamp, and rejection reason.

## Fingerprint

Create:

~~~json
{
  "core_entity": "...",
  "primary_problem": "...",
  "audience": "...",
  "buyer_stage": "...",
  "intent": "...",
  "angle": "...",
  "knowledge_node": "...",
  "keyword_cluster": ["..."]
}
~~~

Use a stable normalized serialization of this object to derive **topic_id**.

## Overlap Score

| Component | Points |
|---|---:|
| Semantic similarity | 30 |
| Search-intent overlap | 25 |
| Keyword-cluster overlap | 20 |
| Knowledge-node overlap | 10 |
| Audience overlap | 5 |
| Buyer-stage overlap | 5 |
| Angle overlap | 5 |

Map:

- 90-100: **REJECT_DUPLICATE**
- 80-89: **MERGE** or **UPDATE_EXISTING**
- 65-79: **CANNIBALIZATION_RISK**
- 40-64: **RELATED**
- below 40: **NEW**

## Decision rules

- Use **UPDATE_EXISTING** when the same intent should refresh an existing article.
- Use **MERGE** when the new concept adds useful evidence or angles but does not justify a separate article.
- Use **CANNIBALIZATION_RISK** when separate articles may compete for the same search need.
- Use **RELATED** when two articles can coexist and should be linked.
- Use **REJECT_DUPLICATE** only when a separate article creates no distinct buyer job.

Do not auto-reject solely from numeric similarity. When audience, intent, or angle creates a genuinely different job, explain the exception and send it to human review.

## Graph relations

Maintain:

- **related_to**
- **supports**
- **updates**
- **competes_with**
- **derived_from**
- **belongs_to**

Preserve:

**Source -> Signal -> Event / Knowledge Gap -> Angle -> Audience -> Intent -> Topic Concept -> Score -> Suggested Title**

## Stable identity

- Do not derive identity from the suggested title.
- Normalize capitalization, punctuation, and singular/plural variants.
- Preserve original terms in evidence while normalizing comparison keys.
- Do not change an existing ID when a title changes.
- Create a new topic when an expired trend is reframed as an Evergreen concept; connect it with **derived_from**.

## Human-owned fields

Never overwrite:

- owner;
- approval decision;
- editorial note;
- manual priority;
- manual status;
- rejection explanation;
- Researcher assignment.

Machine-generated fields may be refreshed only when the evidence timestamp and run ID are also stored.
