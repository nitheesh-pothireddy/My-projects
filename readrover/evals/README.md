# Evaluation Harness

This is the part recruiters care about most: **how do you know it works?**

## Methodology

We evaluate ReadRover on a small set of research topics where a published
human-written survey already exists (the "reference"). For each topic, we:

1. Run `readrover ask "<topic question>"` and capture the brief.
2. Score the brief along three axes using LLM-as-judge:
   - **Coverage** — % of the reference survey's main claims captured.
   - **Faithfulness** — % of the brief's claims grounded in retrieved chunks
     (not hallucinated).
   - **Citation validity** — % of `[arxiv:...]` references that resolve to
     a real arXiv ID retrieved during the run.
3. Also record latency (s) and cost (USD).

Results land in `evals/results/<run-id>.json` and a markdown summary in
`evals/results/<run-id>.md`.

## Topics

See [`topics.json`](topics.json). To add a topic:

```json
{
  "id": "your-topic-id",
  "question": "Your research question.",
  "reference_survey_url": "https://arxiv.org/abs/...",
  "reference_main_claims": [
    "Claim 1.",
    "Claim 2.",
    "..."
  ]
}
```

## Run

```bash
make eval                      # full suite
python evals/run_eval.py --topic small-model-reasoning   # single topic
```

Cost: ~$0.50 for the full 5-topic suite using `claude-3-5-sonnet-latest`.

## Reading results

The runner writes a results table to stdout and JSON for each run to
`evals/results/`. Open `evals/results/latest.md` for the human-readable view.
