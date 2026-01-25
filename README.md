# Seamless PDF

Convert HTML, Markdown, and DOCX documents into continuous, single-page PDFs without page breaks.

## Features

- Single-page PDF output sized to the full document height and width
- Supports HTML, Markdown, and DOCX inputs
- CLI and Python API
- GitHub-style Markdown rendering with syntax highlighting
- DOCX conversion powered by mammoth

## Installation

```bash
pip install seamless-pdf
python -m playwright install chromium
```

## Quick Start

CLI:

```bash
seamless-pdf input.html -o output.pdf
seamless-pdf README.md -o README.pdf
seamless-pdf report.docx -o report.pdf
```

Python:

```python
from seamless_pdf import convert

convert("input.html", "output.pdf")
convert("README.md", "README.pdf")
convert("report.docx", "report.pdf")
```

## Usage

The `convert` function detects the input type by extension (`.html`, `.htm`, `.md`, `.markdown`, `.docx`).
You can override detection with `input_type="html"`, `input_type="markdown"`, or `input_type="docx"`.

```python
from seamless_pdf import convert

convert("docs/notes.md", "notes.pdf", input_type="markdown")
```

## Requirements

- Python >= 3.10 (tested on 3.10-3.12)
- Playwright (Chromium)
- markdown >= 3.10.1
- Pygments >= 2.17.0
- pymdown-extensions >= 10.0
- mammoth >= 1.6.0

## License

MIT License - see [LICENSE](LICENSE) for details.

## Roadmap

- Add support for additional input formats (PDF, Word)
- Improve error handling and diagnostics
- Broaden the PDF manipulation toolset
- HTML/PDF to mobile-friendly interface
- Dark mode PDF output
