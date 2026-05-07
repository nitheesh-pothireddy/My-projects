# Detailed Results

> Populated by `make eval-all` after a training run.

## Headline numbers

| Model | Valid JSON | Schema match | Args correct | Hallucinated tool | Latency (CPU, p50) |
|---|---|---|---|---|---|
| Qwen2.5-0.5B-Instruct (base, zero-shot) | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| Qwen2.5-0.5B-Instruct (base, few-shot) | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| **Qwen2.5-0.5B + ToolSmith LoRA** | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| Claude 3.5 Sonnet (reference) | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ |

Test set: 200 held-out examples generated independently from training (different RNG seed, different city set).

## Per-tool breakdown

| Tool | LoRA accuracy | Most common failure mode |
|---|---|---|
| `get_current_weather` | _TBD_ | _TBD_ |
| `get_forecast` | _TBD_ | _TBD_ |
| `get_historical_weather` | _TBD_ | _TBD_ |
| out-of-scope refusal | _TBD_ | _TBD_ |

## Training curves

[Link to W&B run]

- Train / eval loss
- Gradient norm
- Learning-rate schedule
- Token throughput

## Failure analysis

After running `make eval`, populate this section with 5-10 representative failures from the test set, each with:

- the user prompt
- the model's output
- the gold completion
- a one-line diagnosis

Doing this is the difference between a portfolio project and a *good* portfolio project. It signals that you read your model's outputs.

## Cost summary

| Phase | Cost | Time |
|---|---|---|
| Data generation (Claude) | ~$1.00 | ~5 min |
| Training (T4) | $0 (Colab free) | ~25 min |
| Eval (LoRA + base) | <$0.01 | ~2 min |
| Eval (Claude reference) | ~$0.30 | ~3 min |
| **Total** | **~$1.30** | **~35 min** |
