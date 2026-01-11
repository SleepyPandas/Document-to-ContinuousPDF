# Changelog

All notable changes to this project will be documented in this file.

## [0.1.1] - 2026-01-07

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
