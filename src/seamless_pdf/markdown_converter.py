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


    html_body = markdown.markdown(text)

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

    raise NotImplementedError("Markdown conversion is not implemented yet.")
