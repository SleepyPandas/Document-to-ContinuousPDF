"""
HTML to PDF conversion using Playwright and a single long page size.
"""

from playwright.sync_api import sync_playwright
from seamless_pdf.utils import to_file_url


def convert_html_to_pdf(input_path, output_path="output.pdf"):
    """
    Convert an HTML document to a continuous PDF.

    Args:
        input_path (str): Path to the input document.
        output_path (str): Path to the output PDF.

    Returns:
        None

    Raises:
        FileNotFoundError: If the input file does not exist.
        Exception: Propagates Playwright errors raised during rendering.
    """

    with sync_playwright() as playwright:

        # Launch Chromium headless for deterministic, scriptable rendering.
        browser = playwright.chromium.launch(headless=True)
        # Use a fresh page context for each conversion.
        page = browser.new_page()

        # Ensure Playwright receives a file:// URL, even for relative inputs.
        file_url = to_file_url(input_path)

        # Load the local HTML file into the browser context.
        page.goto(file_url)

        # Emulate "screen" media so rendered styles match on-screen output.
        page.emulate_media(media="screen")

        # Compute the full document size to avoid page breaks.
        page_height = (str)(page.evaluate("document.body.scrollHeight")) + "px"
        page_width = (str)(page.evaluate("document.body.scrollWidth")) + "px"

        # Export a single-page PDF sized to the full document.
        page.pdf(
            path=str(output_path),
            width=page_width,
            height=page_height,
            print_background=True,
        )

        # Always close the browser to release resources.
        browser.close()
