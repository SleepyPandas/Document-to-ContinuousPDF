"""
Document-to-ContinuousPDF

A Python package that converts HTML files into a long,
continuous PDF without page breaks.
"""

__version__ = "0.1.0"

from .converter import convert
from .utils import timer
__all__ = ["convert", "timer", "__version__"]
