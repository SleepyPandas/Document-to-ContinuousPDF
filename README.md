# Seamless PDF

Convert HTML documents into continuous, single-page PDFs without page breaks.

## Installation

```bash
pip install seamless_pdf
playwright install chromium
```

## Quick Start

**CLI:**
```bash
seamless-pdf input.html -o output.pdf
```

**Python:**
```python
from seamless_pdf import convert

convert("input.html", "output.pdf")
```

## Requirements

- Python 3.7+
- Playwright (Chromium)

## License

MIT License - see [LICENSE](LICENSE) for details.


## Whats Next?
[ ] Add support for other formats (e.g. PDF, DOCX, Word, Markdown).
<br>
[ ] Add Error / Expection handling 
<br>
[ ] Branch into A larger suite of tools for PDF manipulation... TBD