import argparse
import sys
from seamless_pdf.converter import convert


def main():
    parser = argparse.ArgumentParser(
        description="Convert an HTML document to a continuous PDF."
    )
    parser.add_argument("input_file", help="Path to the input HTML file.")
    parser.add_argument(
        "-o",
        "--output",
        default="output.pdf",
        help="Path to the output PDF file (default: output.pdf).",
    )

    args = parser.parse_args()

    try:
        convert(args.input_file, args.output)
        print(f"Successfully converted '{args.input_file}' to '{args.output}'")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
