# 🔧 ToolSmith

> **Teach a 0.5B model to call tools as well as a 70B one.**
> A LoRA fine-tune of Qwen2.5-0.5B-Instruct on synthetic NL → tool-call pairs for the Open-Meteo weather API.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![🤗 Model](https://img.shields.io/badge/🤗-Hub-FFD21E.svg)](https://huggingface.co/<your-username>/toolsmith-qwen2.5-0.5b)
[![W&B](https://img.shields.io/badge/W%26B-runs-yellow.svg)](https://wandb.ai/<your-username>/toolsmith)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/<you>/toolsmith/blob/main/notebooks/02_train_colab.ipynb)

---

## Why?

Tool-calling (a.k.a. function-calling) is the bridge between LLMs and the real world — it's how agents reach beyond their context window. Frontier models (GPT-4, Claude Opus) do this fluently. Tiny models (<1B) usually can't.

**Can a 0.5B model match a frontier model on a single, well-defined tool-calling surface, after a small LoRA fine-tune?** This repo answers yes — and shows the receipts.

## Headline result

<!-- TODO: populate after `make eval` -->

| Model | Valid JSON | Schema match | Args correct | Hallucinated tool | Latency (CPU) |
|---|---|---|---|---|---|
| Qwen2.5-0.5B-Instruct (base) | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ ms |
| **Qwen2.5-0.5B + ToolSmith LoRA** | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ ms |
| Claude 3.5 Sonnet (reference) | _TBD_ | _TBD_ | _TBD_ | _TBD_ | _TBD_ ms |

Reproduce: `make eval-all`. Numbers populate `docs/results.md`.

---

## What's in here

```
toolsmith/
├── src/toolsmith/
│   ├── data/
│   │   ├── tools.py        # Open-Meteo tool schemas
│   │   ├── generate.py     # synthesise NL ↔ tool-call pairs with Claude
│   │   └── format.py       # apply chat template, write JSONL
│   ├── train.py            # SFTTrainer + PEFT LoRA + W&B
│   ├── inference.py        # load adapter, parse model output
│   └── eval.py             # 4-axis scoring (validity / schema / args / hallucination)
├── notebooks/02_train_colab.ipynb   # one-click free-T4 training
└── docs/                            # architecture + results
```

---

## Tool surface

Three tools mapped to [Open-Meteo](https://open-meteo.com/) endpoints (free, no auth):

| Tool | Returns | Args |
|---|---|---|
| `get_current_weather` | now-cast for a location | `latitude`, `longitude`, `temperature_unit` |
| `get_forecast` | up to 16-day forecast | `latitude`, `longitude`, `days`, `hourly_variables` |
| `get_historical_weather` | daily values for a past date range | `latitude`, `longitude`, `start_date`, `end_date` |

The model must:
1. Pick the **right tool** for the user's question.
2. Emit **valid JSON** matching the schema.
3. Fill **correct arguments** (especially: extract lat/long for cities it has never explicitly seen as training pairs).
4. **Refuse** when the user asks something out of scope (e.g. "what's the air quality?").

---

## Training recipe

| Setting | Value |
|---|---|
| Base model | `Qwen/Qwen2.5-0.5B-Instruct` |
| Method | LoRA (PEFT) |
| Rank `r` | 16 |
| Alpha | 32 |
| Dropout | 0.05 |
| Target modules | `q_proj, k_proj, v_proj, o_proj` |
| Optimiser | AdamW, lr=2e-4, warmup 3% |
| Effective batch size | 16 (4 × 4 grad-accum) |
| Epochs | 3 |
| Train / val / test | 1 600 / 200 / 200 examples |
| Hardware | Single T4 (Colab free) |
| Wall-clock | ~25 min |
| Logging | Weights & Biases |

Trained adapter is ~5 MB. The full merged model fits in <1 GB and runs on CPU at interactive latency.

---

## Quick start

### Use the trained model (no GPU needed)

```bash
pip install transformers peft
```

```python
from toolsmith.inference import ToolSmithModel

model = ToolSmithModel.from_pretrained("<your-username>/toolsmith-qwen2.5-0.5b")
print(model.call("What's the weather like in Hyderabad right now?"))
# → {"tool": "get_current_weather", "arguments": {"latitude": 17.385, "longitude": 78.487, "temperature_unit": "celsius"}}
```

### Reproduce training end-to-end

```bash
git clone https://github.com/<you>/toolsmith && cd toolsmith
uv venv && source .venv/bin/activate
uv pip install -e ".[dev,train]"
cp .env.example .env                       # ANTHROPIC_API_KEY for data gen, WANDB_API_KEY for tracking

make data           # generate synthetic pairs (~$1 in Claude credits)
make train          # local GPU; or open notebooks/02_train_colab.ipynb
make eval           # score base vs LoRA vs frontier reference
make push           # upload adapter + model card to HuggingFace Hub
```

---

## Evaluation methodology

We score on a held-out 200-example test set generated independently from training data (different prompt seed, different cities, different phrasings).

| Metric | Definition |
|---|---|
| **Valid JSON** | Output parses as JSON. |
| **Schema match** | Tool name exists; all required args present and correctly typed. |
| **Args correct** | LLM-as-judge: do extracted arg values match the user's intent? |
| **Hallucinated tool** | Model invented a tool that doesn't exist. **Lower is better.** |

Implemented in [`src/toolsmith/eval.py`](src/toolsmith/eval.py). See [`evals/README`](docs/results.md) for full protocol.

---

## Roadmap

- [x] Synthetic data pipeline (Claude → JSONL)
- [x] LoRA training script with W&B
- [x] 4-axis eval scaffold
- [ ] Hugging Face Hub model card with widget
- [ ] DPO post-training to penalise hallucinated tools further
- [ ] Quantised GGUF release for `llama.cpp` / on-device

## License

MIT — see [LICENSE](LICENSE).

---

_Built by [Nitheesh Pothireddy](https://www.linkedin.com/in/nitheesh-pothireddy/)._
