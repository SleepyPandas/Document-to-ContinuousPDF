# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2026-01-25

### Added
- Markdown to HTML conversion support with `convert_markdown_to_html` and `convert_markdown_to_pdf`.
- `seamless_pdf.markdown_converter` module.
- Convert Follows Facade Pattern will Take HTML or MD and output a PDF.

## [[0.1.1]](https://github.com/SleepyPandas/Document-to-ContinuousPDF/commits/v0.1.1?since=2026-01-10&until=2026-01-11) - 2026-01-07

### Added
- Custom `PDFConversionError` for conversion failures.
- Tests for converter URL handling and CLI behavior.

### Changed
- Input path handling now resolves relative paths and preserves existing `file://` URLs.
- Conversion errors are wrapped with context for easier debugging.


## [0.1.0] - 2026-01-06

### Added
- Initial release of Seamless PDF.
- Core functionality to convert HTML documents to continuous PDFs using Playwright.
- CLI command `seamless-pdf` for easy usage.
- Configuration management via `pyproject.toml`.
