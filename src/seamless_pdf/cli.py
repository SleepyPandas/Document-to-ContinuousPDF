"""
Command-line interface entry point for seamless_pdf.
"""

import argparse
import sys
from seamless_pdf.converter import convert


def main():
    """Parse CLI arguments and run the conversion."""
    # Define CLI arguments and defaults.
    parser = argparse.ArgumentParser(
        description="Convert an HTML, Markdown, or DOCX document to a continuous PDF."
    )
    parser.add_argument(
        "input_file", help="Path to the input HTML, Markdown, or DOCX file."
    )
    parser.add_argument(
        "-o",
        "--output",
        default="output.pdf",
        help="Path to the output PDF file (default: output.pdf).",
    )
    parser.add_argument(
        "--input-type",
        choices=["html", "markdown", "docx"],
        default=None,
        help="Optional input type override (html, markdown, or docx).",
    )
    parser.add_argument(
        "--width",
        default=None,
        help="Optional page width for the generated PDF (e.g. '800px', '210mm').",
    )
    parser.add_argument(
        "--theme",
        choices=["light", "dark"],
        default="light",
        help="Optional render theme for generated PDF output (default: light).",
    )

    args = parser.parse_args()

    try:
        # Run the conversion and report success.
        convert(
            args.input_file,
            args.output,
            input_type=args.input_type,
            theme=args.theme,
            width=args.width,
        )
        print(f"Successfully converted '{args.input_file}' to '{args.output}'")
    except Exception as e:
        # Surface errors on stderr and exit with a non-zero code.
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    # Allow running as a script: python -m seamless_pdf.cli
    main()
