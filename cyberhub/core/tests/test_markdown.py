from django.test import SimpleTestCase
from django.utils.safestring import SafeString

from core.markdown import render_markdown


class MarkdownFormattingTests(SimpleTestCase):
    def test_returns_safe_string(self):
        self.assertIsInstance(render_markdown("text"), SafeString)

    def test_heading_and_bold(self):
        html = render_markdown("# Title\n\n**bold**")
        self.assertIn("<h1>Title</h1>", html)
        self.assertIn("<strong>bold</strong>", html)

    def test_lists(self):
        self.assertIn("<li>one</li>", render_markdown("- one\n- two"))

    def test_code_block_escapes_its_content(self):
        html = render_markdown("```\n<script>alert(1)</script>\n```")
        self.assertIn("<pre><code>", html)
        self.assertIn("&lt;script&gt;", html)

    def test_table_with_alignment(self):
        html = render_markdown("| A | B |\n|---|--:|\n| 1 | 2 |")
        self.assertIn("<table>", html)
        self.assertIn("text-align:right", html.replace(" ", ""))

    def test_strikethrough(self):
        self.assertIn("<s>old</s>", render_markdown("~~old~~"))

    def test_single_line_break_is_kept(self):
        self.assertIn("<br", render_markdown("one\ntwo"))

    def test_link_gets_safe_rel(self):
        html = render_markdown("[site](https://example.com)")
        self.assertIn('href="https://example.com"', html)
        self.assertIn('rel="noopener noreferrer"', html)


class MarkdownSecurityTests(SimpleTestCase):
    def test_raw_script_is_shown_as_text(self):
        html = render_markdown("<script>alert(1)</script>")
        self.assertNotIn("<script", html)
        self.assertIn("&lt;script&gt;", html)

    def test_event_handler_html_is_not_active(self):
        self.assertNotIn("<img", render_markdown("<img src=x onerror=alert(1)>"))

    def test_dangerous_link_schemes_are_not_links(self):
        for url in ("javascript:alert(1)", "JaVaScRiPt:alert(1)", "data:text/html,<script>alert(1)</script>", "vbscript:msgbox(1)"):
            with self.subTest(url=url):
                self.assertNotIn("href=", render_markdown(f"[click]({url})"))

    def test_iframe_and_style_are_not_active(self):
        html = render_markdown("<iframe src='https://example.com'></iframe>\n\n<style>body{display:none}</style>")
        self.assertNotIn("<iframe", html)
        self.assertNotIn("<style", html)

    def test_markdown_image_is_not_rendered(self):
        self.assertNotIn("<img", render_markdown("![tracker](https://example.com/pixel.png)"))
