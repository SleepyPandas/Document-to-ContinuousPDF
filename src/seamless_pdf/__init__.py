"""
Document-to-ContinuousPDF

A Python package that converts HTML files into a long,
continuous PDF without page breaks.
"""

__version__ = "0.2.0"

from .converter import convert
from .utils import timer
from .markdown_converter import convert_markdown_to_html

__all__ = ["convert", "timer", "__version__", "convert_markdown_to_html"]
