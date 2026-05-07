"""Command-line interface for ReadRover.

Usage:
    readrover ask "your research question here"
    readrover ask "..." --output brief.md --max-papers 3
"""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.markdown import Markdown

from readrover.config import settings
from readrover.graph import build_graph

app = typer.Typer(help="ReadRover — multi-agent research assistant.")
console = Console()


@app.command()
def ask(
    question: str = typer.Argument(..., help="Research question to investigate"),
    output: Path | None = typer.Option(
        None, "--output", "-o", help="Write the brief to a file (default: stdout)"
    ),
    max_papers: int = typer.Option(
        settings.top_k_papers, "--max-papers", "-n", help="Max papers to retrieve"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show agent traces"),
) -> None:
    """Run the full ReadRover pipeline on a single question."""
    settings.top_k_papers = max_papers

    graph = build_graph()
    console.rule(f"[bold cyan]ReadRover[/bold cyan]: {question}")

    final_state = graph.invoke({"question": question})

    brief = final_state.get("brief", "")
    if not brief:
        console.print("[red]No brief produced. Check logs.[/red]")
        raise typer.Exit(code=1)

    if output:
        output.write_text(brief, encoding="utf-8")
        console.print(f"[green]Brief written to {output}[/green]")
    else:
        console.print(Markdown(brief))


@app.command()
def version() -> None:
    """Print ReadRover version."""
    from readrover import __version__

    console.print(f"readrover {__version__}")


if __name__ == "__main__":
    app()
