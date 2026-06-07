
import unittest
import importlib.util
from pathlib import Path

class BuildPageTests(unittest.TestCase):
    def test_html_template_substitution(self):
        # Import HTML_TEMPLATE from scripts/4_build_send_page.py
        spec = importlib.util.spec_from_file_location("build_page", "scripts/4_build_send_page.py")
        build_page = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(build_page)

        template = build_page.HTML_TEMPLATE

        # Original code used .replace() for substitution
        # If the template had {{ }}, the final output would have {{ }} because .replace()
        # doesn't handle brace escaping.

        # Simulate the substitution
        html = (
            template
            .replace("{count}", "10")
            .replace("{rows}", "<tr></tr>")
            .replace("{supabase_url}", "https://test.supabase.co")
            .replace("{supabase_anon_key}", "test-key")
        )

        # If there are doubled braces in the output, it means the template was wrong for .replace()
        self.assertNotIn("{{", html, "Found '{{' in generated HTML. Use single braces in Python template when using .replace()")
        self.assertNotIn("}}", html, "Found '}}' in generated HTML. Use single braces in Python template when using .replace()")

        # Verify specific JS structures are correct
        self.assertIn("function updateStats() {", html)
        self.assertIn("rows.forEach(r => {", html)

if __name__ == "__main__":
    unittest.main()
