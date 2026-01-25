from playwright.sync_api import sync_playwright
from seamless_pdf.utils import to_file_url


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

        file_url = to_file_url(input_path)

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
