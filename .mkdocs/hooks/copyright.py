"""Generate a copyright year range."""

from __future__ import annotations

import re
from datetime import datetime
from typing import TYPE_CHECKING
from zoneinfo import ZoneInfo

if TYPE_CHECKING:
    from mkdocs.config.defaults import MkDocsConfig


_COPYRIGHT_YEAR_REGEX = re.compile(r"(\d{4})")


def on_config(config: MkDocsConfig) -> MkDocsConfig | None:
    """Update the copyright field to show a year range if applicable."""
    if (
        config.copyright
        and (match := _COPYRIGHT_YEAR_REGEX.search(config.copyright))
        and (match.group() != (year := str(datetime.now(ZoneInfo("UTC")).year)))
    ):
        config.copyright = _COPYRIGHT_YEAR_REGEX.sub(rf"\1 - {year}", config.copyright)
    return config
