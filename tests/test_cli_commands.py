"""
Tests for the command-line interface wrapper.
"""

import pytest
from unittest.mock import patch, ANY
import sys
from seamless_pdf.cli import main


def test_cli_success(tmp_path):
    """Test the CLI with valid input and output arguments."""
    # Create a temporary input file and output target.
    input_file = tmp_path / "input.html"
    input_file.touch()
    output_file = tmp_path / "result.pdf"

    # Simulate CLI arguments: program_name input_file -o output_file
    test_args = ["program_name", str(input_file), "-o", str(output_file)]

    with patch.object(sys, "argv", test_args):
        with patch("seamless_pdf.cli.convert") as mock_convert:
            # We also need to mock print/stdout to keep it clean or verify output?
            with patch("builtins.print") as mock_print:
                main()

                mock_convert.assert_called_once_with(
                    str(input_file),
                    str(output_file),
                    input_type=ANY,
                    theme=ANY,
                    width=ANY,
                    margin_top=ANY,
                    margin_right=ANY,
                    margin_bottom=ANY,
                    margin_left=ANY,
                )
                mock_print.assert_any_call(
                    f"Successfully converted '{input_file}' to '{output_file}'"
                )


def test_cli_defaults(tmp_path):
    """Test the CLI uses default output filename when not specified."""
    # Create a temporary input file.
    input_file = tmp_path / "input.html"
    input_file.touch()

    # Only provide the input path to trigger the default output name.
    test_args = ["program_name", str(input_file)]

    with patch.object(sys, "argv", test_args):
        with patch("seamless_pdf.cli.convert") as mock_convert:
            with patch("builtins.print") as mock_print:
                main()

                # Default output is "output.pdf"
                mock_convert.assert_called_once_with(
                    str(input_file),
                    "output.pdf",
                    input_type=ANY,
                    theme=ANY,
                    width=ANY,
                    margin_top=ANY,
                    margin_right=ANY,
                    margin_bottom=ANY,
                    margin_left=ANY,
                )
                mock_print.assert_any_call(
                    f"Successfully converted '{input_file}' to 'output.pdf'"
                )


def test_cli_input_type_override(tmp_path):
    """Test the CLI passes through --input-type to convert()."""
    input_file = tmp_path / "input.md"
    input_file.touch()
    output_file = tmp_path / "result.pdf"
    test_args = [
        "program_name",
        str(input_file),
        "-o",
        str(output_file),
        "--input-type",
        "markdown",
    ]

    with patch.object(sys, "argv", test_args):
        with patch("seamless_pdf.cli.convert") as mock_convert:
            with patch("builtins.print"):
                main()

    mock_convert.assert_called_once_with(
        str(input_file),
        str(output_file),
        input_type="markdown",
        theme=ANY,
        width=ANY,
        margin_top=ANY,
        margin_right=ANY,
        margin_bottom=ANY,
        margin_left=ANY,
    )


def test_cli_theme_override(tmp_path):
    """Test the CLI passes through --theme to convert()."""
    input_file = tmp_path / "input.md"
    input_file.touch()
    output_file = tmp_path / "result.pdf"
    test_args = [
        "program_name",
        str(input_file),
        "-o",
        str(output_file),
        "--theme",
        "dark",
    ]

    with patch.object(sys, "argv", test_args):
        with patch("seamless_pdf.cli.convert") as mock_convert:
            with patch("builtins.print"):
                main()

    mock_convert.assert_called_once_with(
        str(input_file),
        str(output_file),
        input_type=ANY,
        theme="dark",
        width=ANY,
        margin_top=ANY,
        margin_right=ANY,
        margin_bottom=ANY,
        margin_left=ANY,
    )


def test_cli_failure(tmp_path, capsys):
    """Test that the CLI handles converter exceptions gracefully."""
    # Create a temporary input file for the failing conversion path.
    input_file = tmp_path / "input.html"
    input_file.touch()

    test_args = ["program_name", str(input_file)]

    with patch.object(sys, "argv", test_args):
        # Mock convert to raise an exception
        with patch(
            "seamless_pdf.cli.convert", side_effect=Exception("Conversion failed")
        ):
            with pytest.raises(SystemExit) as excinfo:
                main()

            # Verify exit code 1
            assert excinfo.value.code == 1

            # Verify error message was printed to stderr
            captured = capsys.readouterr()
            assert "Error: Conversion failed" in captured.err


def test_cli_missing_args(capsys):
    """Test that argparse handles missing arguments (exits)."""
    # Passing no arguments should trigger argparse to print usage and exit
    test_args = ["program_name"]

    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit) as excinfo:
            main()

        captured = capsys.readouterr()
        # Argparse usually prints to stderr
        assert "the following arguments are required: input_file" in captured.err


def test_cli_invalid_input_type_choice(capsys):
    """Test argparse rejects invalid --input-type values."""
    test_args = ["program_name", "input.html", "--input-type", "txt"]

    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit) as excinfo:
            main()

    assert excinfo.value.code == 2
    captured = capsys.readouterr()
    assert "invalid choice" in captured.err


def test_cli_invalid_theme_choice(capsys):
    """Test argparse rejects invalid --theme values."""
    test_args = ["program_name", "input.html", "--theme", "sepia"]

    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit) as excinfo:
            main()

    assert excinfo.value.code == 2
    captured = capsys.readouterr()
    assert "invalid choice" in captured.err


def test_cli_playwright_missing_browser_hint(tmp_path, capsys):
    """Test that a missing Playwright browser error prints an install hint."""
    input_file = tmp_path / "input.html"
    input_file.touch()

    test_args = ["program_name", str(input_file)]

    with patch.object(sys, "argv", test_args):
        # Mock convert to raise an exception containing "Executable doesn't exist"
        with patch(
            "seamless_pdf.cli.convert",
            side_effect=Exception("Executable doesn't exist at /path/to/browser"),
        ):
            with pytest.raises(SystemExit):
                main()

            captured = capsys.readouterr()
            assert "Playwright browsers are not installed" in captured.err
            assert "python -m playwright install chromium" in captured.err
            assert "Error: Executable doesn't exist" in captured.err
