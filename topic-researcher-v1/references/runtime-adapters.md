# Runtime adapters

The portable contract is:

"Topic Card JSON -> research execution -> Research Pack JSON + Research Report Markdown"

The skill logic stays in this folder. The runtime supplies search, browsing, storage, scheduling, and credentials.

## Shared runtime rules

- Load "SKILL.md" as the controlling procedure.
- Pass one canonical Topic Card per research job.
- Give the agent access to current web search and page-reading tools.
- Require full-source inspection for evidence; snippets are discovery only.
- Persist the final Research Pack, not hidden chain-of-thought.
- Validate JSON against "schemas/research-pack.schema.json".
- Keep state outside the model: topic history, sources, packs, requests, and versions.
- Never place provider credentials in prompts, files, logs, or Research Packs.

## Claude Code

Use the skill folder as project instructions or explicitly tell Claude Code to read "skills/topic-researcher-v1/SKILL.md".

Provide:

- the Topic Card file or JSON;
- output directory;
- allowed research tools;
- optional prior Research Pack.

Require it to write "research_pack.json" first, validate it, then render "research_report.md".

Do not ask Claude Code to make editorial or publishing changes in the same run.

## Codex

Invoke "$topic-researcher-v1" when installed, or direct Codex to this folder in a repository.

Provide the Topic Card and any prior pack. Let Codex use available search or browser tools while preserving citations and source URLs.

Keep code or repository mutations outside the research run unless the user separately requests them.

## OpenClaw

Mount or copy the folder into the agent's skill directory and expose the skill name "topic-researcher-v1".

Configure:

- one job per Topic Card;
- web search and page fetch permissions;
- a durable store for Research Packs and source registry;
- a maximum run time and source budget matching the selected mode;
- JSON as the inter-agent message format.

Use the handoff schema for messages to SEO Planner, Writer, or Editor.

## n8n

Use n8n as orchestrator, not evidence authority.

Recommended nodes:

1. Trigger: schedule, webhook, Feishu status change, or manual run.
2. Load Topic Card.
3. Validate or normalize the Topic Card.
4. AI Agent: execute this Skill with web research tools.
5. Structured Output Parser: use "research-pack.schema.json".
6. Quality Gate: branch on "research_status" and "quality.writer_ready".
7. Store "research_pack.json" and "research_report.md".
8. Send SEO and Writer handoffs only when permitted.
9. Route feedback messages back to Researcher.

For long Standard or Deep runs, split orchestration into discovery, evidence extraction, and pack assembly steps, but keep one canonical Research Object.

Do not implement research judgment as scattered n8n expressions. n8n should schedule, pass inputs, store outputs, validate structure, route states, retry technical failures, and request human review.

## Status routing

- "READY" -> allow SEO Planner and Writer handoffs.
- "READY_WITH_LIMITATIONS" -> allow handoff with limitations visible; optionally require human review.
- "NOT_READY" -> block Writer; route to Researcher retry, topic revision, or human review.
- "TOPIC_PREMISE_ERROR" -> route upstream; do not let Researcher silently rename the topic.

## Idempotency and versions

Use "topic_id" plus a research version or run ID as the idempotency key.

On rerun:

- preserve stable object IDs when meaning is unchanged;
- append new sources and audit entries;
- mark changed claims superseded;
- never overwrite human review fields;
- preserve prior pack versions for audit.
