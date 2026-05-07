"""PDF Reader agent.

Responsibility:
    1. Run each search query against arXiv (via tools/arxiv_client).
    2. Deduplicate by arxiv_id, keep top_k_papers.
    3. Download each PDF, extract text page-by-page.
    4. Chunk text (size + overlap from settings).
    5. Embed chunks and add to the Chroma collection scoped to this question.

Inputs:  state.search_queries
Outputs: state.papers, state.chunks

Implementation hints:
    - Parallelise PDF downloads with httpx + asyncio (or simple ThreadPoolExecutor).
    - Use pypdf for text extraction. Skip pages with <50 chars (figure-only pages).
    - Use a langchain RecursiveCharacterTextSplitter for chunking.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from readrover.graph import State


def run(state: "State") -> dict:
    """Fetch papers, chunk + embed, return updated state."""
    # TODO(nitheesh): implement steps 1-5.
    #   1. from readrover.tools.arxiv_client import search
    #      papers = []
    #      for q in state.search_queries:
    #          papers.extend(search(q, limit=settings.top_k_papers))
    #   2. dedupe by arxiv_id, slice to top_k_papers
    #   3. download PDFs, extract text
    #   4. chunk with RecursiveCharacterTextSplitter
    #   5. from readrover.retrieval.vector_store import VectorStore
    #      vs = VectorStore(collection=hash(state.question))
    #      vs.add_chunks(chunks)
    #   return {"papers": papers, "chunks": chunks}
    raise NotImplementedError("Implement pdf_reader.run — see docstring TODO.")
