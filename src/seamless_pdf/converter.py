from seamless_pdf.markdown_converter import convert_markdown_to_pdf
from seamless_pdf.html_converter import convert_html_to_pdf
from seamless_pdf.utils import detect_input_type
from pathlib import Path
from urllib.parse import unquote, urlparse

from seamless_pdf.utils import timer
from seamless_pdf.exceptions import PDFConversionError


"""
Core conversion logic for document to continuous PDF conversion.
"""


def _get_converter(input_type):
    if input_type == "html":
        return convert_html_to_pdf
    if input_type == "markdown":
        return convert_markdown_to_pdf
    raise ValueError(f"Unsupported input type: {input_type}")


@timer
def convert(input_path, output_path="output.pdf", input_type=None):
    """
    Convert a document to a continuous PDF. This is using a facade pattern to hide the complexity of the conversion process.


    Args:
        input_path (str): Path to the input document.
        output_path (str): Path to the output PDF.
        input_type (str | None): Optional override for input type detection.
    """

    try:
        detected_type = input_type or detect_input_type(input_path)
        converter = _get_converter(detected_type)
        return converter(input_path, output_path)
    except Exception as e:
        raise PDFConversionError(f"Failed to convert {input_path}: {str(e)}") from e
