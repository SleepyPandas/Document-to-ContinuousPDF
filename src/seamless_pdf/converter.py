from pathlib import Path
from urllib.parse import unquote, urlparse

from playwright.sync_api import sync_playwright

from seamless_pdf.utils import timer
from seamless_pdf.exceptions import PDFConversionError


"""
Core conversion logic for document to continuous PDF conversion.
"""

_HTML_EXTENSIONS = {".html", ".htm"}
_MARKDOWN_EXTENSIONS = {".md", ".markdown"}


def _path_from_input(input_path):
    if isinstance(input_path, Path):
        return input_path
    if isinstance(input_path, str) and input_path.startswith("file://"):
        parsed = urlparse(input_path)
        raw_path = unquote(parsed.path)
        if raw_path.startswith("/") and len(raw_path) > 2 and raw_path[2] == ":":
            raw_path = raw_path[1:]
        return Path(raw_path)
    return Path(input_path)


def _detect_input_type(input_path):
    suffix = _path_from_input(input_path).suffix.lower()
    if suffix in _HTML_EXTENSIONS:
        return "html"
    if suffix in _MARKDOWN_EXTENSIONS:
        return "markdown"
    raise ValueError(
        "Unsupported input type. Supported extensions: .html, .htm, .md, .markdown"
    )


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


def convert_html_to_pdf(input_path, output_path="output.pdf"):
    """
    Convert an HTML document to a continuous PDF.

    Args:
        input_path (str): Path to the input document.
        output_path (str): Path to the output PDF.
    """

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


def convert_markdown_to_pdf(input_path, output_path="output.pdf"):
    """
    Convert a Markdown document to a continuous PDF.

    Args:
        input_path (str): Path to the input document.
        output_path (str): Path to the output PDF.
    """

    raise NotImplementedError("Markdown conversion is not implemented yet.")


def _get_converter(input_type):
    if input_type == "html":
        return convert_html_to_pdf
    if input_type == "markdown":
        return convert_markdown_to_pdf
    raise ValueError(f"Unsupported input type: {input_type}")


@timer
def convert(input_path, output_path="output.pdf", input_type=None):
    """
    Convert a document to a continuous PDF.

    Args:
        input_path (str): Path to the input document.
        output_path (str): Path to the output PDF.
        input_type (str | None): Optional override for input type detection.
    """

    try:
        detected_type = input_type or _detect_input_type(input_path)
        converter = _get_converter(detected_type)
        return converter(input_path, output_path)
    except Exception as e:
        raise PDFConversionError(f"Failed to convert {input_path}: {str(e)}") from e
