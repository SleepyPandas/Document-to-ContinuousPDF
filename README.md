# Seamless PDF

Convert HTML and Markdown documents into continuous, single-page PDFs without page breaks.

## Features

- Single-page PDF output sized to the full document height and width
- Supports HTML and Markdown inputs
- CLI and Python API
- GitHub-style Markdown rendering with syntax highlighting

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
```

Python:

```python
from seamless_pdf import convert

convert("input.html", "output.pdf")
convert("README.md", "README.pdf")
```

## Usage

The `convert` function detects the input type by extension (`.html`, `.htm`, `.md`, `.markdown`).
You can override detection with `input_type="html"` or `input_type="markdown"`.

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


## License

MIT License - see [LICENSE](LICENSE) for details.

## Roadmap

- Add support for additional input formats (PDF, DOCX)
- Expand error handling and diagnostics
- Broaden the PDF manipulation toolset
