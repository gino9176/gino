# Feishu Bitable Model

Use four tables. Do not combine raw signals, events, knowledge nodes, and topics into one table.

## 01 Signals

Required fields:

**signal_id**, **title**, **summary**, **source_name**, **source_type**, **source_tier**, **source_url**, **published_at**, **event_date**, **first_seen_at**, **country**, **language**, **entities**, **keywords**, **evidence_class**, **authority_score**, **raw_relevance**, **event_id**, **status**, **run_id**.

Status: **NEW**, **VALID**, **DUPLICATE**, **NOISE**, **CLUSTERED**.

## 02 Events

Required fields:

**event_id**, **event_name**, **event_summary**, **event_type**, **first_seen**, **latest_meaningful_update**, **last_seen**, **signal_count**, **source_count**, **source_type_count**, **countries**, **entities**, **primary_source**, **evidence_sources**, **event_status**, seven Trend component scores, **trend_score**, **cluster_confidence**, **run_id**.

Status: **BREAKING**, **TRENDING**, **EMERGING**, **STABLE**, **DECLINING**, **ARCHIVED**.

## 03 Topics

Store the complete Topic object from **schemas/output.schema.json**, including:

- concept and suggested title;
- type, content role, and angle;
- cluster and knowledge node;
- customer, roles, buyer stage, and intent;
- market and keywords;
- why_now and why_write;
- source lineage;
- Trend and Blog Value components;
- base priority, adjustments, final priority, band, and special queue;
- duplicate status and overlap score;
- graph relationships;
- lifecycle status and rejection reason;
- run ID and evidence timestamp.

## 04 Knowledge Map

Required fields:

**knowledge_id**, **parent_id**, **level_1**, **level_2**, **level_3**, **knowledge_name**, **description**, **importance**, **buyer_relevance**, **target_roles**, **existing_content_count**, **approved_topic_count**, **competitor_coverage**, **search_demand**, **content_gap_score**, **last_scanned**, **status**.

## Upsert policy

1. Inspect table names, field names, types, and options before writing.
2. Map existing fields; do not create near-duplicate columns.
3. Search by stable ID.
4. Update changed machine-owned fields and create only missing records.
5. Preserve owner, approval, manual status, editorial notes, manual priority, and Researcher assignment.
6. Record run_id and update timestamp.
7. Verify the returned record IDs and sample records.
8. If Feishu is unavailable, return JSON and CSV-ready rows; never claim a write occurred.

## Suggested views

- Signals — New / Noise Review
- Events — Breaking / Emerging / Declining
- Topics — P0-P1 / Review / Evergreen / Cannibalization / Rejected
- Knowledge Map — High Gap / Needs Confirmation
