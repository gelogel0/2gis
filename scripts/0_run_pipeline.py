"""Orchestrator: run full lead pipeline end-to-end with one command."""
from __future__ import annotations

import shlex
import subprocess
import sys
from pathlib import Path

import typer

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.pipeline.orchestrator import build_steps, run_plan

ROOT = Path(__file__).resolve().parent
app = typer.Typer(add_completion=False)


@app.command()
def main(
    city: str = typer.Option("Алматы", help="Город для поиска в 2GIS"),
    category: str = typer.Option("салон красоты", help="Категория в 2GIS"),
    scrape_limit: int = typer.Option(100, help="Лимит для скрейпа"),
    enrich_limit: int = typer.Option(100, help="Лимит для enrichment"),
    offers_limit: int = typer.Option(100, help="Лимит для генерации офферов"),
    send_limit: int = typer.Option(500, help="Лимит лидов в send-page"),
    output: Path = typer.Option(
        Path("data/send_page.html"), help="Куда сохранить send-page HTML"
    ),
    skip_scrape: bool = typer.Option(False, help="Пропустить 1_scrape_2gis.py"),
    skip_enrich: bool = typer.Option(False, help="Пропустить 2_enrich_instagram.py"),
    skip_offers: bool = typer.Option(False, help="Пропустить 3_generate_offers.py"),
    skip_send_page: bool = typer.Option(False, help="Пропустить 4_build_send_page.py"),
    dry_run: bool = typer.Option(False, help="Только показать команды, не запускать"),
    timeout_sec: int = typer.Option(0, help="Таймаут шага в секундах (0 = без таймаута)"),
    continue_on_error: bool = typer.Option(
        False, help="Продолжать pipeline при ошибке шага"
    ),
) -> None:
    steps = build_steps(
        city=city,
        category=category,
        scrape_limit=scrape_limit,
        enrich_limit=enrich_limit,
        offers_limit=offers_limit,
        send_limit=send_limit,
        output=output,
        skip_scrape=skip_scrape,
        skip_enrich=skip_enrich,
        skip_offers=skip_offers,
        skip_send_page=skip_send_page,
    )
    if dry_run:
        typer.secho("Dry-run pipeline plan:", fg=typer.colors.YELLOW)
        for cmd in steps:
            typer.echo("  " + " ".join(shlex.quote(x) for x in cmd))
        raise typer.Exit(code=0)

    try:
        run_plan(
            steps,
            project_root=ROOT.parent,
            timeout_sec=timeout_sec if timeout_sec > 0 else None,
            continue_on_error=continue_on_error,
        )
    except subprocess.CalledProcessError as exc:
        typer.secho(
            f"Pipeline stopped: command failed with exit code {exc.returncode}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=exc.returncode) from exc

    typer.secho("Pipeline completed successfully.", fg=typer.colors.GREEN)
    if not skip_send_page:
        typer.echo(f"Open: file://{output.resolve()}")


if __name__ == "__main__":
    app()
