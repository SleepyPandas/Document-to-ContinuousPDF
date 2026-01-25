"""
Facade for converting supported documents into a single, continuous PDF.

This module keeps input-type detection and converter selection in one
place, then wraps underlying errors in a package-specific exception.
"""

from seamless_pdf.markdown_converter import convert_markdown_to_pdf
from seamless_pdf.html_converter import convert_html_to_pdf
from seamless_pdf.utils import detect_input_type, timer
from seamless_pdf.exceptions import PDFConversionError


def _get_converter(input_type):
    """Return the correct converter function for a detected input type."""
    if input_type == "html":
        return convert_html_to_pdf
    if input_type == "markdown":
        return convert_markdown_to_pdf
    raise ValueError(f"Unsupported input type: {input_type}")


@timer
def convert(input_path, output_path="output.pdf", input_type=None):
    """
    Convert a supported document to a continuous PDF.

    Args:
        input_path (str): Path to the input document.
        output_path (str): Path to the output PDF.
        input_type (str | None): Optional override for input type detection.

    Returns:
        Any: The return value from the underlying converter, if any.

    Raises:
        PDFConversionError: If conversion fails for any reason.
    """

    try:
        # Use a caller-provided type override, or detect from the input path.
        detected_type = input_type or detect_input_type(input_path)
        # Dispatch to the appropriate converter function.
        converter = _get_converter(detected_type)
        return converter(input_path, output_path)
    except Exception as e:
        # Normalize all errors into one package-specific exception.
        raise PDFConversionError(f"Failed to convert {input_path}: {str(e)}") from e
