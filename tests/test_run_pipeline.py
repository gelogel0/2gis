from __future__ import annotations

from pathlib import Path
import unittest
from unittest.mock import patch

from src.pipeline.orchestrator import build_steps, run_plan


class PipelineBuildStepTests(unittest.TestCase):
    def test_build_steps_all_enabled(self):
        steps = build_steps(
            city="Алматы",
            category="салон красоты",
            scrape_limit=10,
            enrich_limit=20,
            offers_limit=30,
            send_limit=40,
            output=Path("data/send_page.html"),
            skip_scrape=False,
            skip_enrich=False,
            skip_offers=False,
            skip_send_page=False,
        )
        self.assertEqual(len(steps), 4)
        self.assertIn("scripts/1_scrape_2gis.py", steps[0])
        self.assertIn("scripts/4_build_send_page.py", steps[3])

    def test_build_steps_with_skips(self):
        steps = build_steps(
            city="Алматы",
            category="салон красоты",
            scrape_limit=10,
            enrich_limit=20,
            offers_limit=30,
            send_limit=40,
            output=Path("data/send_page.html"),
            skip_scrape=True,
            skip_enrich=False,
            skip_offers=True,
            skip_send_page=False,
        )
        self.assertEqual(len(steps), 2)
        self.assertIn("scripts/2_enrich_instagram.py", steps[0])
        self.assertIn("scripts/4_build_send_page.py", steps[1])

    @patch("src.pipeline.orchestrator.subprocess.run")
    def test_run_plan_continue_on_error(self, run_mock):
        import subprocess

        run_mock.side_effect = [
            subprocess.CalledProcessError(returncode=1, cmd=["bad"]),
            None,
        ]
        run_plan(
            [["bad"], ["good"]],
            project_root=Path("."),
            continue_on_error=True,
        )
        self.assertEqual(run_mock.call_count, 2)


if __name__ == "__main__":
    unittest.main()
