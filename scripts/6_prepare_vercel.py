"""Prepare static send-page artifact for Vercel deployment."""
from __future__ import annotations

import shutil
from pathlib import Path

import typer

app = typer.Typer(add_completion=False)


@app.command()
def main(
    source: Path = typer.Option(
        Path("data/send_page.html"),
        help="Исходный HTML, обычно результат 4_build_send_page.py",
    ),
    target: Path = typer.Option(
        Path("public/index.html"),
        help="Куда положить файл для Vercel static hosting",
    ),
) -> None:
    if not source.exists():
        raise typer.BadParameter(f"Source file not found: {source}")

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    typer.echo(f"Prepared Vercel artifact: {target.resolve()}")


if __name__ == "__main__":
    app()

