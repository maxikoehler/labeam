"""HTML builder for the presenter/host view."""

from __future__ import annotations

from ._presenter_templates import _PRESENTER_CSS
from ._presenter_templates import _PRESENTER_JS
from ._presenter_templates import _PRESENTER_TEMPLATE


def build_presenter_html(total: int, ws_port: int, theme: str = "light") -> str:
    """Build the presenter view HTML.

    Parameters
    ----------
    total : int
        Total number of slides.
    ws_port : int
        Port the WebSocket server is listening on.
    theme : str
        Initial colour theme — ``"light"`` (default) or ``"dark"``.

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

    js = _PRESENTER_JS.replace("{ws_port}", str(ws_port)).replace("{total}", str(total))

    return _PRESENTER_TEMPLATE.format(
        css=_PRESENTER_CSS,
        total=total,
        theme=theme,
        js=js,
    )
