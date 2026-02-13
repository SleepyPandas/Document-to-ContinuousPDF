<div align="center">

# Seamless PDF

**Convert HTML, Markdown, and DOCX documents into continuous, single-page PDFs -- no page breaks.**

[![PyPI Version](https://img.shields.io/pypi/v/seamless-pdf?style=flat&color=blue)](https://pypi.org/project/seamless-pdf/)
[![License](https://img.shields.io/github/license/SleepyPandas/Document-to-ContinuousPDF?style=flat)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/SleepyPandas/Document-to-ContinuousPDF/test.yml?style=flat&label=tests)](https://github.com/SleepyPandas/Document-to-ContinuousPDF/actions)

![Python Versions](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue?style=flat)

</div>

---



Standard PDF converters split your content across fixed-size pages. **Seamless PDF** renders the entire document onto a single continuous page perfectly sized to the content's width and height. Ideal for long-form reports, documentation snapshots, newsletters and any workflow where page breaks get in the way or you want to retain the original content viewing experience.

---

## Features

| Feature | Description |
|---|---|
| **Single-Page Output** | One continuous PDF sized exactly to your content |
| **Multi-Format Input** | Supports `.html`, `.md`, `.markdown`, and `.docx` files |
| **CLI & Python API** | Use from the terminal or integrate directly into your code |
| **Markdown Rendering** | GitHub-flavored Markdown with syntax highlighting via Pygments |
| **Theme Selection (v0.4.0)** | Render output with `light` or `dark` theme via API/CLI |
| **Reliability Improvements (v0.4.0)** | Safer temp-file handling and stronger HTML render wait strategy |
| **DOCX Diagnostics (v0.4.0)** | Mammoth conversion warnings/errors are surfaced clearly |


---

## Installation

```bash
pip install seamless-pdf
python -m playwright install chromium
playwright install
```

> **Note:** Playwright uses a headless Chromium browser under the hood to render documents. The second command downloads the browser binary. For first time installs of playwright or updates you may need download the new browsers with `playwright install`.
> 

---

## Quick Start

### Command Line

```bash
seamless-pdf input.html -o output.pdf
seamless-pdf README.md -o README.pdf
seamless-pdf report.docx -o report.pdf
seamless-pdf README.md -o README-dark.pdf --theme dark
```

### Python API

```python
from seamless_pdf import convert

convert("input.html", "output.pdf")
convert("README.md", "readme.pdf")
convert("report.docx", "report.pdf")
convert("README.md", "readme-dark.pdf", theme="dark")
```

---

## Usage

The `convert` function automatically detects the input format from the file extension (`.html`, `.htm`, `.md`, `.markdown`, `.docx`). You can also specify the format explicitly:

```python
from seamless_pdf import convert

# Auto-detected as Markdown
convert("docs/notes.md", "notes.pdf")

# Explicit input type override
convert("docs/notes.txt", "notes.pdf", input_type="markdown")

# Optional render theme (light or dark)
convert("docs/notes.md", "notes-dark.pdf", theme="dark")
```

### CLI Options

```bash
# Explicit input type override
seamless-pdf docs/notes.txt -o notes.pdf --input-type markdown

# Dark theme rendering
seamless-pdf docs/notes.md -o notes-dark.pdf --theme dark
```

### NOTES on DARKMODE FLAG

Dark mode behavior depends on the input type:

- **Markdown / DOCX inputs**: Seamless PDF generates HTML and injects the selected theme styles. Using `--theme dark` (or `theme="dark"`) is expected to produce dark-themed output consistently.
- **HTML inputs**: Seamless PDF respects the source HTML/CSS and renders it as-is in Chromium with dark color-scheme emulation. If the source HTML is not dark-aware (for example, no dark styles, no `prefers-color-scheme` rules, or hardcoded light colors), dark output is **best effort** and cannot be guaranteed.

Practical guidance:

- For guaranteed dark output from HTML, provide HTML that already supports dark mode.
- For light-only HTML, `--theme dark` remains available but may produce mixed contrast depending on the original styles.

### Supported Input Types

| Extension | Type Keyword |
|---|---|
| `.html`, `.htm` | `html` |
| `.md`, `.markdown` | `markdown` |
| `.docx` | `docx` |

---

## Requirements

| Dependency | Version |
|---|---|
| Python | 3.10, 3.11, 3.12, 3.13 |
| Playwright (Chromium) | >= 1.40.0 |
| markdown | >= 3.10.1 |
| Pygments | >= 2.17.0 |
| pymdown-extensions | >= 10.0 |
| mammoth | >= 1.6.0 |

---

## Roadmap

- [ ] PDF-to-PDF re-rendering (merge & reflow existing PDFs)
- [ ] Broader PDF manipulation toolset

---

## What's New in v0.4.0

- Added optional dark-mode rendering through `theme="dark"` (API) and `--theme dark` (CLI).
- Replaced hardcoded temporary intermediate HTML filenames with per-run temp files and cleanup for safer concurrent conversions.
- Hardened Playwright page-settle behavior before document measurement/PDF export to reduce race-condition failures.
- DOCX conversion now surfaces Mammoth diagnostics (warnings and errors) instead of silently ignoring conversion messages.
- Added developer extras and coverage config so editable development installs are documented and reproducible.

---





## Cloning for your purposes...
```bash
git clone https://github.com/SleepyPandas/Document-to-ContinuousPDF.git
cd Document-to-ContinuousPDF
pip install -e ".[dev]"
pytest
```

---

## License

This project is licensed under the **MIT License** -- see the [LICENSE](LICENSE) file for details.
