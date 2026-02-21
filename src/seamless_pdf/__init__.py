"""
seamless_pdf package.

Provides helpers to convert HTML, Markdown, and DOCX files into a single,
continuous PDF without page breaks.
"""

__version__ = "1.0.1"

# Re-export common entry points for convenience.
from .converter import convert
from .utils import timer
from .markdown_converter import convert_markdown_to_html
from .docx_converter import convert_docx_to_html

__all__ = [
    "convert",
    "timer",
    "__version__",
    "convert_markdown_to_html",
    "convert_docx_to_html",
]
