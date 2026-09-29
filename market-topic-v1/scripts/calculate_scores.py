#!/usr/bin/env python3
"""Calculate deterministic Market Topic V1 score totals.

Accept either one Topic object or a complete output object with a topics
array. Read JSON from a file or stdin and write updated JSON to stdout or a
file. This script does not invent component scores.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


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


def load_json(path: str) -> Any:
    if path == "-":
        return json.load(sys.stdin)
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(data: Any, path: str) -> None:
    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if path == "-":
        sys.stdout.write(rendered)
        return
    Path(path).write_text(rendered, encoding="utf-8")


def numeric(value: Any, label: str, maximum: float) -> float:
    if value is None and label == "search_growth":
        return 0.0
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be numeric")
    if value < 0 or value > maximum:
        raise ValueError(f"{label} must be between 0 and {maximum}")
    return float(value)


def score_band(value: int) -> str:
    if value >= 90:
        return "P0_IMMEDIATE"
    if value >= 80:
        return "P1_HIGH_PRIORITY"
    if value >= 70:
        return "P2_RECOMMENDED"
    if value >= 60:
        return "P3_BACKLOG"
    return "REJECT_ARCHIVE"


def calculate_topic(topic: dict[str, Any]) -> None:
    scores = topic.get("scores")
    if not isinstance(scores, dict):
        raise ValueError("topic.scores must be an object")

    trend = scores.get("trend")
    if not isinstance(trend, dict) or not isinstance(trend.get("components"), dict):
        raise ValueError("scores.trend.components must be an object")
    trend_components = trend["components"]
    missing_trend = sorted(set(TREND_MAX) - set(trend_components))
    if missing_trend:
        raise ValueError(f"missing Trend components: {', '.join(missing_trend)}")
    trend_total = sum(
        numeric(trend_components[name], name, maximum)
        for name, maximum in TREND_MAX.items()
    )
    trend["total"] = round(trend_total, 2)

    blog = scores.get("blog_value")
    if not isinstance(blog, dict) or not isinstance(blog.get("components"), dict):
        raise ValueError("scores.blog_value.components must be an object")
    blog_components = blog["components"]
    missing_blog = sorted(set(BLOG_MAX) - set(blog_components))
    if missing_blog:
        raise ValueError(f"missing Blog Value components: {', '.join(missing_blog)}")

    blog_total = 0.0
    for name, maximum in BLOG_MAX.items():
        component = blog_components[name]
        if not isinstance(component, dict):
            raise ValueError(f"Blog Value component {name} must be an object")
        if component.get("max") != maximum:
            raise ValueError(f"{name}.max must equal {maximum}")
        blog_total += numeric(component.get("score"), name, maximum)
    blog["total"] = round(blog_total, 2)

    base = round(blog_total * 0.70 + trend_total * 0.30, 2)
    scores["base_priority"] = base

    boosts = scores.get("boosts", [])
    penalties = scores.get("penalties", [])
    if not isinstance(boosts, list) or not isinstance(penalties, list):
        raise ValueError("boosts and penalties must be arrays")

    boost_total = 0.0
    for adjustment in boosts:
        value = adjustment.get("value") if isinstance(adjustment, dict) else None
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
            raise ValueError("boost values must be non-negative numbers")
        boost_total += value

    penalty_total = 0.0
    for adjustment in penalties:
        value = adjustment.get("value") if isinstance(adjustment, dict) else None
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value > 0:
            raise ValueError("penalty values must be non-positive numbers")
        penalty_total += value

    final = max(0, min(100, round(base + boost_total + penalty_total)))
    scores["final_priority"] = final
    scores["band"] = score_band(final)

    topic_type = topic.get("topic_type")
    special_queue = None
    if topic_type in {"NEWS", "NEWS_ANALYSIS"} and trend_total >= 85 and blog_total >= 65:
        special_queue = "URGENT_REVIEW"
    elif blog_total >= 85 and trend_total < 30:
        special_queue = "EVERGREEN_PRIORITY"
    scores["special_queue"] = special_queue


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="-", help="JSON file or - for stdin")
    parser.add_argument("-o", "--output", default="-", help="JSON file or - for stdout")
    args = parser.parse_args()

    try:
        data = load_json(args.input)
        topics = data.get("topics") if isinstance(data, dict) else None
        if isinstance(topics, list):
            for topic in topics:
                if not isinstance(topic, dict):
                    raise ValueError("each topic must be an object")
                calculate_topic(topic)
        elif isinstance(data, dict):
            calculate_topic(data)
        else:
            raise ValueError("input must be a Topic object or an output object")
        write_json(data, args.output)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
