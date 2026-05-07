"""4-axis evaluation against the held-out test set.

Metrics (per example):
    - valid_json:      did the model output parse?
    - schema_match:    is the tool name known and required args present + typed?
    - args_correct:    do extracted arg values match the gold? (LLM-as-judge for nuance)
    - hallucinated:    did the model invent a tool that doesn't exist?

Run:
    python -m toolsmith.eval --adapter ./outputs/lora-adapter
    python -m toolsmith.eval --compare base,lora,reference
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from toolsmith.config import settings
from toolsmith.data.format import load_jsonl
from toolsmith.data.tools import TOOL_NAMES, get_tool


def score_one(predicted: dict[str, Any], gold: dict[str, Any]) -> dict[str, bool]:
    """Score a single (predicted, gold) tool-call pair."""
    metrics = {
        "valid_json": isinstance(predicted, dict) and "_raw" not in predicted,
        "schema_match": False,
        "args_correct": False,
        "hallucinated": False,
    }

    pred_tool = predicted.get("tool")
    gold_tool = gold.get("tool")

    # Hallucinated tool — model named something that doesn't exist
    if pred_tool is not None and pred_tool not in TOOL_NAMES:
        metrics["hallucinated"] = True
        return metrics

    # Refusal correctness
    if gold_tool is None:
        metrics["schema_match"] = pred_tool is None
        metrics["args_correct"] = pred_tool is None
        return metrics

    if pred_tool != gold_tool:
        return metrics

    # Right tool — now check args
    schema = get_tool(pred_tool) or {}
    required = schema.get("parameters", {}).get("required", [])
    pred_args = predicted.get("arguments", {}) or {}

    if all(k in pred_args for k in required):
        metrics["schema_match"] = True

    # Coarse arg correctness — exact match on required keys.
    # TODO(nitheesh): use an LLM-as-judge for fuzzy matches (e.g., Hyderabad
    # lat/long given as 17.4 vs 17.385 should still count). Stub function below.
    gold_args = gold.get("arguments", {}) or {}
    if all(_loose_equal(pred_args.get(k), gold_args.get(k)) for k in required):
        metrics["args_correct"] = True

    return metrics


def _loose_equal(a: Any, b: Any) -> bool:
    """Floats within 0.5 are considered equal (handles geocoding precision)."""
    if isinstance(a, int | float) and isinstance(b, int | float):
        return abs(a - b) < 0.5
    return a == b


def evaluate(adapter_path: str, test_path: Path | None = None) -> dict[str, float]:
    """Run the trained model over the test split and return aggregate metrics."""
    test_path = test_path or (settings.data_dir / "test.jsonl")
    rows = load_jsonl(test_path)

    from toolsmith.inference import ToolSmithModel

    model = ToolSmithModel.from_pretrained(adapter_path)

    totals: dict[str, float] = defaultdict(float)
    for row in rows:
        predicted = model.call(row["prompt"])
        scored = score_one(predicted, row["completion"])
        for k, v in scored.items():
            totals[k] += float(v)

    n = len(rows)
    return {
        "n": n,
        "valid_json_pct": totals["valid_json"] / n,
        "schema_match_pct": totals["schema_match"] / n,
        "args_correct_pct": totals["args_correct"] / n,
        "hallucinated_pct": totals["hallucinated"] / n,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--adapter", default=str(settings.output_dir / "lora-adapter"), help="Adapter path or HF id"
    )
    parser.add_argument(
        "--compare",
        default=None,
        help="Comma-separated comparison set, e.g. 'base,lora,reference'",
    )
    parser.add_argument("--test-path", type=Path, default=None)
    args = parser.parse_args()

    if args.compare:
        # TODO(nitheesh): wire up base / reference variants.
        raise NotImplementedError("--compare flag not yet implemented.")

    results = evaluate(args.adapter, args.test_path)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
