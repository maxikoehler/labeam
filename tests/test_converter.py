"""Tests for converter and HTML builder."""

from __future__ import annotations

from pathlib import Path

import pytest

from labeam._config import PresentationConfig
from labeam._html_builder import _js_string
from labeam._html_builder import _toc_to_js
from labeam._html_builder import build_audience_html
from labeam._html_builder import build_html
from labeam.converter import extract_toc

# ---------------------------------------------------------------------------
# Helpers — create a minimal valid PDF in memory (no external deps)
# ---------------------------------------------------------------------------


def _make_minimal_pdf(n_pages: int = 2) -> bytes:
    """Return the bytes of a minimal valid PDF with *n_pages* blank pages."""
    objects: list[bytes] = []

    def obj(n: int, body: str) -> bytes:
        return f"{n} 0 obj\n{body}\nendobj\n".encode()

    # Object 1: Catalog
    # Object 2: Pages root  (filled later)
    # Object 3+: Page objects

    page_refs = " ".join(f"{3 + i} 0 R" for i in range(n_pages))

    objects.append(obj(1, "<< /Type /Catalog /Pages 2 0 R >>"))
    objects.append(obj(2, f"<< /Type /Pages /Kids [{page_refs}] /Count {n_pages} >>"))

    objects.extend(
        obj(
            3 + i,
            "<< /Type /Page /Parent 2 0 R "
            "/MediaBox [0 0 792 612] "
            "/Resources << >> "
            f"/Contents {3 + n_pages + i} 0 R >>",
        )
        for i in range(n_pages)
    )

    for i in range(n_pages):
        stream_data = b"q Q"
        objects.append(
            obj(
                3 + n_pages + i,
                f"<< /Length {len(stream_data)} >>\nstream\n".encode().decode()
                + stream_data.decode()
                + "\nendstream",
            )
        )

    header = b"%PDF-1.4\n"
    body = b"".join(objects)

    # Cross-reference table
    xref_offset = len(header) + len(body)
    offsets: list[int] = []
    pos = len(header)
    for o in objects:
        offsets.append(pos)
        pos += len(o)

    n_obj = len(objects) + 1  # +1 for free entry 0
    xref_lines = [f"xref\n0 {n_obj}\n", "0000000000 65535 f \n"]
    xref_lines.extend(f"{off:010d} 00000 n \n" for off in offsets)
    xref = "".join(xref_lines).encode()

    trailer = (
        f"trailer\n<< /Size {n_obj} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n"
    ).encode()

    return header + body + xref + trailer


# ---------------------------------------------------------------------------
# converter.extract_toc
# ---------------------------------------------------------------------------


class TestExtractToc:
    def test_missing_file_raises(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            extract_toc(tmp_path / "missing.pdf")

    def test_pdf_without_outline_returns_empty(self, tmp_path: Path) -> None:
        pdf = tmp_path / "blank.pdf"
        pdf.write_bytes(_make_minimal_pdf(2))
        result = extract_toc(pdf)
        assert result == []

    def test_returns_list_of_tuples(self, tmp_path: Path) -> None:
        pdf = tmp_path / "blank.pdf"
        pdf.write_bytes(_make_minimal_pdf(1))
        result = extract_toc(pdf)
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, tuple)
            assert len(item) == 2
            assert isinstance(item[0], int)
            assert isinstance(item[1], str)


# ---------------------------------------------------------------------------
# _html_builder helpers
# ---------------------------------------------------------------------------


class TestJsString:
    def test_plain_string(self) -> None:
        assert _js_string("hello") == '"hello"'

    def test_escapes_double_quote(self) -> None:
        assert _js_string('say "hi"') == '"say \\"hi\\""'

    def test_escapes_backslash(self) -> None:
        assert _js_string("a\\b") == '"a\\\\b"'

    def test_empty_string(self) -> None:
        assert _js_string("") == '""'


class TestTocToJs:
    def test_empty(self) -> None:
        assert _toc_to_js([]) == "[]"

    def test_single_entry(self) -> None:
        result = _toc_to_js([(0, "Intro")])
        assert result == '[[0, "Intro"]]'

    def test_multiple_entries(self) -> None:
        result = _toc_to_js([(0, "Intro"), (2, "Chapter 1")])
        assert "0" in result
        assert "Intro" in result
        assert "2" in result
        assert "Chapter 1" in result


# ---------------------------------------------------------------------------
# build_html
# ---------------------------------------------------------------------------

_DUMMY_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10">'
    '<rect width="10" height="10"/></svg>'
)


class TestBuildHtml:
    def test_raises_on_empty_slides(self) -> None:
        cfg = PresentationConfig()
        with pytest.raises(ValueError, match="empty"):
            build_html([], [], cfg)

    def test_returns_string(self) -> None:
        cfg = PresentationConfig(title="Test")
        result = build_html([_DUMMY_SVG], [], cfg)
        assert isinstance(result, str)

    def test_contains_doctype(self) -> None:
        cfg = PresentationConfig()
        result = build_html([_DUMMY_SVG], [], cfg)
        assert "<!DOCTYPE html>" in result

    def test_title_escaped_in_output(self) -> None:
        cfg = PresentationConfig(title="Hello <World>")
        result = build_html([_DUMMY_SVG], [], cfg)
        assert "&lt;World&gt;" in result

    def test_slide_count_matches(self) -> None:
        cfg = PresentationConfig()
        result = build_html([_DUMMY_SVG, _DUMMY_SVG, _DUMMY_SVG], [], cfg)
        # Count <section class="slide …"> elements only (not slide-svg, slide-counter …)
        assert result.count('<section class="slide') == 3

    def test_first_slide_is_active(self) -> None:
        cfg = PresentationConfig()
        result = build_html([_DUMMY_SVG, _DUMMY_SVG], [], cfg)
        assert 'class="slide active"' in result

    def test_dark_theme_attribute(self) -> None:
        cfg = PresentationConfig(theme="dark")
        result = build_html([_DUMMY_SVG], [], cfg)
        assert 'data-theme="dark"' in result

    def test_light_theme_attribute(self) -> None:
        cfg = PresentationConfig(theme="light")
        result = build_html([_DUMMY_SVG], [], cfg)
        assert 'data-theme="light"' in result

    def test_svg_embedded_as_data_uri(self) -> None:
        cfg = PresentationConfig()
        result = build_html([_DUMMY_SVG], [], cfg)
        assert "data:image/svg+xml;base64," in result

    def test_toc_data_injected(self) -> None:
        cfg = PresentationConfig()
        result = build_html([_DUMMY_SVG], [(0, "My Chapter")], cfg)
        assert "My Chapter" in result

    def test_progress_bar_present(self) -> None:
        cfg = PresentationConfig()
        result = build_html([_DUMMY_SVG], [], cfg)
        assert "progressBar" in result

    def test_laser_pointer_present(self) -> None:
        cfg = PresentationConfig()
        result = build_html([_DUMMY_SVG], [], cfg)
        assert "laserPointer" in result

    def test_toc_overlay_present(self) -> None:
        cfg = PresentationConfig()
        result = build_html([_DUMMY_SVG], [], cfg)
        assert "tocOverlay" in result


# ---------------------------------------------------------------------------
# build_audience_html
# ---------------------------------------------------------------------------


class TestBuildAudienceHtml:
    def test_raises_on_zero_total(self) -> None:
        cfg = PresentationConfig()
        with pytest.raises(ValueError, match="total must be at least 1"):
            build_audience_html(0, [], cfg, 8766)

    def test_returns_string(self) -> None:
        cfg = PresentationConfig(title="Hosted")
        result = build_audience_html(3, [], cfg, 8766)
        assert isinstance(result, str)

    def test_contains_doctype(self) -> None:
        assert "<!DOCTYPE html>" in build_audience_html(
            1, [], PresentationConfig(), 8766
        )

    def test_slides_reference_url_not_base64(self) -> None:
        result = build_audience_html(3, [], PresentationConfig(), 8766)
        assert "/slide/0" in result
        assert "/slide/2" in result
        assert "data:image/svg+xml" not in result

    def test_ws_port_injected(self) -> None:
        result = build_audience_html(2, [], PresentationConfig(), 9999)
        assert "9999" in result

    def test_show_slide_exported(self) -> None:
        result = build_audience_html(2, [], PresentationConfig(), 8766)
        assert "window.showSlide" in result

    def test_ws_audience_js_present(self) -> None:
        result = build_audience_html(2, [], PresentationConfig(), 8766)
        assert "_handleWsLaser" in result

    def test_laser_uses_canvas_coords(self) -> None:
        result = build_audience_html(2, [], PresentationConfig(), 8766)
        # Audience should position laser using the 1920x1080 canvas math
        assert "1920" in result
        assert "1080" in result

    def test_dark_theme(self) -> None:
        cfg = PresentationConfig(theme="dark")
        assert 'data-theme="dark"' in build_audience_html(1, [], cfg, 8766)

    def test_toc_injected(self) -> None:
        result = build_audience_html(3, [(0, "Intro")], PresentationConfig(), 8766)
        assert "Intro" in result

    def test_progress_bar_present(self) -> None:
        assert "progressBar" in build_audience_html(1, [], PresentationConfig(), 8766)

    def test_laser_pointer_element_present(self) -> None:
        assert "laserPointer" in build_audience_html(1, [], PresentationConfig(), 8766)
