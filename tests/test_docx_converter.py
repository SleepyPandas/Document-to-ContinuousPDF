"""
Tests for DOCX converter utilities.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

from seamless_pdf.docx_converter import convert_docx_to_html, convert_docx_to_pdf
from seamless_pdf.utils import css_style, detect_input_type
from seamless_pdf.converter import convert


def _make_dummy_docx(tmp_path: Path) -> Path:
    docx_path = tmp_path / "sample.docx"
    docx_path.write_bytes(b"fake-docx-content")
    return docx_path


def test_convert_docx_to_html_writes_wrapped_html(tmp_path):
    docx_path = _make_dummy_docx(tmp_path)
    output_path = tmp_path / "output.html"
    mocked_html = "<h1>Hello DOCX</h1>"

    with patch("seamless_pdf.docx_converter.mammoth.convert_to_html") as mock_convert:
        mock_result = MagicMock()
        mock_result.value = mocked_html
        mock_convert.return_value = mock_result

        convert_docx_to_html(str(docx_path), str(output_path))

    contents = output_path.read_text(encoding="utf-8")
    assert mocked_html in contents
    assert css_style in contents
    assert "<!DOCTYPE html>" in contents


def test_convert_docx_to_pdf_calls_html_pipeline(tmp_path, monkeypatch):
    docx_path = _make_dummy_docx(tmp_path)
    output_path = tmp_path / "output.pdf"

    monkeypatch.chdir(tmp_path)

    with patch("seamless_pdf.docx_converter.convert_docx_to_html") as mock_docx_to_html:
        with patch(
            "seamless_pdf.docx_converter.convert_html_to_pdf"
        ) as mock_html_to_pdf:
            convert_docx_to_pdf(str(docx_path), str(output_path))

    mock_docx_to_html.assert_called_once_with(str(docx_path), "temp.html")
    mock_html_to_pdf.assert_called_once_with("temp.html", str(output_path))


def test_detect_input_type_docx():
    assert detect_input_type("file.docx") == "docx"


def test_convert_routes_docx(tmp_path):
    docx_path = _make_dummy_docx(tmp_path)
    output_path = tmp_path / "output.pdf"

    with patch("seamless_pdf.converter.convert_docx_to_pdf") as mock_docx_to_pdf:
        convert(str(docx_path), str(output_path))

    mock_docx_to_pdf.assert_called_once_with(str(docx_path), str(output_path))