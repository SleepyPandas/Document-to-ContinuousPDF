from pathlib import Path

from playwright.sync_api import sync_playwright

from seamless_pdf.utils import timer
from seamless_pdf.exceptions import PDFConversionError


"""
Core conversion logic for document to continuous PDF conversion.
"""
from seamless_pdf.markdown_converter import convert_markdown_to_pdf
from seamless_pdf.html_converter import convert_html_to_pdf
from seamless_pdf.docx_converter import convert_docx_to_pdf
from seamless_pdf.utils import detect_input_type, timer
from seamless_pdf.exceptions import PDFConversionError


def _get_converter(input_type):
    """Return the correct converter function for a detected input type."""
    if input_type == "html":
        return convert_html_to_pdf
    if input_type == "markdown":
        return convert_markdown_to_pdf
    if input_type == "docx":
        return convert_docx_to_pdf
    raise ValueError(f"Unsupported input type: {input_type}")


def _to_file_url(input_path):
    if isinstance(input_path, str) and input_path.startswith("file://"):
        return input_path

    resolved_path = Path(input_path).expanduser()
    if not resolved_path.is_absolute():
        resolved_path = (Path.cwd() / resolved_path).resolve()
    else:
        resolved_path = resolved_path.resolve()

    if not resolved_path.exists():
        raise FileNotFoundError(f"Input file not found: {resolved_path}")

    return resolved_path.as_uri()

@timer
def convert(input_path, output_path="output.pdf"):
    """
    Convert a document to a continuous PDF.

    Args:
        input_path (str): Path to the input document.
        output_path (str): Path to the output PDF.
    """

    try:
        with sync_playwright() as playwright:

            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()

            file_url = _to_file_url(input_path)

            page.goto(file_url)

            # As if a human was viewing the page it fixes some odd graphical errors.

            page.emulate_media(media="screen")

            # now find the scrollHeight

            page_height = (str)(page.evaluate("document.body.scrollHeight")) + "px"
            page_width = (str)(page.evaluate("document.body.scrollWidth")) + "px"

            page.pdf(
                path=str(output_path),
                width=page_width,
                height=page_height,
                print_background=True,
            )

            browser.close()
    except Exception as e:
        raise PDFConversionError(f"Failed to convert {input_path}: {str(e)}") from e
