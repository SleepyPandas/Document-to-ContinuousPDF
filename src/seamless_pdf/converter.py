from pathlib import Path

from playwright.sync_api import sync_playwright

from seamless_pdf.utils import timer
from seamless_pdf.exceptions import PDFConversionError


"""
Core conversion logic for document to continuous PDF conversion.
"""


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
