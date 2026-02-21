# Changelog

All notable changes to this project will be documented in this file.

## [1.0.3] - 2026-02-21

### Added
- Expanded PyPI project metadata in `pyproject.toml` including classifiers, keywords, and project URLs to improve sidebar display and discoverability.

## [1.0.2] - 2026-02-20

### Fixed
- Added explicitly defined Trove classifiers to `pyproject.toml` so the correct MIT license badge correctly displays on the package's PyPI index page.

## [1.0.1] - 2026-02-20

### Fixed
- Fixed an issue where fractional pixel rounding in Chromium caused a blank second page to render for certain documents.
- Fixed `pypdf` not installing automatically with `pip install seamless-pdf`.

## [1.0.0] - 2026-02-20

### Added
- **Page Width Control** framework enabling users to constrain extremely wide continuous PDFs via `--width`.
- **Custom Margins** for refined padding on output documents via `--margin-top`, `--margin-right`, `--margin-bottom`, and `--margin-left`.
- **PDF Outlines (Bookmarks)** which automatically evaluate output headings (`<h1>` to `<h6>`) and maps them hierarchically into a native PDF index outline for easy navigation using `pypdf`.

### Changed
- Added `pypdf` as a project dependency.
- Updated `README.md` and tests to accommodate the updated API and CLI interfaces alongside their new test mocking structures.

## [0.4.0] - 2026-02-13

### Added
- Dark/light render theme selection across API and CLI (`theme="dark"` and `--theme dark`).
- Dedicated CSS theme mapping helpers for consistent Markdown and DOCX styling.
- Documented developer extras workflow with coverage / testing tooling support (`pip install -e ".[dev]"`).

### Changed
- Markdown and DOCX conversion pipelines now use unique per-run temporary HTML files with guaranteed cleanup.
- HTML rendering waits for stronger load-state signals before measuring page dimensions and generating PDF.
- README now includes v0.4.0 usage examples and release-focused documentation updates.

### Fixed
- DOCX conversion now surfaces Mammoth diagnostics instead of silently dropping conversion warnings/errors.
- Reduced intermittent PDF generation failures caused by timing/load-state races during HTML rendering.
- Fixed Markdown documents embed tags rendering as plain text

## [0.3.0] - 2026-02-08

### Added
- DOCX to PDF conversion support with `convert_docx_to_html` and `convert_docx_to_pdf`.
- `seamless_pdf.docx_converter` module powered by mammoth.
- Converter facade now accepts `.docx` files and routes them through the new DOCX pipeline.
- `mammoth` added as a project dependency.

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
