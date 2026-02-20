"""
Tests for DOCX converter utilities.
"""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from seamless_pdf.docx_converter import convert_docx_to_html, convert_docx_to_pdf
from seamless_pdf.utils import css_style, detect_input_type, get_css_style
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


def test_convert_docx_to_html_emits_warning_diagnostics(tmp_path):
    docx_path = _make_dummy_docx(tmp_path)
    output_path = tmp_path / "output.html"

    with patch("seamless_pdf.docx_converter.mammoth.convert_to_html") as mock_convert:
        mock_result = MagicMock()
        mock_result.value = "<p>hello</p>"
        mock_result.messages = [
            SimpleNamespace(type="warning", message="Unrecognized paragraph style")
        ]
        mock_convert.return_value = mock_result

        with pytest.warns(UserWarning, match="Unrecognized paragraph style"):
            convert_docx_to_html(str(docx_path), str(output_path))

    assert output_path.exists()


def test_convert_docx_to_html_raises_on_error_diagnostics(tmp_path):
    docx_path = _make_dummy_docx(tmp_path)
    output_path = tmp_path / "output.html"

    with patch("seamless_pdf.docx_converter.mammoth.convert_to_html") as mock_convert:
        mock_result = MagicMock()
        mock_result.value = "<p>hello</p>"
        mock_result.messages = [
            SimpleNamespace(type="warning", message="Unrecognized paragraph style"),
            SimpleNamespace(type="error", message="Image data is corrupted"),
        ]
        mock_convert.return_value = mock_result

        with pytest.raises(ValueError, match="Image data is corrupted"):
            convert_docx_to_html(str(docx_path), str(output_path))

    assert not output_path.exists()


def test_convert_docx_to_pdf_calls_html_pipeline(tmp_path, monkeypatch):
    docx_path = _make_dummy_docx(tmp_path)
    output_path = tmp_path / "output.pdf"

    monkeypatch.chdir(tmp_path)

    with patch("seamless_pdf.docx_converter.convert_docx_to_html") as mock_docx_to_html:
        with patch(
            "seamless_pdf.docx_converter.convert_html_to_pdf"
        ) as mock_html_to_pdf:
            convert_docx_to_pdf(str(docx_path), str(output_path))

    mock_docx_to_html.assert_called_once()
    temp_html_path = mock_docx_to_html.call_args.args[1]
    assert temp_html_path.endswith(".html")
    mock_html_to_pdf.assert_called_once_with(
        temp_html_path, str(output_path), theme="light", width=None
    )
    assert not Path(temp_html_path).exists()


def test_convert_docx_to_pdf_cleans_temp_file_on_failure(tmp_path):
    docx_path = _make_dummy_docx(tmp_path)
    output_path = tmp_path / "output.pdf"

    with patch("seamless_pdf.docx_converter.convert_docx_to_html") as mock_docx_to_html:
        with patch(
            "seamless_pdf.docx_converter.convert_html_to_pdf",
            side_effect=RuntimeError("PDF conversion failed"),
        ):
            with pytest.raises(RuntimeError, match="PDF conversion failed"):
                convert_docx_to_pdf(str(docx_path), str(output_path))

    mock_docx_to_html.assert_called_once()
    temp_html_path = mock_docx_to_html.call_args.args[1]
    assert not Path(temp_html_path).exists()


def test_convert_docx_to_pdf_uses_unique_temp_paths_across_runs(tmp_path):
    docx_path = _make_dummy_docx(tmp_path)
    output_file_a = tmp_path / "output-a.pdf"
    output_file_b = tmp_path / "output-b.pdf"

    with patch("seamless_pdf.docx_converter.convert_docx_to_html") as mock_docx_to_html:
        with patch("seamless_pdf.docx_converter.convert_html_to_pdf"):
            convert_docx_to_pdf(str(docx_path), str(output_file_a))
            convert_docx_to_pdf(str(docx_path), str(output_file_b))

    temp_paths = [call.args[1] for call in mock_docx_to_html.call_args_list]
    assert len(temp_paths) == 2
    assert temp_paths[0] != temp_paths[1]
    assert all(path.endswith(".html") for path in temp_paths)
    assert all(not Path(path).exists() for path in temp_paths)


def test_convert_docx_to_html_uses_dark_theme_css(tmp_path):
    docx_path = _make_dummy_docx(tmp_path)
    output_path = tmp_path / "dark-output.html"

    with patch("seamless_pdf.docx_converter.mammoth.convert_to_html") as mock_convert:
        mock_result = MagicMock()
        mock_result.value = "<p>dark theme</p>"
        mock_result.messages = []
        mock_convert.return_value = mock_result
        convert_docx_to_html(str(docx_path), str(output_path), theme="dark")

    contents = output_path.read_text(encoding="utf-8")
    assert get_css_style("dark") in contents


def test_convert_docx_to_pdf_passes_dark_theme_to_pipeline(tmp_path):
    docx_path = _make_dummy_docx(tmp_path)
    output_path = tmp_path / "output.pdf"

    with patch("seamless_pdf.docx_converter.convert_docx_to_html") as mock_docx_to_html:
        with patch(
            "seamless_pdf.docx_converter.convert_html_to_pdf"
        ) as mock_html_to_pdf:
            convert_docx_to_pdf(str(docx_path), str(output_path), theme="dark")

    temp_html_path = mock_docx_to_html.call_args.args[1]
    mock_docx_to_html.assert_called_once_with(
        str(docx_path), temp_html_path, theme="dark"
    )
    mock_html_to_pdf.assert_called_once_with(
        temp_html_path, str(output_path), theme="dark", width=None
    )


def test_convert_docx_to_pdf_cleans_temp_when_docx_stage_fails(tmp_path):
    docx_path = _make_dummy_docx(tmp_path)
    output_path = tmp_path / "output.pdf"

    with patch(
        "seamless_pdf.docx_converter.convert_docx_to_html",
        side_effect=RuntimeError("DOCX conversion failed"),
    ) as mock_docx_to_html:
        with pytest.raises(RuntimeError, match="DOCX conversion failed"):
            convert_docx_to_pdf(str(docx_path), str(output_path))

    temp_html_path = mock_docx_to_html.call_args.args[1]
    assert not Path(temp_html_path).exists()


def test_detect_input_type_docx():
    assert detect_input_type("file.docx") == "docx"


def test_convert_routes_docx(tmp_path):
    docx_path = _make_dummy_docx(tmp_path)
    output_path = tmp_path / "output.pdf"

    with patch("seamless_pdf.converter.convert_docx_to_pdf") as mock_docx_to_pdf:
        convert(str(docx_path), str(output_path))

    mock_docx_to_pdf.assert_called_once_with(
        str(docx_path), str(output_path), theme="light", width=None
    )
