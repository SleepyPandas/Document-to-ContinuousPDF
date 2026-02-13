"""
HTML to PDF conversion using Playwright and a single long page size.
"""

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError, sync_playwright

from seamless_pdf.utils import normalize_theme, to_file_url

DEFAULT_NAVIGATION_TIMEOUT_MS = 30_000
DEFAULT_LOAD_STATE_TIMEOUT_MS = 10_000
DEFAULT_RENDER_SETTLE_MS = 250


def _wait_for_page_to_settle(page):
    """
    Wait until the page has reached a stable render state.

    Some documents run client-side scripts or lazy-load assets. Waiting for
    multiple load signals helps avoid race conditions when measuring content
    dimensions for PDF generation.
    """

    page.wait_for_load_state("domcontentloaded", timeout=DEFAULT_LOAD_STATE_TIMEOUT_MS)
    page.wait_for_load_state("load", timeout=DEFAULT_LOAD_STATE_TIMEOUT_MS)
    try:
        page.wait_for_load_state("networkidle", timeout=DEFAULT_LOAD_STATE_TIMEOUT_MS)
    except PlaywrightTimeoutError:
        # Some pages keep long-running connections open; proceed once primary
        # load states are complete instead of failing indefinitely.
        pass
    page.wait_for_function(
        "() => document.body !== null && document.readyState !== 'loading'",
        timeout=DEFAULT_LOAD_STATE_TIMEOUT_MS,
    )
    page.wait_for_timeout(DEFAULT_RENDER_SETTLE_MS)


def convert_html_to_pdf(input_path, output_path="output.pdf", theme="light"):
    """
    Convert an HTML document to a continuous PDF.

    Args:
        input_path (str): Path to the input document.
        output_path (str): Path to the output PDF.
        theme (str): Render theme ("light" or "dark").

    Returns:
        None

    Raises:
        FileNotFoundError: If the input file does not exist.
        Exception: Propagates Playwright errors raised during rendering.
    """

    with sync_playwright() as playwright:
        selected_theme = normalize_theme(theme)

        # Launch Chromium headless for deterministic, scriptable rendering.
        browser = playwright.chromium.launch(headless=True)
        # Use a fresh page context for each conversion.
        page = browser.new_page()
        page.set_default_navigation_timeout(DEFAULT_NAVIGATION_TIMEOUT_MS)
        page.set_default_timeout(DEFAULT_LOAD_STATE_TIMEOUT_MS)

        # Ensure Playwright receives a file:// URL, even for relative inputs.
        file_url = to_file_url(input_path)

        # Load the local HTML file into the browser context.
        page.goto(
            file_url,
            wait_until="domcontentloaded",
            timeout=DEFAULT_NAVIGATION_TIMEOUT_MS,
        )

        # Emulate "screen" media so rendered styles match on-screen output.
        page.emulate_media(media="screen", color_scheme=selected_theme)
        _wait_for_page_to_settle(page)

        # Compute the full document size to avoid page breaks.
        page_height = (
            str(
                int(
                    page.evaluate(
                        """
                        () => {
                            const body = document.body;
                            const doc = document.documentElement;
                            return Math.max(
                                body ? body.scrollHeight : 0,
                                body ? body.offsetHeight : 0,
                                doc ? doc.clientHeight : 0,
                                doc ? doc.scrollHeight : 0,
                                doc ? doc.offsetHeight : 0,
                                1
                            );
                        }
                        """
                    )
                )
            )
            + "px"
        )
        page_width = (
            str(
                int(
                    page.evaluate(
                        """
                        () => {
                            const body = document.body;
                            const doc = document.documentElement;
                            return Math.max(
                                body ? body.scrollWidth : 0,
                                body ? body.offsetWidth : 0,
                                doc ? doc.clientWidth : 0,
                                doc ? doc.scrollWidth : 0,
                                doc ? doc.offsetWidth : 0,
                                1
                            );
                        }
                        """
                    )
                )
            )
            + "px"
        )

        # Export a single-page PDF sized to the full document.
        page.pdf(
            path=str(output_path),
            width=page_width,
            height=page_height,
            print_background=True,
        )

        # Always close the browser to release resources.
        browser.close()
