from __future__ import annotations

import shlex
import subprocess
import sys
from pathlib import Path


def build_steps(
    *,
    city: str,
    category: str,
    scrape_limit: int,
    enrich_limit: int,
    offers_limit: int,
    send_limit: int,
    output: Path,
    skip_scrape: bool,
    skip_enrich: bool,
    skip_offers: bool,
    skip_send_page: bool,
) -> list[list[str]]:
    steps: list[list[str]] = []
    if not skip_scrape:
        steps.append(
            [
                sys.executable,
                "scripts/1_scrape_2gis.py",
                "--city",
                city,
                "--category",
                category,
                "--limit",
                str(scrape_limit),
            ]
        )
    if not skip_enrich:
        steps.append(
            [sys.executable, "scripts/2_enrich_instagram.py", "--limit", str(enrich_limit)]
        )
    if not skip_offers:
        steps.append(
            [sys.executable, "scripts/3_generate_offers.py", "--limit", str(offers_limit)]
        )
    if not skip_send_page:
        steps.append(
            [
                sys.executable,
                "scripts/4_build_send_page.py",
                "--output",
                str(output),
                "--limit",
                str(send_limit),
            ]
        )
    return steps


def run_step(cmd: list[str], project_root: Path) -> None:
    pretty = " ".join(shlex.quote(x) for x in cmd)
    print(f"→ {pretty}")
    subprocess.run(cmd, check=True, cwd=project_root)


def run_plan(
    steps: list[list[str]],
    *,
    project_root: Path,
    timeout_sec: int | None = None,
    continue_on_error: bool = False,
) -> None:
    for cmd in steps:
        pretty = " ".join(shlex.quote(x) for x in cmd)
        print(f"→ {pretty}")
        try:
            subprocess.run(cmd, check=True, cwd=project_root, timeout=timeout_sec)
        except subprocess.CalledProcessError:
            if continue_on_error:
                print(f"⚠ failed, continue: {pretty}")
                continue
            raise
