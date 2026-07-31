from app.preview import render_markdown


def test_render_markdown_supports_tables() -> None:
    html = render_markdown("| A | B |\n| - | - |\n| 1 | 2 |")
    assert "<table>" in html
    assert "<td>1</td>" in html


def test_render_markdown_strips_active_content() -> None:
    html = render_markdown('[x](javascript:alert(1))\n\n<script>alert(1)</script>')
    assert 'href="javascript:' not in html
    assert "<script" not in html
    assert "&lt;script&gt;" in html
