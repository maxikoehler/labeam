# LaBeam

> Tool for converting PDF presentations to HTML for easier presenting.

LaBeam* turns LaTeX Beamer PDFs into interactive HTML presentations — with a laser pointer, dark mode, table of contents, a full presenter view with notes, and real-time audience synchronisation.
Core utilities are:
- ```labeam convert``` for converting a PDF presentation to a cross-plattform presentable HTML file, or
- ```labeam host``` for hosting a PDF preentation with presenter mode.

*_LaBeam stands for the initial missing **la**ser **beam** in **La**TeX **Beam**er presentations. Pun intended._

## Quickstart

### Prerequisites

In order to install and use the package, you need Python >=3.10. The package is tested up to Python 3.14.
Additionally you might use [uv](https://docs.astral.sh/uv/getting-started/installation/).

### Installation

Clone the repository and install from your local checkout.

**Option A — with [uv](https://docs.astral.sh/uv/) (recommended)**

```shell
git clone https://github.com/maxikoehler/labeam.git
cd labeam
uv tool install .
```

**Option B — with pip**

```shell
git clone https://github.com/maxikoehler/labeam.git
cd labeam
pip install .
```

Verify the installation:

```shell
labeam --help
```

### Usage

After that you can

```shell
labeam convert <PDF_FILE_PATH> -o <HTML_FILE_PATH>
```

to convert a PDF to HTML, or simply host a presentation on your local machine via:

```shell
labeam host <PDF_FILE_PATH>
```

## Acknowledgements

Thanks to Moritz Weber for sparking the idea and providing a nice and sufficient design to start with :)
