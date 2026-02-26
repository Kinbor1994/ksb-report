# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-26

### Added

**Core Engine**
- PDF generation engine with FPDF2 wrapper (`ReportFPDF`)
- Pydantic schemas for JSON-driven report configuration
- Variable resolution system (`{{key}}` placeholders)
- Built-in variables: `current_date`, `current_time`, `year`, `month`, `day`

**13 Content Elements**
- `text` — Rich text with font, style, alignment, color
- `table` — Tables with headers, column widths/aligns, striped rows, auto-pagination
- `image` — Local image rendering with alignment
- `spacer` — Vertical spacing
- `section_title` — Colored section headers
- `key_value` — Label/value pairs
- `page_break` — Forced page breaks
- `separator` — Horizontal line dividers
- `list` — Bulleted, numbered, and dashed lists
- `box` — Bordered containers with nested elements
- `columns` — Multi-column layouts with page-break awareness
- `qrcode` — QR code generation from text/URLs
- `signature_block` — Multi-signature layouts with labels

**Page Configuration**
- Configurable page format (A4, A3, Letter), orientation, margins
- Custom font support (embedded DejaVu Sans)
- Header with logos (left/right), text lines, color bar, separator
- Footer with left/center text, page numbers, date
- Watermark (diagonal text on every page)

**Interfaces**
- Python library API (`ReportEngine`)
- FastAPI HTTP API (`/api/reports/generate`, `/api/reports/preview`)
- CLI tool (`ksb-report serve`, `ksb-report generate`)

**Templates**
- Invoice template (`ksb_report.templates.invoice_template`)

**Documentation**
- Comprehensive README with badges and examples
- User guide with all 13 elements documented
- API reference for HTTP endpoints
- CONTRIBUTING, CODE_OF_CONDUCT, SECURITY policies

**CI/CD**
- GitHub Actions CI (Python 3.10–3.13, ruff lint, pytest)
- GitHub Actions publish to PyPI on tag

[0.1.0]: https://github.com/Kinbor1994/ksb-report/releases/tag/v0.1.0
