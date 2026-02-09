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
| **Markdown Rendering** | GitHub-flavored Markdown with syntax highlighting via Pygments


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
```

### Python API

```python
from seamless_pdf import convert

convert("input.html", "output.pdf")
convert("README.md", "readme.pdf")
convert("report.docx", "report.pdf")
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
```

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
- [ ] Improved error handling and diagnostics
- [ ] Broader PDF manipulation toolset
- [ ] Dark mode PDF output

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
