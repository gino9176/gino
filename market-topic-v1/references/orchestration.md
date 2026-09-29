# Orchestration

The same contract must work in Claude Code, Codex, OpenClaw, and n8n. Keep intelligence rules in this Skill and orchestration outside it.

## Shared invocation

Pass:

- the contents or path of **SKILL.md**;
- one configuration matching **schemas/input.schema.json**;
- prior topic memory when available;
- web or search tools;
- optional Feishu and SEO-provider credentials through the runtime's normal secret mechanism;
- an output path for one JSON object matching **schemas/output.schema.json**.

Do not place credentials in prompts, examples, logs, or GitHub.

## Claude Code

1. Place or clone the skill directory in the workspace.
2. Instruct Claude Code to read SKILL.md and the referenced resources.
3. Supply a config based on **templates/config.example.yaml**.
4. Request JSON output at a known path.
5. Run **python3 scripts/validate_output.py result.json**.
6. Persist only after validation succeeds.

## Codex

Invoke **$market-topic-v1** with a configuration or natural-language brief. Load referenced files progressively, browse when current evidence is needed, validate the result, and stop at Topic Score.

## OpenClaw

Define one agent job with:

- the Skill directory mounted read-only;
- config passed as job input;
- tool permissions limited to required search, database, and Feishu actions;
- JSON result as job output;
- the validation command as the final local step.

Keep scheduling and retry policy in OpenClaw, not in the Skill.

## n8n

Recommended flow:

**Schedule Trigger -> Build Config -> Execute Agent -> Parse JSON -> Validate -> Upsert Feishu -> Notify / Error Branch**

n8n responsibilities:

- schedule Daily, Weekly, and Monthly runs;
- retrieve prior Feishu rows or database memory;
- pass configuration and memory to the agent;
- parse returned JSON;
- call validation;
- upsert verified rows;
- retry transport failures;
- notify a human about P0, Urgent Review, validation failure, or partial coverage.

n8n must not independently:

- invent topics;
- change scoring weights;
- deduplicate by title only;
- calculate subjective component scores;
- rewrite human approval or manual status;
- call Researcher automatically before approval.

## Idempotency

Use stable **run_id**, **signal_id**, **event_id**, **knowledge_id**, and **topic_id**. Repeating the same job should update evidence and machine-owned fields without creating duplicate records.

## Failure handling

- Retry network and rate-limit failures with bounded backoff.
- Do not retry invalid configuration or schema errors without correction.
- Route partial results to review when an important source category is unavailable.
- Keep the last verified result if a new run fails.
- Log the failing stage without exposing credentials or full sensitive payloads.
