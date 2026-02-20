"""
DOCX conversion utilities.

This module converts DOCX documents to HTML (using mammoth) and then
to a continuous PDF via the HTML converter.
"""

import os
import tempfile
import warnings

import mammoth

from seamless_pdf.html_converter import convert_html_to_pdf
from seamless_pdf.utils import get_css_style


def _format_mammoth_diagnostics(messages):
    """Format Mammoth messages into readable diagnostics."""
    formatted = []
    for message in messages:
        level = str(getattr(message, "type", "info")).upper()
        text = str(getattr(message, "message", message))
        formatted.append(f"- [{level}] {text}")
    return "\n".join(formatted)


def _emit_docx_diagnostics(messages):
    """
    Surface Mammoth diagnostics to users and callers.

    Errors are raised so failed conversions are explicit. Non-error diagnostics
    are emitted as warnings to improve visibility without breaking flow.
    """

    if not messages:
        return

    diagnostics = _format_mammoth_diagnostics(messages)
    diagnostic_message = f"DOCX conversion reported diagnostics:\n{diagnostics}"
    has_errors = any(
        str(getattr(msg, "type", "")).lower() == "error" for msg in messages
    )

    if has_errors:
        raise ValueError(diagnostic_message)

    warnings.warn(diagnostic_message, UserWarning, stacklevel=2)


def convert_docx_to_html(input_path, output_path="output.html", theme="light"):
    """
    Convert a DOCX document to HTML.

    Args:
        input_path (str): Path to the input DOCX document.
        output_path (str): Path to the output HTML file.
        theme (str): Render theme for injected CSS ("light" or "dark").

    Returns:
        None

    Raises:
        ValueError: If Mammoth reports one or more conversion errors.
    """

    # Read the DOCX file and convert its content to HTML via mammoth.
    with open(input_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        _emit_docx_diagnostics(list(getattr(result, "messages", []) or []))
        html_body = result.value

    # Wrap the generated HTML in a full document and inject CSS styling.
    final_output = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Document</title>
        {get_css_style(theme)}
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """

    # Write the HTML document to disk.
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_output)


def convert_docx_to_pdf(
    input_path, output_path="output.pdf", theme="light", width=None
):
    """
    Convert a DOCX document to a continuous PDF.

    Args:
        input_path (str): Path to the input DOCX document.
        output_path (str): Path to the output PDF.
        theme (str): Render theme for generated output ("light" or "dark").
        width (str | None): Optional page width.

    Returns:
        None
    """

    # Convert DOCX to a unique temporary HTML file, then render to PDF.
    temp_fd, temp_html_path = tempfile.mkstemp(suffix=".html")
    os.close(temp_fd)

    try:
        convert_docx_to_html(input_path, temp_html_path, theme=theme)
        convert_html_to_pdf(temp_html_path, output_path, theme=theme, width=width)
    finally:
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)
