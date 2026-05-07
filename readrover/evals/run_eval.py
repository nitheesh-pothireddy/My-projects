"""Evaluation harness runner.

Loads `evals/topics.json`, runs ReadRover on each, scores the brief along
three axes (coverage / faithfulness / citation validity) and writes a results
table to `evals/results/`.

Usage:
    python evals/run_eval.py                       # all topics
    python evals/run_eval.py --topic <topic-id>    # single topic
    python evals/run_eval.py --dry-run             # plan only, no LLM calls
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EVAL_DIR = Path(__file__).parent
RESULTS_DIR = EVAL_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def load_topics() -> list[dict[str, Any]]:
    return json.loads((EVAL_DIR / "topics.json").read_text())


def run_topic(topic: dict[str, Any]) -> dict[str, Any]:
    """Run ReadRover on one topic and score the brief."""
    from readrover.graph import build_graph

    started = time.time()
    graph = build_graph()
    final_state = graph.invoke({"question": topic["question"]})
    latency_s = time.time() - started

    brief = final_state.get("brief", "")

    # TODO(nitheesh): replace these placeholders with real LLM-as-judge scoring.
    coverage = score_coverage(brief, topic["reference_main_claims"])
    faithfulness = score_faithfulness(brief, final_state.get("chunks", []))
    citation_validity = score_citation_validity(brief, final_state.get("papers", []))

    return {
        "topic_id": topic["id"],
        "question": topic["question"],
        "brief": brief,
        "metrics": {
            "coverage": coverage,
            "faithfulness": faithfulness,
            "citation_validity": citation_validity,
            "latency_s": round(latency_s, 1),
        },
    }


def score_coverage(brief: str, reference_claims: list[str]) -> float:
    """% of reference_claims plausibly covered in the brief.

    TODO: implement with an LLM call:
        For each reference_claim, ask the judge LLM:
            "Does the brief make a claim that semantically matches:
             '{reference_claim}'? yes/no"
        Return the fraction of yeses.
    """
    if not brief:
        return 0.0
    return 0.0  # placeholder


def score_faithfulness(brief: str, chunks: list[Any]) -> float:
    """% of brief claims that can be traced to a retrieved chunk.

    TODO: implement with an LLM call. Decompose the brief into atomic claims,
    then for each claim ask the judge:
        "Is this claim supported by any of these chunks? yes/no"
    Return the fraction of yeses.
    """
    if not brief:
        return 0.0
    return 0.0  # placeholder


def score_citation_validity(brief: str, papers: list[Any]) -> float:
    """% of [arxiv:XXXX] citations in the brief that match a retrieved paper."""
    import re

    citations = re.findall(r"\[arxiv:([\d.]+v?\d*)\]", brief)
    if not citations:
        return 0.0
    paper_ids = {p.arxiv_id if hasattr(p, "arxiv_id") else p["arxiv_id"] for p in papers}
    valid = sum(1 for c in citations if c in paper_ids)
    return valid / len(citations)


def write_summary(results: list[dict[str, Any]], run_id: str) -> Path:
    """Write a markdown summary table."""
    lines = [
        f"# ReadRover Eval — {run_id}",
        "",
        "| Topic | Coverage | Faithfulness | Citation Valid | Latency (s) |",
        "|---|---|---|---|---|",
    ]
    for r in results:
        m = r["metrics"]
        lines.append(
            f"| {r['topic_id']} | {m['coverage']:.0%} | {m['faithfulness']:.0%} | "
            f"{m['citation_validity']:.0%} | {m['latency_s']} |"
        )
    summary_path = RESULTS_DIR / f"{run_id}.md"
    summary_path.write_text("\n".join(lines) + "\n")
    (RESULTS_DIR / "latest.md").write_text("\n".join(lines) + "\n")
    return summary_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", help="Run only one topic by id")
    parser.add_argument("--dry-run", action="store_true", help="Validate setup, no LLM calls")
    args = parser.parse_args()

    topics = load_topics()
    if args.topic:
        topics = [t for t in topics if t["id"] == args.topic]
        if not topics:
            raise SystemExit(f"No topic with id '{args.topic}'")

    if args.dry_run:
        print(f"Would run {len(topics)} topic(s):")
        for t in topics:
            print(f"  - {t['id']}: {t['question']}")
        return

    run_id = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    results = []
    for topic in topics:
        print(f"\n→ Running {topic['id']} ...")
        try:
            result = run_topic(topic)
            results.append(result)
            print(f"  ✓ coverage={result['metrics']['coverage']:.0%}")
        except Exception as exc:  # noqa: BLE001
            print(f"  ✗ {exc}")
            results.append({"topic_id": topic["id"], "error": str(exc), "metrics": {}})

    json_path = RESULTS_DIR / f"{run_id}.json"
    json_path.write_text(json.dumps(results, indent=2, default=str))

    summary_path = write_summary([r for r in results if "metrics" in r], run_id)
    print(f"\nResults: {json_path}\nSummary: {summary_path}")


if __name__ == "__main__":
    main()
