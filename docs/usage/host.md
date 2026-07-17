# Host

`labeam host` starts a **local presenter server** for a PDF presentation.
It opens two browser tabs automatically — an audience view and a presenter view — and keeps both synchronised in real time via WebSocket.

## Basic usage

```shell
labeam host presentation.pdf
```

The server runs until you press `Ctrl+C`.

## Options

| Option | Default | Description |
|---|---|---|
| `PDF_PATH` | *(required)* | Path to the source PDF file |
| `--port` | `8765` | HTTP server port (audience + presenter views) |
| `--ws-port` | `8766` | WebSocket server port (real-time sync) |
| `--no-browser` | *(flag)* | Do not open browser tabs automatically |

## Examples

**Default — opens both tabs automatically:**

```shell
labeam host slides.pdf
```

**Custom ports (e.g. if defaults are in use):**

```shell
labeam host slides.pdf --port 9000 --ws-port 9001
```

**Start without opening a browser (e.g. for a headless setup):**

```shell
labeam host slides.pdf --no-browser
```

Then open the views manually:

- Audience view: `http://localhost:8765/`
- Presenter view: `http://localhost:8765/presenter`

## The two views

### Audience view (`/`)

A full-screen, distraction-free view intended for the projected display or a second screen.
It shows the current slide and a laser-pointer dot whenever the presenter activates one.

### Presenter view (`/presenter`)

A control panel intended for the presenter's own screen. It contains:

| Element | Description |
|---|---|
| **Current slide** | Live preview of the active slide |
| **Next slide** | Preview of the upcoming slide |
| **Navigation controls** | Previous / Next buttons plus a slide counter |
| **Notes area** | Per-slide text field for speaker notes |
| **Timer / clock** | Elapsed presentation time and current wall-clock time |
| **Dark-mode toggle** | Switches both views simultaneously |

## Features

### Real-time synchronisation

The presenter view and audience view share a WebSocket connection.
Navigating slides in the presenter view instantly updates the audience view.

### Speaker notes

Each slide has an editable text field in the presenter view.
Notes are **automatically saved** to a JSON file next to the PDF
(e.g. `slides.notes.json`) whenever they change, so they persist across sessions.

### Laser pointer

Click and hold anywhere on the current-slide preview in the presenter view to project a laser-pointer dot.
The dot appears in the audience view at the same relative position.

### Dark mode

The dark-mode toggle in the presenter view synchronises the colour scheme across both views simultaneously.

## Notes file location

Slide notes are stored as a JSON file in the same directory as the source PDF, named `<pdf_stem>.notes.json`.
The file is created automatically on first save and is human-readable.

```
slides.pdf          ← source
slides.notes.json   ← notes (auto-created)
```
