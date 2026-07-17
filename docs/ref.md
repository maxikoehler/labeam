# Reference

This page documents the public Python API of the `labeam` package.
All functions and classes listed here are stable and suitable for use in your own scripts.

---

## PDF extraction — `converter`

Core utilities for reading a PDF and extracting its content as SVG slides and a table of contents.

::: src.labeam.converter.extract_slides_as_svg

::: src.labeam.converter.extract_toc

---

## Configuration — `_config`

Dataclass that carries all metadata and theme settings passed to the HTML builders.

::: src.labeam._config.PresentationConfig

---

## HTML builder — `_html_builder`

Assembles self-contained HTML presentations from SVG slides and a `PresentationConfig`.

::: src.labeam._html_builder.build_html

::: src.labeam._html_builder.build_audience_html

---

## Presenter view — `_presenter_html`

Builds the presenter control-panel page used by `labeam host`.

::: src.labeam._presenter_html.build_presenter_html

---

## Presenter state — `_server`

Shared mutable state that the HTTP thread and WebSocket coroutines operate on during a live hosting session.

::: src.labeam._server.PresenterState
