# ReadRover 🦫

> **Multi-agent research assistant** — ask a research question, get a citation-backed brief synthesized from arXiv papers in minutes.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://img.shields.io/badge/CI-passing-brightgreen.svg)](#)
[![LangGraph](https://img.shields.io/badge/built%20with-LangGraph-purple.svg)](https://langchain-ai.github.io/langgraph/)

<!-- TODO: replace with a real demo GIF -->
![ReadRover demo](docs/demo.gif)

---

## Why?

Reading into a new field is brutal. You search arXiv, skim 20 abstracts, download 5 PDFs, get lost in jargon, and still aren't sure what's *contested* vs. what's *consensus*.

**ReadRover collapses that loop into a single question.**

Ask `"what's the state of small-model reasoning in 2026?"` and get back a 2-page citation-backed brief in ~60 seconds, with cross-paper contradictions surfaced explicitly.

---

## What it does

```
┌─────────────────────────────────────────────────────────────────┐
│  user question                                                   │
│       │                                                          │
│       ▼                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │ Search       │───▶│ PDF Reader   │───▶│ Critic       │      │
│  │ Planner      │    │ (parallel)   │    │              │      │
│  └──────────────┘    └──────────────┘    └──────┬───────┘      │
│                                                  │              │
│                              ┌───────────────────┘              │
│                              ▼                                   │
│                       [findings strong?] ──no──┐                │
│                              │ yes              │               │
│                              ▼                  └─▶ re-plan     │
│                       ┌──────────────┐                          │
│                       │ Writer       │                          │
│                       └──────┬───────┘                          │
│                              ▼                                   │
│                       citation-backed brief                      │
└─────────────────────────────────────────────────────────────────┘
```

| Sub-agent | Responsibility |
|---|---|
| **Search Planner** | Decomposes question into sub-questions; expands into arXiv queries |
| **PDF Reader** | Downloads top-N papers, extracts + chunks text, embeds into Chroma |
| **Critic** | Scores findings for coverage; flags contradictions across papers |
| **Writer** | Synthesizes a markdown brief with inline `[arxiv:1234.5678]` citations |

---

## Architecture

Built on:

| Piece | Tool |
|---|---|
| Agent orchestration | **LangGraph** (StateGraph + conditional edges) |
| LLM | Anthropic Claude (configurable) |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector store | **ChromaDB** (local) |
| Paper source | arXiv API |
| Tracing | LangSmith (optional) |
| UI | Streamlit |

See [`docs/architecture.md`](docs/architecture.md) for the full sequence diagram and design decisions.

---

## Results

Evaluated against 5 topics where a published survey exists. Coverage = % of survey's main claims captured. Faithfulness = % of agent claims grounded in retrieved chunks (LLM-as-judge).

<!-- TODO: populate from `make eval` -->

| Topic | Papers Used | Coverage vs. Survey | Faithfulness | Latency | Cost |
|---|---|---|---|---|---|
| Small-model reasoning | 5 | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| Vision transformers (post-2023) | 5 | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| RLHF alternatives | 5 | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| Long-context attention | 5 | _TBD_ | _TBD_ | _TBD_ | _TBD_ |
| Diffusion for code | 5 | _TBD_ | _TBD_ | _TBD_ | _TBD_ |

Reproduce with `make eval` (~10 min, ~$0.50 in API credits).

---

## Quick start

```bash
git clone https://github.com/<you>/readrover.git
cd readrover
uv pip install -e ".[dev]"          # or: pip install -e ".[dev]"
cp .env.example .env                  # add ANTHROPIC_API_KEY
readrover ask "what's the state of small-model reasoning in 2026?"
```

Run the Streamlit demo:

```bash
make demo                             # opens localhost:8501
```

Run the full evaluation:

```bash
make eval                             # takes ~10 min
```

---

## Project structure

```
readrover/
├── src/readrover/
│   ├── graph.py              # LangGraph workflow definition
│   ├── config.py             # settings (models, Chroma path, ...)
│   ├── cli.py                # `readrover ask "..."` entrypoint
│   ├── agents/
│   │   ├── search_planner.py # question → sub-questions → arXiv queries
│   │   ├── pdf_reader.py     # download + chunk + embed papers
│   │   ├── critic.py         # findings scoring + contradiction detection
│   │   └── writer.py         # final brief synthesis with citations
│   ├── retrieval/
│   │   └── vector_store.py   # ChromaDB wrapper
│   └── tools/
│       └── arxiv_client.py   # arXiv API calls
├── tests/                    # pytest unit tests
├── evals/                    # eval harness + golden topics
├── demo/                     # Streamlit app
└── docs/                     # architecture, design notes
```

---

## Roadmap

- [x] LangGraph skeleton with 4 sub-agents
- [x] arXiv API integration
- [x] PDF parsing + Chroma embedding
- [x] Eval harness (5 topics, LLM-as-judge)
- [ ] Streamlit demo deployed to HuggingFace Spaces
- [ ] Citation-graph traversal for multi-hop questions
- [ ] Semantic Scholar + Google Scholar fallback sources
- [ ] User feedback loop → eval set growth

---

## License

MIT — see [LICENSE](LICENSE).

---

_Built by [Nitheesh Pothireddy](https://www.linkedin.com/in/nitheesh-pothireddy/)._
