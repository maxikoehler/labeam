"""HTML presentation builder.

Assembles a self-contained HTML file from a list of SVG slide strings and a
:class:`~labeam._config.PresentationConfig`.
"""

from __future__ import annotations

import base64
import html as _html_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._config import PresentationConfig

from ._html_builder_templates import _CSS
from ._html_builder_templates import _HTML_TEMPLATE
from ._html_builder_templates import _JS
from ._html_builder_templates import _WS_AUDIENCE_JS

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_html(
    svg_slides: list[str],
    toc: list[tuple[int, str]],
    config: PresentationConfig,
) -> str:
    """Assemble a self-contained HTML presentation string.

    Parameters
    ----------
    svg_slides : list[str]
        One SVG string per slide, as returned by
        :func:`~labeam.converter.extract_slides_as_svg`.
    toc : list[tuple[int, str]]
        ``(page_index, title)`` pairs (0-based) for the TOC overlay.
        Pass an empty list to fall back to ``"Slide N"`` labels.
    config : PresentationConfig
        Metadata and theme settings.

    Returns:
    -------
    str
        Complete HTML document as a string.

    Raises:
    ------
    ValueError
        If *svg_slides* is empty.
    """
    if not svg_slides:
        msg = "svg_slides must not be empty"
        raise ValueError(msg)

    slides_html = _build_slides_html(svg_slides)
    toc_js = _toc_to_js(toc)

    return _HTML_TEMPLATE.format(
        theme=config.theme,
        title_escaped=_html_module.escape(config.title),
        title_js=_js_string(config.title),
        classification_js=_js_string(config.classification),
        year_js=_js_string(""),  # filled from config if needed
        author_js=_js_string(config.author),
        department_js=_js_string(config.department),
        date_js=_js_string(config.date),
        toc_js=toc_js,
        css=_CSS,
        slides_html=slides_html,
        js=_JS,
    )


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _svg_to_data_uri(svg_text: str) -> str:
    """Encode an SVG string as a base64 data-URI."""
    encoded = base64.b64encode(svg_text.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def _build_slides_html(svg_slides: list[str]) -> str:
    """Render all slides as ``<section class="slide …">`` elements."""
    parts: list[str] = []
    for i, svg in enumerate(svg_slides):
        active_class = " active" if i == 0 else ""
        data_uri = _svg_to_data_uri(svg)
        parts.append(
            f'    <section class="slide{active_class}" data-index="{i}">\n'
            f'      <img class="slide-svg" src="{data_uri}" alt="Slide {i + 1}">\n'
            f"    </section>"
        )
    return "\n".join(parts)


def _js_string(value: str) -> str:
    """Format a Python string as a JSON/JS string literal."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _toc_to_js(toc: list[tuple[int, str]]) -> str:
    """Serialise the TOC list to a JavaScript array literal."""
    if not toc:
        return "[]"
    entries = ", ".join(
        f'[{page_idx}, "{title.replace(chr(34), chr(92) + chr(34))}"]'
        for page_idx, title in toc
    )
    return f"[{entries}]"


# ---------------------------------------------------------------------------
# Public API — hosted (URL-based slides, WebSocket-controlled audience view)
# ---------------------------------------------------------------------------

# Uses WS_PORT_PLACEHOLDER instead of a format spec to avoid conflicts with
# JavaScript curly-brace syntax when the string is later processed.


def _make_ws_audience_js(ws_port: int) -> str:
    """Return the audience WebSocket client JS with *ws_port* substituted."""
    return _WS_AUDIENCE_JS.replace("WS_PORT_PLACEHOLDER", str(ws_port))


def _build_slides_html_by_url(total: int) -> str:
    """Build ``<section class="slide …">`` elements referencing ``/slide/{i}`` URLs."""
    parts: list[str] = []
    for i in range(total):
        active_class = " active" if i == 0 else ""
        parts.append(
            f'    <section class="slide{active_class}" data-index="{i}">\n'
            f'      <img class="slide-svg" src="/slide/{i}" alt="Slide {i + 1}">\n'
            f"    </section>"
        )
    return "\n".join(parts)


def build_audience_html(
    total: int,
    toc: list[tuple[int, str]],
    config: PresentationConfig,
    ws_port: int,
) -> str:
    """Build the audience HTML for the host/presenter mode.

    Like :func:`build_html` but slides reference ``/slide/N`` HTTP endpoints
    and a WebSocket client syncs navigation and laser-pointer state from the
    presenter view in real time.

    Parameters
    ----------
    total : int
        Total number of slides.
    toc : list[tuple[int, str]]
        ``(page_index, title)`` pairs for the TOC overlay.
    config : PresentationConfig
        Metadata and theme settings.
    ws_port : int
        Port the WebSocket server is listening on.

    Returns:
    -------
    str
        Complete HTML document string.

    Raises:
    ------
    ValueError
        If *total* is less than 1.
    """
    if total < 1:
        msg = "total must be at least 1"
        raise ValueError(msg)

    slides_html = _build_slides_html_by_url(total)
    toc_js = _toc_to_js(toc)
    ws_js = _make_ws_audience_js(ws_port)

    return _HTML_TEMPLATE.format(
        theme=config.theme,
        title_escaped=_html_module.escape(config.title),
        title_js=_js_string(config.title),
        classification_js=_js_string(config.classification),
        year_js=_js_string(""),
        author_js=_js_string(config.author),
        department_js=_js_string(config.department),
        date_js=_js_string(config.date),
        toc_js=toc_js,
        css=_CSS,
        slides_html=slides_html,
        js=_JS + "\n" + ws_js,
    )
