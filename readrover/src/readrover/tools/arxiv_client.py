"""Thin wrapper around the `arxiv` Python client.

We expose one function: `search(query, limit) -> list[Paper]`.
That keeps the rest of the codebase decoupled from arxiv's specifics.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import arxiv

if TYPE_CHECKING:
    from readrover.graph import Paper


def search(query: str, limit: int = 5) -> list["Paper"]:
    """Search arXiv and return up to `limit` papers as our internal Paper model."""
    from readrover.graph import Paper

    client = arxiv.Client(page_size=limit, delay_seconds=3.0, num_retries=3)
    search_obj = arxiv.Search(
        query=query,
        max_results=limit,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    return [
        Paper(
            arxiv_id=result.get_short_id(),
            title=result.title.strip(),
            authors=[a.name for a in result.authors],
            abstract=result.summary.strip(),
            published=result.published.isoformat(),
            pdf_url=result.pdf_url,
        )
        for result in client.results(search_obj)
    ]


def download_pdf(pdf_url: str, dest_path: str) -> str:
    """Stream a PDF to disk; returns the local path."""
    import httpx

    with httpx.stream("GET", pdf_url, follow_redirects=True, timeout=60.0) as response:
        response.raise_for_status()
        with open(dest_path, "wb") as fh:
            for chunk in response.iter_bytes(chunk_size=8192):
                fh.write(chunk)
    return dest_path
