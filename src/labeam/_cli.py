"""Command line application."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

from typer import Argument
from typer import Exit
from typer import Option
from typer import Typer
from typer import echo

from ._config import PresentationConfig
from ._html_builder import build_html
from ._server import host
from .converter import extract_slides_as_svg
from .converter import extract_toc

app = Typer(rich_markup_mode=None)


@app.callback()
def _main() -> None: ...


@app.command("convert")
def _convert(
    pdf_path: Annotated[Path, Argument(help="Path to the source PDF file")],
    output: Annotated[
        Path | None,
        Option("--output", "-o", help="Output HTML file (default: <pdf_stem>.html)"),
    ] = None,
    title: Annotated[
        str | None,
        Option("--title", help="Presentation title"),
    ] = None,
    author: Annotated[
        str,
        Option("--author", help="Author name shown in slide footers"),
    ] = "",
    date: Annotated[
        str,
        Option("--date", help='Date string shown in footers (e.g. "July 2026")'),
    ] = "",
    department: Annotated[
        str,
        Option("--department", help="Department or team name"),
    ] = "",
    classification: Annotated[
        str,
        Option("--classification", help="Document classification label"),
    ] = "",
    theme: Annotated[
        str,
        Option("--theme", help="Initial colour theme: light or dark"),
    ] = "light",
) -> None:
    """Convert a PDF presentation to a self-contained HTML file."""
    if not pdf_path.exists():
        echo(f"Error: PDF not found: {pdf_path}", err=True)
        raise Exit(1)

    if theme not in {"light", "dark"}:
        echo("Error: --theme must be 'light' or 'dark'", err=True)
        raise Exit(1)

    resolved_output: Path = output or pdf_path.with_suffix(".html")
    resolved_title: str = title or pdf_path.stem.replace("_", " ").replace("-", " ")

    echo(f"Extracting slides from {pdf_path} …")
    try:
        svg_slides = extract_slides_as_svg(pdf_path)
    except (FileNotFoundError, ValueError) as exc:
        echo(f"Error: {exc}", err=True)
        raise Exit(1) from exc

    toc = extract_toc(pdf_path)

    config = PresentationConfig(
        title=resolved_title,
        author=author,
        date=date,
        department=department,
        classification=classification,
        theme=theme,  # type: ignore[arg-type]
    )

    echo(f"Building HTML ({len(svg_slides)} slides) …")
    html = build_html(svg_slides, toc, config)

    resolved_output.write_text(html, encoding="utf-8")
    echo(f"Saved: {resolved_output}")


@app.command("host")
def _host(
    pdf_path: Annotated[Path, Argument(help="Path to the source PDF file")],
    port: Annotated[
        int,
        Option("--port", help="HTTP server port"),
    ] = 8765,
    ws_port: Annotated[
        int,
        Option("--ws-port", help="WebSocket server port"),
    ] = 8766,
    no_browser: Annotated[
        bool,
        Option("--no-browser", help="Do not open browser windows automatically"),
    ] = False,
) -> None:
    """Start a local presenter server for a PDF presentation.

    Opens two browser tabs: the audience view (/) and the presenter
    view (/presenter).  Both are synchronised in real time via WebSocket.
    Press Ctrl+C to stop the server.
    """
    if not pdf_path.exists():
        echo(f"Error: PDF not found: {pdf_path}", err=True)
        raise Exit(1)

    try:
        host(
            pdf_path=pdf_path,
            port=port,
            ws_port=ws_port,
            open_browser=not no_browser,
        )
    except (FileNotFoundError, ValueError, OSError) as exc:
        echo(f"Error: {exc}", err=True)
        raise Exit(1) from exc
