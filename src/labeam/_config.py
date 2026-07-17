"""Configuration dataclass for HTML presentation generation."""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Literal


@dataclass
class PresentationConfig:
    """Configuration for a generated HTML presentation.

    Parameters
    ----------
    title : str
        The presentation title shown in the browser tab and title slide.
    author : str
        Author name shown in slide footers.
    date : str
        Date string shown in slide footers (e.g. ``"July 2026"``).
    department : str
        Department or team name shown in slide footers.
    classification : str
        Document classification label (e.g. ``"Public"``).
    theme : Literal["light", "dark"]
        Initial colour theme. Defaults to ``"light"``.
    """

    title: str = "Presentation"
    author: str = ""
    date: str = ""
    department: str = ""
    classification: str = ""
    theme: Literal["light", "dark"] = "light"
    _extra: dict[str, str] = field(default_factory=dict, repr=False)
