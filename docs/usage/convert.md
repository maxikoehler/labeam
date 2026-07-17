# Convert

`labeam convert` converts a PDF presentation into a **self-contained HTML file**.
Every slide is embedded as an SVG; no external assets are required to open or share the result.

## Basic usage

```shell
labeam convert presentation.pdf
```

The output file is written to `presentation.html` in the same directory.

## Options

| Option | Default | Description |
|---|---|---|
| `PDF_PATH` | *(required)* | Path to the source PDF file |
| `--output`, `-o` | `<pdf_stem>.html` | Output HTML file path |
| `--title` | PDF filename (sanitised) | Presentation title shown in the browser tab |
| `--author` | *(empty)* | Author name shown in slide footers |
| `--date` | *(empty)* | Date string shown in slide footers (e.g. `"July 2026"`) |
| `--department` | *(empty)* | Department or team name shown in slide footers |
| `--classification` | *(empty)* | Document classification label (e.g. `"Public"`) |
| `--theme` | `light` | Initial colour theme: `light` or `dark` |

## Examples

**Minimal — output next to the source PDF:**

```shell
labeam convert slides.pdf
```

**Custom output path with metadata:**

```shell
labeam convert slides.pdf \
  --output ~/Desktop/slides.html \
  --title "Q3 Review" \
  --author "Jane Doe" \
  --date "July 2026" \
  --department "R&D" \
  --classification "Internal"
```

**Start in dark mode:**

```shell
labeam convert slides.pdf --theme dark
```

## Features of the generated HTML

The resulting HTML file is fully self-contained and works offline in any modern browser.

### Navigation

| Action | Keyboard | Mouse / Touch |
|---|---|---|
| Next slide | `→` or `Space` | Click the `→` button / swipe left |
| Previous slide | `←` | Click the `←` button / swipe right |
| First slide | `Home` | — |
| Last slide | `End` | — |

### Table of contents

Press `T` (or click the `≡` button) to open a slide overview panel.
Entries are built from the PDF's bookmark outline; if the PDF has no outline, the panel lists all slides by number.

### Laser pointer

Press `L` to activate the laser pointer.
Move the mouse over the slide to project a red dot.
Press `L` again or `Esc` to deactivate.

### Dark / light mode

Press `D` (or click the `☾` button) to toggle between light and dark theme.
The toggle is persistent within the current browser session.

### Progress bar

A thin bar at the top of the viewport indicates progress through the deck.
