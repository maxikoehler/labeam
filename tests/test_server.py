"""Tests for the presenter server and HTML builder."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from labeam._presenter_html import build_presenter_html
from labeam._server import PresenterState
from labeam._server import _make_http_handler
from labeam._server import _port_is_free

_DUMMY_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10">'
    '<rect width="10" height="10"/></svg>'
)


# ---------------------------------------------------------------------------
# PresenterState
# ---------------------------------------------------------------------------


class TestPresenterState:
    def test_raises_on_empty_slides(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="empty"):
            PresenterState([], tmp_path / "notes.json")

    def test_initial_index_is_zero(self, tmp_path: Path) -> None:
        state = PresenterState([_DUMMY_SVG, _DUMMY_SVG], tmp_path / "notes.json")
        assert state.current_index == 0

    def test_goto_clamps_below_zero(self, tmp_path: Path) -> None:
        state = PresenterState([_DUMMY_SVG, _DUMMY_SVG], tmp_path / "notes.json")
        assert state.goto(-5) == 0

    def test_goto_clamps_above_total(self, tmp_path: Path) -> None:
        state = PresenterState([_DUMMY_SVG, _DUMMY_SVG], tmp_path / "notes.json")
        assert state.goto(99) == 1

    def test_goto_valid_index(self, tmp_path: Path) -> None:
        state = PresenterState(
            [_DUMMY_SVG, _DUMMY_SVG, _DUMMY_SVG], tmp_path / "notes.json"
        )
        assert state.goto(2) == 2
        assert state.current_index == 2

    def test_total_equals_slide_count(self, tmp_path: Path) -> None:
        state = PresenterState([_DUMMY_SVG] * 5, tmp_path / "notes.json")
        assert state.total == 5

    # ---- Notes ----

    def test_set_and_get_note(self, tmp_path: Path) -> None:
        notes_file = tmp_path / "notes.json"
        state = PresenterState([_DUMMY_SVG, _DUMMY_SVG], notes_file)
        state.set_note(0, "Hello world")
        assert state.notes["0"] == "Hello world"

    def test_empty_note_removes_key(self, tmp_path: Path) -> None:
        notes_file = tmp_path / "notes.json"
        state = PresenterState([_DUMMY_SVG], notes_file)
        state.set_note(0, "Something")
        state.set_note(0, "")
        assert "0" not in state.notes

    def test_notes_persisted_to_disk(self, tmp_path: Path) -> None:
        notes_file = tmp_path / "notes.json"
        state = PresenterState([_DUMMY_SVG, _DUMMY_SVG], notes_file)
        state.set_note(1, "My note")
        assert notes_file.exists()
        data = json.loads(notes_file.read_text())
        assert data["1"] == "My note"

    def test_notes_loaded_on_init(self, tmp_path: Path) -> None:
        notes_file = tmp_path / "notes.json"
        notes_file.write_text(json.dumps({"0": "Preloaded note"}), encoding="utf-8")
        state = PresenterState([_DUMMY_SVG], notes_file)
        assert state.notes["0"] == "Preloaded note"

    def test_corrupt_notes_file_ignored(self, tmp_path: Path) -> None:
        notes_file = tmp_path / "notes.json"
        notes_file.write_text("not valid json", encoding="utf-8")
        state = PresenterState([_DUMMY_SVG], notes_file)
        assert state.notes == {}

    # ---- Messages ----

    def test_state_message_json(self, tmp_path: Path) -> None:
        state = PresenterState([_DUMMY_SVG, _DUMMY_SVG], tmp_path / "notes.json")
        state.goto(1)
        msg = json.loads(state.state_message())
        assert msg["type"] == "state"
        assert msg["index"] == 1
        assert msg["total"] == 2

    def test_notes_message_json(self, tmp_path: Path) -> None:
        notes_file = tmp_path / "notes.json"
        state = PresenterState([_DUMMY_SVG], notes_file)
        state.set_note(0, "Test")
        msg = json.loads(state.notes_message())
        assert msg["type"] == "notes"
        assert msg["data"]["0"] == "Test"

    def test_dark_mode_default_false(self, tmp_path: Path) -> None:
        state = PresenterState([_DUMMY_SVG], tmp_path / "notes.json")
        assert state.dark_mode is False

    def test_darkmode_message_json(self, tmp_path: Path) -> None:
        state = PresenterState([_DUMMY_SVG], tmp_path / "notes.json")
        msg = json.loads(state.darkmode_message())
        assert msg["type"] == "darkmode"
        assert msg["dark"] is False

    def test_darkmode_message_reflects_state(self, tmp_path: Path) -> None:
        state = PresenterState([_DUMMY_SVG], tmp_path / "notes.json")
        state.dark_mode = True
        msg = json.loads(state.darkmode_message())
        assert msg["dark"] is True


# ---------------------------------------------------------------------------
# HTTP handler (basic smoke test using urllib)
# ---------------------------------------------------------------------------


class TestHTTPHandler:
    def _make_server(self, tmp_path: Path):
        """Return a started HTTPServer on an ephemeral port and its PresenterState."""
        from http.server import HTTPServer

        state = PresenterState([_DUMMY_SVG, _DUMMY_SVG], tmp_path / "notes.json")
        handler = _make_http_handler(
            state, 8766, "<html>audience</html>", "<html>presenter</html>"
        )
        server = HTTPServer(("127.0.0.1", 0), handler)
        return server, state

    @staticmethod
    def _urlopen(url: str):
        """Open *url* directly, bypassing any proxy set in the environment."""
        import urllib.request

        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        return opener.open(url)

    def test_root_returns_200(self, tmp_path: Path) -> None:
        import threading

        server, _ = self._make_server(tmp_path)
        port = server.server_address[1]
        t = threading.Thread(target=server.handle_request)
        t.start()
        response = self._urlopen(f"http://127.0.0.1:{port}/")
        t.join(timeout=2)
        assert response.status == 200
        server.server_close()

    def test_presenter_returns_200(self, tmp_path: Path) -> None:
        import threading

        server, _ = self._make_server(tmp_path)
        port = server.server_address[1]
        t = threading.Thread(target=server.handle_request)
        t.start()
        response = self._urlopen(f"http://127.0.0.1:{port}/presenter")
        t.join(timeout=2)
        assert response.status == 200
        server.server_close()

    def test_slide_endpoint_returns_svg(self, tmp_path: Path) -> None:
        import threading

        server, _ = self._make_server(tmp_path)
        port = server.server_address[1]
        t = threading.Thread(target=server.handle_request)
        t.start()
        response = self._urlopen(f"http://127.0.0.1:{port}/slide/0")
        t.join(timeout=2)
        assert response.status == 200
        assert "svg" in response.headers.get("Content-Type", "")
        server.server_close()

    def test_unknown_path_returns_404(self, tmp_path: Path) -> None:
        import threading
        import urllib.error

        server, _ = self._make_server(tmp_path)
        port = server.server_address[1]
        t = threading.Thread(target=server.handle_request)
        t.start()
        with pytest.raises(urllib.error.HTTPError) as exc_info:
            self._urlopen(f"http://127.0.0.1:{port}/does-not-exist")
        t.join(timeout=2)
        assert exc_info.value.code == 404
        server.server_close()

    def test_slide_out_of_range_returns_404(self, tmp_path: Path) -> None:
        import threading
        import urllib.error

        server, _ = self._make_server(tmp_path)
        port = server.server_address[1]
        t = threading.Thread(target=server.handle_request)
        t.start()
        with pytest.raises(urllib.error.HTTPError) as exc_info:
            self._urlopen(f"http://127.0.0.1:{port}/slide/99")
        t.join(timeout=2)
        assert exc_info.value.code == 404
        server.server_close()


# ---------------------------------------------------------------------------
# Port utilities
# ---------------------------------------------------------------------------


class TestPortIsFree:
    def test_ephemeral_port_is_free(self) -> None:
        import socket

        # Grab an ephemeral port, release it, then check it's "free".
        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]
        assert _port_is_free(port)

    def test_bound_port_is_not_free(self) -> None:
        import socket

        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]
            assert not _port_is_free(port)


# ---------------------------------------------------------------------------
# build_presenter_html
# ---------------------------------------------------------------------------


class TestBuildPresenterHtml:
    def test_raises_on_zero_total(self) -> None:
        with pytest.raises(ValueError, match="total must be at least 1"):
            build_presenter_html(0, 8766)

    def test_returns_string(self) -> None:
        result = build_presenter_html(5, 8766)
        assert isinstance(result, str)

    def test_contains_doctype(self) -> None:
        assert "<!DOCTYPE html>" in build_presenter_html(3, 8766)

    def test_ws_port_injected(self) -> None:
        result = build_presenter_html(3, 9999)
        assert "9999" in result

    def test_total_injected(self) -> None:
        result = build_presenter_html(42, 8766)
        assert "42" in result

    def test_slide_grid_present(self) -> None:
        assert "slideGrid" in build_presenter_html(3, 8766)

    def test_timer_present(self) -> None:
        assert "timer" in build_presenter_html(1, 8766).lower()

    def test_notes_area_present(self) -> None:
        assert "noteArea" in build_presenter_html(1, 8766)

    def test_default_theme_is_light(self) -> None:
        result = build_presenter_html(2, 8766)
        assert 'data-theme="light"' in result

    def test_dark_theme_injected(self) -> None:
        result = build_presenter_html(2, 8766, theme="dark")
        assert 'data-theme="dark"' in result

    def test_theme_btn_present(self) -> None:
        assert "themeBtn" in build_presenter_html(1, 8766)

    def test_next_preview_present(self) -> None:
        assert "nextWrap" in build_presenter_html(2, 8766)

    def test_presenter_laser_element_present(self) -> None:
        assert "presenterLaser" in build_presenter_html(1, 8766)

    def test_goto_prev_goto_next_exposed(self) -> None:
        result = build_presenter_html(3, 8766)
        assert "gotoPrev" in result
        assert "gotoNext" in result
