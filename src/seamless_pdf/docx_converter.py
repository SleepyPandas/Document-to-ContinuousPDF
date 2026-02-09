"""
DOCX conversion utilities.

This module converts DOCX documents to HTML (using mammoth) and then
to a continuous PDF via the HTML converter.
"""

import mammoth

from seamless_pdf.html_converter import convert_html_to_pdf
from seamless_pdf.utils import css_style


def convert_docx_to_html(input_path, output_path="output.html"):
    """
    Convert a DOCX document to HTML.

    Args:
        input_path (str): Path to the input DOCX document.
        output_path (str): Path to the output HTML file.

    Returns:
        None
    """

    # Read the DOCX file and convert its content to HTML via mammoth.
    with open(input_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html_body = result.value

    # Wrap the generated HTML in a full document and inject CSS styling.
    final_output = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Document</title>
        {css_style}
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """

    # Write the HTML document to disk.
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_output)


def convert_docx_to_pdf(input_path, output_path="output.pdf"):
    """
    Convert a DOCX document to a continuous PDF.

    Args:
        input_path (str): Path to the input DOCX document.
        output_path (str): Path to the output PDF.

    Returns:
        None
    """

    # Convert DOCX to a temporary HTML file, then render to PDF.
    convert_docx_to_html(input_path, "temp.html")
    convert_html_to_pdf("temp.html", output_path)
