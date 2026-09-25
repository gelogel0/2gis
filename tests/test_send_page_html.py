from __future__ import annotations

import importlib
import unittest

from src.ui.send_page import row_html, safe_wa_link


class SendPageHtmlTests(unittest.TestCase):
    def test_row_html_escapes_visible_and_attribute_fields(self):
        lead = {
            "id": '" onmouseover="alert(1)',
            "name": "<b>Bad</b>",
            "category": "<script>x</script>",
            "city": 'Almaty" onclick="x',
            "main_phone": "<img src=x onerror=1>",
            "generated_offer": "<div>offer</div>",
            "wa_link": 'https://wa.me/77000000000?text="x"&a=<b>',
            "template_id": "A",
        }
        row = row_html(1, lead)

        self.assertIn("&lt;b&gt;Bad&lt;/b&gt;", row)
        self.assertIn("&lt;script&gt;x&lt;/script&gt;", row)
        self.assertIn("&lt;img src=x onerror=1&gt;", row)
        self.assertIn("&lt;div&gt;offer&lt;/div&gt;", row)
        self.assertIn("data-id=\"&quot; onmouseover=&quot;alert(1)\"", row)
        self.assertIn("?text=&quot;x&quot;&amp;a=&lt;b&gt;", row)
        self.assertNotIn("<script>x</script>", row)
        self.assertIn('class="send-btn js-send-btn"', row)
        self.assertIn('class="mark-btn js-mark-btn"', row)
        self.assertNotIn("markSent(", row)

    def test_row_html_rejects_non_wa_link_and_unknown_template(self):
        lead = {
            "id": "123",
            "name": "OK",
            "category": "OK",
            "city": "OK",
            "main_phone": "+77000000000",
            "generated_offer": "Offer",
            "wa_link": "javascript:alert(1)",
            "template_id": 'A" onclick="alert(1)',
        }
        row = row_html(2, lead)
        self.assertIn('class="template-?"', row)
        self.assertIn('<span class="tag">no phone</span>', row)
        self.assertNotIn('href="javascript:alert(1)"', row)

    def test_safe_wa_link_strict_validation(self):
        self.assertEqual(
            safe_wa_link("https://wa.me/77000000000?text=hello"),
            "https://wa.me/77000000000?text=hello",
        )
        self.assertEqual(
            safe_wa_link("https://wa.me/77000000000?text=<hi>"),
            "https://wa.me/77000000000?text=&lt;hi&gt;",
        )
        self.assertEqual(safe_wa_link("https://wa.me/"), "")
        self.assertEqual(safe_wa_link("http://wa.me/7700"), "")
        self.assertEqual(safe_wa_link("https://evil.com/7700"), "")
        self.assertEqual(safe_wa_link("https://wa.me/not-a-phone"), "")
        self.assertEqual(safe_wa_link("https://user:pass@wa.me/7700"), "")
        self.assertEqual(safe_wa_link("https://wa.me:444/7700"), "")

    def test_html_template_ux_improvements(self):
        mod = importlib.import_module("scripts.4_build_send_page")
        html_template = getattr(mod, "HTML_TEMPLATE")
        self.assertIn('aria-label="Поиск лидов"', html_template)
        self.assertIn(":focus-visible { outline: 2px solid #4ade80; outline-offset: 2px; }", html_template)
        self.assertIn(".mark-btn:disabled { opacity: 0.5; cursor: not-allowed; }", html_template)
        self.assertIn('id="no-results-row"', html_template)
        self.assertIn("Лиды не найдены", html_template)


if __name__ == "__main__":
    unittest.main()
