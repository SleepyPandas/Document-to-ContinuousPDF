from seamless_pdf.html_converter import convert_html_to_pdf
from seamless_pdf.utils import css_style
import markdown


def convert_markdown_to_html(input_path, output_path="output.html"):
    """
    Convert a Markdown document to HTML.

    Args:
        input_path (str): Path to the input document.
        output_path (str): Path to the output HTML.
    """

    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    extensions = [
        # --- Standard Built-ins ---
        "extra",  # Tables, Footnotes, Definition Lists, Abbreviations
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
        "pymdownx.smartsymbols",  # Converts --> to →, =/= to ≠
    ]

    html_body = markdown.markdown(text, extensions=extensions)

    final_output = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>GitHub Style Doc</title>
        {css_style}
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_output)


def convert_markdown_to_pdf(input_path, output_path="output.pdf"):
    """
    Convert a Markdown document to a continuous PDF.

    Args:
        input_path (str): Path to the input document.
        output_path (str): Path to the output PDF.
    """

    convert_markdown_to_html(input_path, "temp.html")
    convert_html_to_pdf("temp.html", output_path)
