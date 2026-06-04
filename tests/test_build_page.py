from __future__ import annotations
import unittest
import importlib.util
from pathlib import Path
import sys

class TestBuildPage(unittest.TestCase):
    def test_html_template_substitution(self):
        # Load the module without executing its main()
        spec = importlib.util.spec_from_file_location("build_page", "scripts/4_build_send_page.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        template = module.HTML_TEMPLATE

        # Simulate the replacement logic in main()
        html = (
            template
            .replace("{count}", "10")
            .replace("{rows}", "<tr></tr>")
            .replace("{supabase_url}", "https://url")
            .replace("{supabase_anon_key}", "key")
        )

        # Verify that placeholders are replaced
        self.assertIn("Send Queue (10 лидов)", html)
        self.assertIn("https://url", html)
        self.assertIn("key", html)

        # Verify that we don't have doubled braces in the output HTML
        # Doubled braces in JS (e.g. function() {{ ... }}) are syntax errors
        self.assertNotIn("{{", html)
        self.assertNotIn("}}", html)

        # Verify that we have single braces for JS blocks
        self.assertIn("function updateStats() {", html)
        self.assertIn("rows.forEach(r => {", html)

if __name__ == "__main__":
    unittest.main()
