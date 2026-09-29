#!/usr/bin/env python3
"""Validate Market Topic V1 output without third-party packages."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


TOP_KEYS = {
    "run", "summary", "signals", "events", "knowledge_map", "topics",
    "rankings", "errors",
}

TREND_MAX = {
    "recency": 15,
    "velocity": 20,
    "source_count": 10,
    "source_authority": 15,
    "cross_platform": 15,
    "search_growth": 15,
    "market_relevance": 10,
}

BLOG_MAX = {
    "buyer_relevance": 25,
    "commercial_relevance": 20,
    "eeat_value": 15,
    "search_opportunity": 15,
    "product_relevance": 10,
    "content_gap": 10,
    "evergreen_potential": 5,
}

TOPIC_REQUIRED = {
    "topic_id", "topic_concept", "suggested_title", "topic_type",
    "content_role", "angle", "industry_cluster", "knowledge_node",
    "target_customer", "primary_role", "secondary_role", "buyer_stage",
    "search_intent", "target_market", "primary_keyword",
    "secondary_keywords", "seo_metrics", "why_now", "why_write",
    "event_id", "knowledge_gap_id", "signal_ids", "fingerprint", "scores",
    "duplicate_status", "overlap_score", "related_topic_ids",
    "pillar_topic_id", "lineage", "publish_window", "status",
}


def close(a: float, b: float) -> bool:
    return math.isclose(a, b, rel_tol=0, abs_tol=0.011)


def band(value: int) -> str:
    if value >= 90:
        return "P0_IMMEDIATE"
    if value >= 80:
        return "P1_HIGH_PRIORITY"
    if value >= 70:
        return "P2_RECOMMENDED"
    if value >= 60:
        return "P3_BACKLOG"
    return "REJECT_ARCHIVE"


def number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def validate_topic(topic: Any, index: int, errors: list[str], warnings: list[str]) -> None:
    prefix = f"topics[{index}]"
    if not isinstance(topic, dict):
        errors.append(f"{prefix} must be an object")
        return

    missing = sorted(TOPIC_REQUIRED - set(topic))
    if missing:
        errors.append(f"{prefix} missing fields: {', '.join(missing)}")
        return

    if not topic["topic_id"] or not topic["topic_concept"] or not topic["suggested_title"]:
        errors.append(f"{prefix} has an empty identity, concept, or title")
    if not topic["target_market"]:
        errors.append(f"{prefix}.target_market must not be empty")
    if not topic["why_write"]:
        errors.append(f"{prefix}.why_write must not be empty")
    if not topic["lineage"]:
        errors.append(f"{prefix}.lineage must not be empty")
    if topic["event_id"] is None and topic["knowledge_gap_id"] is None:
        errors.append(f"{prefix} must link to an event or knowledge gap")

    scores = topic.get("scores")
    if not isinstance(scores, dict):
        errors.append(f"{prefix}.scores must be an object")
        return

    trend = scores.get("trend", {})
    t_components = trend.get("components", {}) if isinstance(trend, dict) else {}
    if set(t_components) != set(TREND_MAX):
        errors.append(f"{prefix} Trend component keys do not match V1")
        return

    trend_total = 0.0
    for name, maximum in TREND_MAX.items():
        value = t_components[name]
        if value is None and name == "search_growth":
            value = 0
        if not number(value) or value < 0 or value > maximum:
            errors.append(f"{prefix} Trend {name} is outside 0-{maximum}")
            return
        trend_total += value
    if not number(trend.get("total")) or not close(trend_total, trend["total"]):
        errors.append(f"{prefix} Trend total should be {trend_total}")

    blog = scores.get("blog_value", {})
    b_components = blog.get("components", {}) if isinstance(blog, dict) else {}
    if set(b_components) != set(BLOG_MAX):
        errors.append(f"{prefix} Blog Value component keys do not match V1")
        return

    blog_total = 0.0
    for name, maximum in BLOG_MAX.items():
        component = b_components[name]
        if not isinstance(component, dict):
            errors.append(f"{prefix} Blog Value {name} must be an object")
            return
        score = component.get("score")
        if component.get("max") != maximum:
            errors.append(f"{prefix} Blog Value {name}.max must be {maximum}")
        if not number(score) or score < 0 or score > maximum:
            errors.append(f"{prefix} Blog Value {name}.score is outside 0-{maximum}")
            return
        if not component.get("rationale"):
            errors.append(f"{prefix} Blog Value {name} lacks rationale")
        blog_total += score
    if not number(blog.get("total")) or not close(blog_total, blog["total"]):
        errors.append(f"{prefix} Blog Value total should be {blog_total}")

    expected_base = round(blog_total * 0.70 + trend_total * 0.30, 2)
    if not number(scores.get("base_priority")) or not close(expected_base, scores["base_priority"]):
        errors.append(f"{prefix} base_priority should be {expected_base}")

    boosts = scores.get("boosts", [])
    penalties = scores.get("penalties", [])
    if not isinstance(boosts, list) or not isinstance(penalties, list):
        errors.append(f"{prefix} boosts and penalties must be arrays")
        return
    for adjustment in boosts:
        if not isinstance(adjustment, dict) or not number(adjustment.get("value")) or adjustment["value"] < 0:
            errors.append(f"{prefix} contains an invalid boost")
            return
    for adjustment in penalties:
        if not isinstance(adjustment, dict) or not number(adjustment.get("value")) or adjustment["value"] > 0:
            errors.append(f"{prefix} contains an invalid penalty")
            return

    expected_final = max(
        0,
        min(
            100,
            round(
                expected_base
                + sum(x["value"] for x in boosts)
                + sum(x["value"] for x in penalties)
            ),
        ),
    )
    if scores.get("final_priority") != expected_final:
        errors.append(f"{prefix} final_priority should be {expected_final}")
    if scores.get("band") != band(expected_final):
        errors.append(f"{prefix} band should be {band(expected_final)}")

    expected_queue = None
    if topic["topic_type"] in {"NEWS", "NEWS_ANALYSIS"} and trend_total >= 85 and blog_total >= 65:
        expected_queue = "URGENT_REVIEW"
    elif blog_total >= 85 and trend_total < 30:
        expected_queue = "EVERGREEN_PRIORITY"
    if scores.get("special_queue") != expected_queue:
        errors.append(f"{prefix} special_queue should be {expected_queue}")

    seo = topic.get("seo_metrics")
    if isinstance(seo, dict) and seo.get("provider") is None:
        numeric_metrics = [seo.get("search_volume"), seo.get("keyword_difficulty"), seo.get("cpc")]
        if any(value is not None for value in numeric_metrics):
            warnings.append(f"{prefix} has SEO metrics but no provider")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", help="Market Topic V1 result JSON")
    args = parser.parse_args()

    try:
        with Path(args.result).open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 1

    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(data, dict):
        print("ERROR: top level must be an object")
        return 1

    missing = sorted(TOP_KEYS - set(data))
    if missing:
        errors.append(f"missing top-level fields: {', '.join(missing)}")

    topics = data.get("topics", [])
    if not isinstance(topics, list):
        errors.append("topics must be an array")
        topics = []
    for index, topic in enumerate(topics):
        validate_topic(topic, index, errors, warnings)

    topic_ids = [topic.get("topic_id") for topic in topics if isinstance(topic, dict)]
    if len(topic_ids) != len(set(topic_ids)):
        errors.append("topic_id values must be unique")
    valid_ids = set(topic_ids)

    rankings = data.get("rankings", {})
    limits = {
        "trending_top_5": 5,
        "commercial_top_5": 5,
        "evergreen_top_5": 5,
        "overall_top_10": 10,
    }
    if not isinstance(rankings, dict):
        errors.append("rankings must be an object")
    else:
        for name, limit in limits.items():
            values = rankings.get(name)
            if not isinstance(values, list):
                errors.append(f"rankings.{name} must be an array")
                continue
            if len(values) > limit:
                errors.append(f"rankings.{name} exceeds {limit} items")
            if len(values) != len(set(values)):
                errors.append(f"rankings.{name} contains duplicates")
            unknown = sorted(set(values) - valid_ids)
            if unknown:
                errors.append(f"rankings.{name} references unknown topics: {', '.join(unknown)}")

    summary = data.get("summary", {})
    if isinstance(summary, dict):
        if summary.get("events") != len(data.get("events", [])):
            warnings.append("summary.events differs from events array length")
        if summary.get("generated_topics") != len(topics):
            warnings.append("summary.generated_topics differs from topics array length")
    else:
        errors.append("summary must be an object")

    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARNING: {message}")

    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"PASSED: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
