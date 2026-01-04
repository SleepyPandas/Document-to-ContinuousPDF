"""
Document-to-ContinuousPDF

A Python package that converts Doc, PDF, Word, and HTML files
into a long continuous PDF without page breaks.
"""

__version__ = "0.1.0"

from .converter import convert

__all__ = ["convert", "__version__"]
