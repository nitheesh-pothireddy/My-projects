"""Pytest fixtures shared across the test suite."""

from __future__ import annotations

import pytest

from readrover.graph import Chunk, Finding, Paper, State


@pytest.fixture
def sample_paper() -> Paper:
    return Paper(
        arxiv_id="2401.00001",
        title="Toy Paper",
        authors=["A. Researcher"],
        abstract="A short abstract.",
        published="2024-01-01T00:00:00",
        pdf_url="https://arxiv.org/pdf/2401.00001",
    )


@pytest.fixture
def sample_chunk() -> Chunk:
    return Chunk(
        paper_id="2401.00001",
        text="Small models can match larger models when trained on curated data.",
        page=1,
    )


@pytest.fixture
def sample_finding(sample_chunk: Chunk) -> Finding:
    return Finding(
        claim="Curated training data helps small models match larger ones.",
        supporting_chunk_ids=[f"{sample_chunk.paper_id}::0"],
        confidence=0.9,
    )


@pytest.fixture
def initial_state() -> State:
    return State(question="What is the state of small-model reasoning in 2026?")
