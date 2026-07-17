# Functionality

LaBeam provides two complementary workflows for presenting PDF slides.
Both share the same underlying SVG rendering pipeline — every slide is
extracted from the PDF as a scalable vector graphic, so the output is
always pixel-perfect regardless of screen resolution.

---

## `labeam convert` — Standalone HTML file

`labeam convert` packages a PDF into a **single, fully self-contained HTML file**.
The file contains all slides as inline SVG and runs entirely offline in any
modern browser — no server, no internet connection, no additional assets required.

### Advantages

- **Zero dependencies at runtime** — share or archive a single `.html` file.
- **Pixel-perfect scaling** — slides are rendered at 1920 × 1080 and scaled
  to the viewport automatically; no blurry rasterisation.
- **Rich interactivity** — laser pointer, table of contents, dark mode, and
  touch/swipe support built in.
- **Metadata embedding** — author, date, department, and classification are
  written into slide footers at conversion time.

### Keyboard shortcuts

| Key | Action |
|---|---|
| `→` or `Space` | Next slide |
| `←` | Previous slide |
| `Home` | First slide |
| `End` | Last slide |
| `T` | Open / close table of contents |
| `L` | Toggle laser pointer |
| `D` | Toggle dark / light mode |
| `Escape` | Close table of contents or deactivate laser pointer |

### Mouse & touch

| Gesture | Action |
|---|---|
| Click `→` / `←` button | Next / previous slide |
| Swipe left | Next slide |
| Swipe right | Previous slide |
| Click `≡` button | Open table of contents |
| Click `●` button | Toggle laser pointer |
| Click `☾` button | Toggle dark / light mode |

### Table of contents

Press `T` or click `≡` to open a slide-overview panel.
Entries are built from the PDF's bookmark outline.
If the PDF has no outline, every slide is listed by number.
Clicking any entry jumps directly to that slide.

### Laser pointer

Press `L` (or click `●`) to activate the laser pointer.
While active the cursor is hidden and a red dot tracks your mouse position.
Press `L` again or `Escape` to deactivate.

### Progress bar

A thin progress bar runs along the bottom of the slide, growing as you
advance through the presentation.

### Dark / light mode

Press `D` (or click `☾`) to switch between the light and dark colour theme.
The initial theme can be set at conversion time with `--theme dark`.

---

## `labeam host` — Live presenter server

`labeam host` renders the PDF and starts a local HTTP + WebSocket server.
It opens **two browser tabs automatically** — one for the projected display
(audience view) and one for the presenter's own screen (presenter view).
Both views are kept in sync in real time.

### Advantages

- **Dedicated presenter view** with speaker notes, next-slide preview, and
  a presentation timer — all on the presenter's screen only.
- **Real-time synchronisation** — any navigation in the presenter view
  instantly updates the audience display via WebSocket.
- **Persistent speaker notes** — notes are saved automatically to a JSON
  file next to the PDF and reloaded on the next session.
- **Laser pointer sync** — the laser dot from the presenter view is
  broadcast to the audience view in real time.
- **Auto-reconnect** — if the WebSocket connection drops, both views
  reconnect automatically within two seconds.

---

### Audience view (`/`)

Full-screen and distraction-free — intended for the projector or second
screen.

| Element | Description |
|---|---|
| Current slide | Fills the entire viewport |
| Laser dot | Appears whenever the presenter activates the laser |

---

### Presenter view (`/presenter`)

Split-panel control surface — intended for the presenter's laptop screen.

| Panel | Element | Description |
|---|---|---|
| Left | **Current slide** | Large live preview of the active slide, including the mirrored laser dot |
| Right | **Next slide** | Preview of the upcoming slide |
| Right | **Slide counter** | `current / total` display |
| Right | **Prev / Next buttons** | Click-based navigation |
| Right | **Speaker notes** | Editable text field per slide; auto-saved to `<pdf>.notes.json` |
| Right | **Wall clock** | Current time (`HH:MM:SS`) |
| Right | **Presentation timer** | Elapsed time; start/pause with the `▶` / `⏸` button |
| Right | **Laser pointer button** | Activates the laser in the current-slide preview and broadcasts to the audience |
| Right | **Dark-mode toggle** | Switches both views simultaneously |

### Keyboard shortcuts (presenter view)

| Key | Action |
|---|---|
| `→` or `Space` | Next slide |
| `←` | Previous slide |
| `Home` | First slide |
| `End` | Last slide |
| `L` | Toggle laser pointer |
| `D` | Toggle dark / light mode |

### Speaker notes

Notes are typed in the text field in the right sidebar of the presenter
view. They are saved automatically — no explicit save action required.
The notes file (e.g. `slides.notes.json`) lives next to the source PDF
and is reloaded every time `labeam host` starts, so notes persist across
presentation sessions.

### Presentation timer

The timer in the top-right of the presenter view starts when you first
navigate to the next slide or press `▶`. It can be paused and resumed at
any time. The timer counts up from zero and displays elapsed time as
`MM:SS`.
