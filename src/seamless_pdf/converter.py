from playwright.sync_api import sync_playwright


"""
Core conversion logic for document to continuous PDF conversion.
"""


def convert(input_path, output_path="output.pdf"):
    """
    Convert a document to a continuous PDF. TODO: This is only for HTML files currently.

    Args:
        input_path (str): Path to the input document.
        output_path (str): Path to the output PDF.
    """

    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("file:///" + input_path)

        # As if a human was viewing the page it fixes some odd graphical errors.

        page.emulate_media(media="screen")

        # now find the scrollHeight

        page_height = (str)(page.evaluate("document.body.scrollHeight")) + "px"
        page_width = (str)(page.evaluate("document.body.scrollWidth")) + "px"

        page.pdf(
            path=output_path,
            width=page_width,
            height=page_height,
            print_background=True,
        )

        browser.close()


# TODO: ADD file:/// to aboslute path at beginning


if __name__ == "__main__":
    convert(
        "C:/Users/AnthonyPC/Documents/GitHub/Document-to-ContinuousPDF/examples/207 individutal contribution.html"
    )
