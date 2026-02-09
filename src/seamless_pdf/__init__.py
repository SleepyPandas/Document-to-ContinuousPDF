"""
Document-to-ContinuousPDF

A Python package that converts HTML files into a long,
continuous PDF without page breaks.
"""

__version__ = "0.3.0"
Provides helpers to convert HTML, Markdown, and DOCX files into a single,
continuous PDF without page breaks.
"""

__version__ = "0.3.0"

from .converter import convert
from .utils import timer
__all__ = ["convert", "timer", "__version__"]
from .markdown_converter import convert_markdown_to_html
from .docx_converter import convert_docx_to_html

__all__ = [
    "convert",
    "timer",
    "__version__",
    "convert_markdown_to_html",
    "convert_docx_to_html",
]
