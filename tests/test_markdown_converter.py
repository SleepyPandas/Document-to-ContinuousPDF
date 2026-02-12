"""
Tests for Markdown converter utilities.
"""

from pathlib import Path
from unittest.mock import patch

import pytest

from seamless_pdf.markdown_converter import convert_markdown_to_pdf


def _make_dummy_markdown(tmp_path: Path) -> Path:
    markdown_path = tmp_path / "sample.md"
    markdown_path.write_text("# Sample", encoding="utf-8")
    return markdown_path


def test_convert_markdown_to_pdf_calls_html_pipeline(tmp_path):
    markdown_path = _make_dummy_markdown(tmp_path)
    output_path = tmp_path / "output.pdf"

    with patch(
        "seamless_pdf.markdown_converter.convert_markdown_to_html"
    ) as mock_markdown_to_html:
        with patch(
            "seamless_pdf.markdown_converter.convert_html_to_pdf"
        ) as mock_html_to_pdf:
            convert_markdown_to_pdf(str(markdown_path), str(output_path))

    mock_markdown_to_html.assert_called_once()
    temp_html_path = mock_markdown_to_html.call_args.args[1]
    assert temp_html_path.endswith(".html")
    mock_html_to_pdf.assert_called_once_with(temp_html_path, str(output_path))
    assert not Path(temp_html_path).exists()


def test_convert_markdown_to_pdf_cleans_temp_file_on_failure(tmp_path):
    markdown_path = _make_dummy_markdown(tmp_path)
    output_path = tmp_path / "output.pdf"

    with patch(
        "seamless_pdf.markdown_converter.convert_markdown_to_html"
    ) as mock_markdown_to_html:
        with patch(
            "seamless_pdf.markdown_converter.convert_html_to_pdf",
            side_effect=RuntimeError("PDF conversion failed"),
        ):
            with pytest.raises(RuntimeError, match="PDF conversion failed"):
                convert_markdown_to_pdf(str(markdown_path), str(output_path))

    mock_markdown_to_html.assert_called_once()
    temp_html_path = mock_markdown_to_html.call_args.args[1]
    assert not Path(temp_html_path).exists()
