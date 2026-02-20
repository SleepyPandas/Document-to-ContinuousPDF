"""
Markdown conversion utilities.

This module converts Markdown to HTML (with GitHub-like styling) and then
to a continuous PDF via the HTML converter.
"""

import markdown
import os
import re
import tempfile

from seamless_pdf.html_converter import convert_html_to_pdf
from seamless_pdf.utils import get_css_style


def _enable_markdown_inside_center_divs(text):
    """
    Add markdown=\"1\" to centered div wrappers so Markdown badges render.
    """

    def _replace_div(match):
        attrs = match.group("attrs") or ""
        attrs_lower = attrs.lower()
        if "markdown=" in attrs_lower:
            return match.group(0)
        if "align" not in attrs_lower or "center" not in attrs_lower:
            return match.group(0)
        return f'<div{attrs} markdown="1">'

    return re.sub(
        r"<div(?P<attrs>[^>]*)>",
        _replace_div,
        text,
        flags=re.IGNORECASE,
    )


def convert_markdown_to_html(input_path, output_path="output.html", theme="light"):
    """
    Convert a Markdown document to HTML.

    Args:
        input_path (str): Path to the input document.
        output_path (str): Path to the output HTML.
        theme (str): Render theme for injected CSS ("light" or "dark").

    Returns:
        None
    """

    # Read Markdown source from disk.
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()
    text = _enable_markdown_inside_center_divs(text)

    # Enable a rich set of Markdown extensions for a GitHub-like experience.
    extensions = [
        # --- Standard Built-ins ---
        "extra",  # Tables, Footnotes, Definition Lists, Abbreviations
        "md_in_html",  # Enable Markdown parsing inside opted-in raw HTML blocks
        "codehilite",  # Syntax Highlighting
        "toc",  # Auto-generates Table of Contents [TOC]
        "admonition",  # "Note" and "Warning" callout blocks
        "sane_lists",  # Better list behavior (standardizes mixing list types)
        "tables",  # Tables
        # --- PyMdown "Power User" Extensions ---
        "pymdownx.tasklist",  # GitHub-style Checkboxes (- [x])
        "pymdownx.arithmatex",  # Math/LaTeX support ($E=mc^2$)
        "pymdownx.superfences",  # Allows nesting code blocks inside lists
        "pymdownx.details",  # Collapsible "Details" blocks (requires superfences)
        "pymdownx.magiclink",  # Auto-links URLs without needing <brackets>
        "pymdownx.emoji",  # Emoji support (:smile:)
        "pymdownx.tilde",  # Strikethrough (~~text~~)
        "pymdownx.caret",  # Superscript (^text^)
        "pymdownx.mark",  # Highlighter text (==text==)
        "pymdownx.smartsymbols",  # Converts arrows and not-equal to typographic symbols
    ]

    # Convert Markdown into HTML.
    html_body = markdown.markdown(text, extensions=extensions)

    # Wrap the generated HTML in a full document and inject CSS styling.
    final_output = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>GitHub Style Doc</title>
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


def convert_markdown_to_pdf(
    input_path,
    output_path="output.pdf",
    theme="light",
    width=None,
    margin_top=None,
    margin_right=None,
    margin_bottom=None,
    margin_left=None,
):
    """
    Convert a Markdown document to a continuous PDF.

    Args:
        input_path (str): Path to the input document.
        output_path (str): Path to the output PDF.
        theme (str): Render theme for generated output ("light" or "dark").
        width (str | None): Optional page width.
        margin_top (str | None): Optional top margin.
        margin_right (str | None): Optional right margin.
        margin_bottom (str | None): Optional bottom margin.
        margin_left (str | None): Optional left margin.

    Returns:
        None
    """

    # Convert Markdown to a unique temporary HTML file, then render to PDF.
    temp_fd, temp_html_path = tempfile.mkstemp(suffix=".html")
    os.close(temp_fd)

    try:
        convert_markdown_to_html(input_path, temp_html_path, theme=theme)
        convert_html_to_pdf(
            temp_html_path,
            output_path,
            theme=theme,
            width=width,
            margin_top=margin_top,
            margin_right=margin_right,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
        )
    finally:
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)
