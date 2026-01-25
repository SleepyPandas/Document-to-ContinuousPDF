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
        description="Convert an HTML or Markdown document to a continuous PDF."
    )
    parser.add_argument("input_file", help="Path to the input HTML or Markdown file.")
    parser.add_argument(
        "-o",
        "--output",
        default="output.pdf",
        help="Path to the output PDF file (default: output.pdf).",
    )

    args = parser.parse_args()

    try:
        # Run the conversion and report success.
        convert(args.input_file, args.output)
        print(f"Successfully converted '{args.input_file}' to '{args.output}'")
    except Exception as e:
        # Surface errors on stderr and exit with a non-zero code.
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    # Allow running as a script: python -m seamless_pdf.cli
    main()
