"""
Tests for conversion utilities and the main convert facade.
"""

# Note: run with pytest from the repository root.

import pytest
from pathlib import Path
from seamless_pdf.utils import to_file_url
import os
from seamless_pdf.exceptions import PDFConversionError


def test_to_file_url_absolute_path(tmp_path):
    """Test converting an absolute path to a file URL."""
    # Create a dummy file
    f = tmp_path / "test.html"
    f.touch()

    expected_uri = f.as_uri()
    assert to_file_url(str(f)) == expected_uri


def test_to_file_url_relative_path(tmp_path):
    """Test converting a relative path to a file URL."""
    # Create a dummy file in the current working directory context
    # Since we can't easily change cwd in tests safely, we'll assume the file is in cwd
    # or just mock Path.cwd if strictly needed, but let's try creating a file relative to where pytest runs if possible.
    # Actually, simpler to just test that it resolves correctly using Path logic.

    # We will create a file in the current working directory, then cleanup
    cwd = Path.cwd()
    f = cwd / "temp_relative_test_file.html"
    f.touch()
    try:
        relative_path = "temp_relative_test_file.html"
        expected_uri = f.as_uri()
        assert to_file_url(relative_path) == expected_uri
    finally:
        f.unlink()


def test_to_file_url_existing_uri():
    """Test that an existing file:// URI is returned as is."""
    uri = "file:///path/to/file.html"
    assert to_file_url(uri) == uri


def test_to_file_url_not_found():
    """Test that FileNotFoundError is raised for non-existent files."""
    with pytest.raises(FileNotFoundError):
        to_file_url("non_existent_file.html")


from unittest.mock import patch, MagicMock
from seamless_pdf.converter import convert


# -------- Test Convert Function --------


@patch("seamless_pdf.html_converter.sync_playwright")
def test_convert_calls_playwright_correctly(mock_playwright, tmp_path):
    """Test that convert launches browser and calls PDF generation (Mocked)."""

    # Setup our mocks
    mock_context = mock_playwright.return_value.__enter__.return_value
    mock_browser = mock_context.chromium.launch.return_value
    mock_page = mock_browser.new_page.return_value

    # We need to simulate the page evaluating scroll height/width
    # The order of calls in your code: 1. scrollHeight, 2. scrollWidth
    mock_page.evaluate.side_effect = ["1000", "800"]

    # Create a dummy input file
    input_file = tmp_path / "test.html"
    input_file.touch()

    output_file = tmp_path / "output.pdf"

    # Run the function
    convert(str(input_file), str(output_file))

    # Assertions: Did it do what we expect?
    mock_page.goto.assert_called_once()
    assert mock_page.goto.call_args.kwargs["wait_until"] == "domcontentloaded"
    assert mock_page.goto.call_args.kwargs["timeout"] == 30000
    mock_page.emulate_media.assert_called_once_with(
        media="screen", color_scheme="light"
    )
    mock_page.wait_for_load_state.assert_any_call("domcontentloaded", timeout=10000)
    mock_page.wait_for_load_state.assert_any_call("load", timeout=10000)
    mock_page.wait_for_function.assert_called_once()

    # Verify PDF generation args
    mock_page.pdf.assert_called_with(
        path=str(output_file), width="800px", height="1000px", print_background=True
    )

    # Verify cleanup
    mock_browser.close.assert_called()


def test_convert_uses_input_type_override_without_detection(tmp_path):
    """Test that explicit input_type bypasses extension detection."""
    output_file = tmp_path / "output.pdf"

    with patch("seamless_pdf.converter.detect_input_type") as mock_detect:
        with patch(
            "seamless_pdf.converter.convert_markdown_to_pdf"
        ) as mock_markdown_converter:
            convert("document.unknown", str(output_file), input_type="markdown")

    mock_detect.assert_not_called()
    mock_markdown_converter.assert_called_once_with(
        "document.unknown", str(output_file), theme="light", width=None
    )


def test_convert_passes_theme_to_selected_converter(tmp_path):
    """Test that theme is forwarded to the selected converter."""
    output_file = tmp_path / "output.pdf"

    with patch("seamless_pdf.converter.convert_docx_to_pdf") as mock_docx_converter:
        convert("document.docx", str(output_file), theme="dark")

    mock_docx_converter.assert_called_once_with(
        "document.docx", str(output_file), theme="dark", width=None
    )


def test_convert_wraps_converter_failure_in_pdf_conversion_error(tmp_path):
    """Test converter failures are normalized to PDFConversionError."""
    output_file = tmp_path / "output.pdf"

    with patch("seamless_pdf.converter.convert_html_to_pdf") as mock_html_converter:
        mock_html_converter.side_effect = RuntimeError("renderer crashed")
        with pytest.raises(PDFConversionError, match="renderer crashed"):
            convert("document.html", str(output_file))


def test_convert_wraps_unsupported_input_type_errors(tmp_path):
    """Test unsupported input type override is wrapped consistently."""
    output_file = tmp_path / "output.pdf"

    with pytest.raises(PDFConversionError, match="Unsupported input type"):
        convert("document.md", str(output_file), input_type="rst")


def test_convert_wraps_unsupported_theme_errors(tmp_path):
    """Test unsupported themes are wrapped consistently."""
    output_file = tmp_path / "output.pdf"

    with pytest.raises(PDFConversionError, match="Unsupported theme"):
        convert("document.md", str(output_file), input_type="markdown", theme="sepia")
