"""Local HTTP + WebSocket server for the presenter/host mode."""

from __future__ import annotations

import asyncio
import contextlib
import json
import os
import socket
import tempfile
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import websockets

from ._config import PresentationConfig
from ._html_builder import build_audience_html
from ._presenter_html import build_presenter_html
from .converter import extract_slides_as_svg
from .converter import extract_toc

# ---------------------------------------------------------------------------
# Shared presenter state
# ---------------------------------------------------------------------------


class PresenterState:
    """Mutable state shared between the HTTP thread and the WebSocket coroutines.

    Parameters
    ----------
    slides : list[str]
        SVG strings for each slide, in order.
    notes_path : Path
        File path for persisting per-slide notes as JSON.
    """

    def __init__(self, slides: list[str], notes_path: Path) -> None:
        if not slides:
            msg = "slides must not be empty"
            raise ValueError(msg)
        self.slides: list[str] = slides
        self.total: int = len(slides)
        self.current_index: int = 0
        self.notes_path: Path = notes_path
        self.notes: dict[str, str] = {}
        self.dark_mode: bool = False
        self._lock = threading.Lock()
        self.load_notes()

    # ---- Index management ------------------------------------------------

    def goto(self, index: int) -> int:
        """Clamp *index* to valid range and update :attr:`current_index`.

        Returns:
        -------
        int
            The new (clamped) index.
        """
        clamped = max(0, min(index, self.total - 1))
        with self._lock:
            self.current_index = clamped
        return clamped

    # ---- Notes I/O -------------------------------------------------------

    def save_notes(self) -> None:
        """Atomically write :attr:`notes` to :attr:`notes_path`.

        Uses write-then-rename to avoid partial writes.
        """
        with self._lock:
            data = json.dumps(self.notes, ensure_ascii=False, indent=2)
        tmp_fd, tmp_name = tempfile.mkstemp(
            dir=self.notes_path.parent,
            prefix=".notes_tmp_",
            suffix=".json",
        )
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as fh:
                fh.write(data)
            Path(tmp_name).replace(self.notes_path)
        except Exception:
            with contextlib.suppress(OSError):
                Path(tmp_name).unlink()
            raise

    def load_notes(self) -> None:
        """Load notes from :attr:`notes_path` if it exists."""
        if not self.notes_path.exists():
            return
        try:
            raw = self.notes_path.read_text(encoding="utf-8")
            loaded = json.loads(raw)
            if isinstance(loaded, dict):
                with self._lock:
                    self.notes = {str(k): str(v) for k, v in loaded.items()}
        except (json.JSONDecodeError, OSError):
            pass

    def set_note(self, index: int, text: str) -> None:
        """Set the note for slide *index* and persist to disk."""
        key = str(index)
        with self._lock:
            if text:
                self.notes[key] = text
            else:
                self.notes.pop(key, None)
        self.save_notes()

    # ---- Serialisation helpers -------------------------------------------

    def state_message(self) -> str:
        """Return a JSON ``state`` message for the current slide."""
        with self._lock:
            idx = self.current_index
        return json.dumps({"type": "state", "index": idx, "total": self.total})

    def notes_message(self) -> str:
        """Return a JSON ``notes`` message with all current notes."""
        with self._lock:
            data = dict(self.notes)
        return json.dumps({"type": "notes", "data": data})

    def darkmode_message(self) -> str:
        """Return a JSON ``darkmode`` message with the current dark-mode state."""
        return json.dumps({"type": "darkmode", "dark": self.dark_mode})


# ---------------------------------------------------------------------------
# HTTP handler
# ---------------------------------------------------------------------------


def _make_http_handler(
    state: PresenterState, _ws_port: int, audience_html: str, presenter_html: str
) -> type:
    """Return a ``BaseHTTPRequestHandler`` subclass bound to *state*.

    Using a factory avoids global variables while still satisfying the
    ``HTTPServer`` constructor which expects an un-instantiated class.
    """

    class _Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            path = urlparse(self.path).path.rstrip("/")

            if path in {"", "/"}:
                self._respond(
                    200, "text/html; charset=utf-8", audience_html.encode("utf-8")
                )
            elif path == "/presenter":
                self._respond(
                    200, "text/html; charset=utf-8", presenter_html.encode("utf-8")
                )
            elif path.startswith("/slide/"):
                self._serve_slide(path)
            else:
                self._respond(404, "text/plain", b"Not found")

        def _serve_slide(self, path: str) -> None:
            try:
                idx = int(path.rsplit("/", maxsplit=1)[-1])
            except ValueError:
                self._respond(404, "text/plain", b"Invalid slide index")
                return
            if idx < 0 or idx >= state.total:
                self._respond(404, "text/plain", b"Slide index out of range")
                return
            body = state.slides[idx].encode("utf-8")
            self._respond(200, "image/svg+xml; charset=utf-8", body)

        def _respond(self, code: int, content_type: str, body: bytes) -> None:
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, fmt: str, *args: object) -> None:
            # Suppress default access log to keep terminal clean.
            pass

    return _Handler


# ---------------------------------------------------------------------------
# WebSocket handler
# ---------------------------------------------------------------------------


async def _ws_handler(
    websocket: Any,
    state: PresenterState,
    clients: set,
) -> None:
    """Handle a single WebSocket connection."""
    clients.add(websocket)
    # Send initial state and notes to the new client.
    try:
        await websocket.send(state.state_message())
        await websocket.send(state.notes_message())
        await websocket.send(state.darkmode_message())
    except websockets.exceptions.ConnectionClosed:
        clients.discard(websocket)
        return

    try:
        async for raw in websocket:
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                continue

            msg_type = msg.get("type")

            if msg_type == "goto":
                new_idx = state.goto(int(msg.get("index", 0)))
                broadcast = json.dumps(
                    {"type": "state", "index": new_idx, "total": state.total}
                )
                await _broadcast(broadcast, clients)

            elif msg_type == "laser":
                broadcast = json.dumps(
                    {
                        "type": "laser",
                        "active": bool(msg.get("active", False)),
                        "x": float(msg.get("x", 0.5)),
                        "y": float(msg.get("y", 0.5)),
                    }
                )
                await _broadcast_except(broadcast, clients, websocket)

            elif msg_type == "darkmode":
                dark = bool(msg.get("dark", False))
                state.dark_mode = dark
                broadcast = json.dumps({"type": "darkmode", "dark": dark})
                await _broadcast_except(broadcast, clients, websocket)

            elif msg_type == "note":
                idx = int(msg.get("index", 0))
                text = str(msg.get("text", ""))
                await asyncio.get_event_loop().run_in_executor(
                    None, state.set_note, idx, text
                )

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        clients.discard(websocket)


async def _broadcast(message: str, clients: set) -> None:
    """Send *message* to all connected clients, ignoring closed sockets."""
    if not clients:
        return
    results = await asyncio.gather(
        *[c.send(message) for c in set(clients)],
        return_exceptions=True,
    )
    for client, result in zip(set(clients), results, strict=False):
        if isinstance(result, Exception):
            clients.discard(client)


async def _broadcast_except(message: str, clients: set, exclude: Any) -> None:
    """Send *message* to all connected clients except *exclude*."""
    targets = [c for c in clients if c is not exclude]
    if not targets:
        return
    results = await asyncio.gather(
        *[c.send(message) for c in targets],
        return_exceptions=True,
    )
    for client, result in zip(targets, results, strict=False):
        if isinstance(result, Exception):
            clients.discard(client)


# ---------------------------------------------------------------------------
# HTML templates for audience and host mode
# ---------------------------------------------------------------------------

_AUDIENCE_HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Presentation</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{
      height: 100%; overflow: hidden;
      background: #111; display: flex;
      align-items: center; justify-content: center;
    }}
    .slide-wrap {{
      width: 100vw; height: 100vh;
      display: flex; align-items: center; justify-content: center;
    }}
    .slide-img {{
      max-width: 100vw; max-height: 100vh;
      width: auto; height: auto;
      object-fit: contain;
      display: block;
    }}
    .laser {{
      position: fixed; pointer-events: none; z-index: 9999;
      width: 26px; height: 26px; border-radius: 50%;
      transform: translate(-50%, -50%);
      background: radial-gradient(circle,
        rgba(255,110,110,1) 0%, rgba(255,40,40,0.95) 26%,
        rgba(255,0,0,0.65) 44%, rgba(255,0,0,0.12) 68%,
        rgba(255,0,0,0) 100%);
      box-shadow: 0 0 0 2px rgba(255,60,60,0.24), 0 0 22px rgba(255,0,0,0.65);
      opacity: 0; transition: opacity 0.15s;
    }}
    .laser.visible {{ opacity: 1; }}
  </style>
</head>
<body>
  <div class="slide-wrap">
    <img class="slide-img" id="slideImg" src="/slide/0" alt="Slide 1">
  </div>
  <div class="laser" id="laserDot"></div>
  <script>
    (function() {{
      var WS_PORT = {ws_port};
      var img = document.getElementById('slideImg');
      var laser = document.getElementById('laserDot');
      var ws, reconnectTimer;

      function connect() {{
        ws = new WebSocket('ws://localhost:' + WS_PORT);
        ws.onmessage = function(e) {{
          var msg = JSON.parse(e.data);
          if (msg.type === 'state') {{
            img.src = '/slide/' + msg.index;
            img.alt = 'Slide ' + (msg.index + 1);
          }} else if (msg.type === 'laser') {{
            if (msg.active) {{
              laser.style.left = (msg.x * 100) + 'vw';
              laser.style.top  = (msg.y * 100) + 'vh';
              laser.classList.add('visible');
            }} else {{
              laser.classList.remove('visible');
            }}
          }}
        }};
        ws.onclose = function() {{
          clearTimeout(reconnectTimer);
          reconnectTimer = setTimeout(connect, 2000);
        }};
      }}
      connect();
    }})();
  </script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Port utilities
# ---------------------------------------------------------------------------


def _port_is_free(port: int) -> bool:
    """Return True if *port* is not currently in use on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind(("127.0.0.1", port))
        except OSError:
            return False
        else:
            return True


# ---------------------------------------------------------------------------
# Main host() entry point
# ---------------------------------------------------------------------------


def host(
    pdf_path: Path,
    port: int = 8765,
    ws_port: int = 8766,
    open_browser: bool = True,
) -> None:
    """Extract slides from *pdf_path* and start the presenter server.

    Blocks until the user presses Ctrl+C.

    Parameters
    ----------
    pdf_path : Path
        Source PDF file.
    port : int
        TCP port for the HTTP server.
    ws_port : int
        TCP port for the WebSocket server.
    open_browser : bool
        Whether to open the audience and presenter tabs automatically.

    Raises:
    ------
    FileNotFoundError
        If *pdf_path* does not exist.
    OSError
        If *port* or *ws_port* is already in use.
    """
    if not pdf_path.exists():
        msg = f"PDF not found: {pdf_path}"
        raise FileNotFoundError(msg)

    for p in (port, ws_port):
        if not _port_is_free(p):
            msg = (
                f"Port {p} is already in use. "
                "Use --port / --ws-port to choose different ports."
            )
            raise OSError(msg)

    print(f"Extracting slides from {pdf_path} …")
    svg_slides = extract_slides_as_svg(pdf_path)
    print(f"  {len(svg_slides)} slides loaded.")

    notes_path = pdf_path.with_suffix(".notes.json")
    state = PresenterState(svg_slides, notes_path)

    toc = extract_toc(pdf_path)
    cfg = PresentationConfig(title=pdf_path.stem.replace("_", " ").replace("-", " "))
    audience_html = build_audience_html(state.total, toc, cfg, ws_port)
    presenter_html = build_presenter_html(state.total, ws_port, theme=cfg.theme)

    handler_class = _make_http_handler(state, ws_port, audience_html, presenter_html)
    http_server = HTTPServer(("127.0.0.1", port), handler_class)

    http_thread = threading.Thread(target=http_server.serve_forever, daemon=True)
    http_thread.start()

    print(f"\nAudience view : http://localhost:{port}/")
    print(f"Presenter view: http://localhost:{port}/presenter")
    print(f"WebSocket     : ws://localhost:{ws_port}")
    print("\nPress Ctrl+C to stop.\n")

    if open_browser:
        # Small delay so the HTTP server is ready before the browser connects.
        threading.Timer(
            0.5, lambda: webbrowser.open(f"http://localhost:{port}/presenter")
        ).start()
        threading.Timer(
            0.9, lambda: webbrowser.open(f"http://localhost:{port}/")
        ).start()

    clients: set = set()

    async def _serve() -> None:
        async def _handler(ws: Any) -> None:
            await _ws_handler(ws, state, clients)

        async with websockets.serve(_handler, "127.0.0.1", ws_port):
            await asyncio.Future()  # run forever until cancelled

    try:
        asyncio.run(_serve())
    except KeyboardInterrupt:
        print("\nShutting down …")
    finally:
        http_server.shutdown()
