"""Tiny Typer CLI entrypoint: `toolsmith call "..."`."""

from __future__ import annotations

import json

import typer
from rich.console import Console

app = typer.Typer(help="ToolSmith — tool-calling on a 0.5B model.")
console = Console()


@app.command()
def call(
    prompt: str = typer.Argument(..., help="User prompt"),
    adapter: str = typer.Option(
        "./outputs/lora-adapter", "--adapter", "-a", help="Path or HF Hub id"
    ),
) -> None:
    """Generate a tool call for a prompt."""
    from toolsmith.inference import ToolSmithModel

    model = ToolSmithModel.from_pretrained(adapter)
    result = model.call(prompt)
    console.print_json(json.dumps(result))


@app.command()
def version() -> None:
    from toolsmith import __version__

    console.print(f"toolsmith {__version__}")


if __name__ == "__main__":
    app()
