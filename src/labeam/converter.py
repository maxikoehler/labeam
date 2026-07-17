"""PDF extraction utilities for HTML presentation generation."""

from __future__ import annotations

from pathlib import Path

import fitz  # PyMuPDF


def extract_slides_as_svg(pdf_path: str | Path) -> list[str]:
    """Extract every page of a PDF as an SVG string.

    Each returned string is a complete ``<svg …>…</svg>`` document that can be
    embedded inline inside an HTML file or encoded as a data-URI.

    Parameters
    ----------
    pdf_path : str or Path
        Path to the source PDF file.

    Returns:
    -------
    list[str]
        One SVG string per PDF page, in page order.

    Raises:
    ------
    FileNotFoundError
        If *pdf_path* does not exist.
    ValueError
        If the PDF contains no pages.
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        msg = f"PDF not found: {pdf_path}"
        raise FileNotFoundError(msg)

    doc: fitz.Document = fitz.open(str(pdf_path))

    if len(doc) == 0:
        msg = f"PDF contains no pages: {pdf_path}"
        raise ValueError(msg)

    svgs: list[str] = []
    for page in doc:
        svg_text: str = page.get_svg_image(matrix=fitz.Identity)
        svgs.append(svg_text)

    doc.close()
    return svgs


def extract_toc(pdf_path: str | Path) -> list[tuple[int, str]]:
    """Extract the table of contents from a PDF.

    Reads the PDF outline (bookmarks). When no outline is present an empty list
    is returned; the caller is responsible for generating fallback labels such
    as ``"Slide N"``.

    Parameters
    ----------
    pdf_path : str or Path
        Path to the source PDF file.

    Returns:
    -------
    list[tuple[int, str]]
        A list of ``(page_index, title)`` tuples (0-based page index).
        Only top-level entries are included.

    Raises:
    ------
    FileNotFoundError
        If *pdf_path* does not exist.
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        msg = f"PDF not found: {pdf_path}"
        raise FileNotFoundError(msg)

    doc: fitz.Document = fitz.open(str(pdf_path))
    # get_toc() returns [[level, title, page_1based, …], …]
    raw_toc = doc.get_toc(simple=True)
    doc.close()

    # Keep only top-level entries (level == 1) and convert to 0-based index.
    return [(entry[2] - 1, entry[1]) for entry in raw_toc if entry[0] == 1]
